import meshio, json, pathfinder, os, pygalmesh, tempfile, random, nibabel, numpy as np, time, multiprocessing
from pathlib import Path
from ctypes import c_char, create_string_buffer


#read voxel file into binary + output color map
def mri2mesh3d(subject_file, triangle_size, freesurfer_color_map):
    stack = nibabel.load(subject_file)
    header = stack.header
    a = np.array(stack.dataobj)

    unique_labels = list(np.unique(a))
    unique_labels.remove(0)

    if len(unique_labels) > 254:
        print('error: this file contains more than 255 labels; label values must fit into one byte. support for files with more labels may be added in future releases. email yocissms@gmail.com to request an update or open an issue at https://github.com/myociss/freesurgery/issues.')
        return

    label_dict = {unique_labels[i]: i+1 for i in range(len(unique_labels))}

    x_dim = a.shape[0]
    y_dim = a.shape[1]
    z_dim = a.shape[2]

    voxel_size_x = header.get_zooms()[0]
    voxel_size_y = header.get_zooms()[1]
    voxel_size_z = header.get_zooms()[2]

    item_size = np.dtype(a[0,0,0]).itemsize

    header_attrs = {'XDIM': x_dim, 'YDIM': y_dim, 'ZDIM': z_dim, 'VDIM': 1,
        'TYPE': 'unsigned fixed', 'PIXSIZE': '8 bits', 'CPU': 'decm', 'VX': voxel_size_x, 'VY': voxel_size_y, 'VZ': voxel_size_z}

    inr_header = '#INRIMAGE-4#{\n'

    inr_header += '\n'.join([f'{key}={value}' for key, value in header_attrs.items()])
    header_end = '##}\n'

    hlen = 256 - len(inr_header + header_end)

    inr_header += ''.join(['\n' for i in range(hlen)]) + header_end
    
    data = []

    for i in range(x_dim):
        print('writing slice ' + str(i+1) + ' of ' + str(x_dim))
        for j in range(y_dim):
            for k in range(z_dim):
                 if a[i,j,k].item()==0:
                     data.append(c_char(a[i,j,k].item()))
                 else:
                     data.append(c_char(label_dict[a[i,j,k].item()]))
   

    c_str = create_string_buffer(bytes(inr_header, 'utf-8'))

    fd, path = tempfile.mkstemp()

    with os.fdopen(fd, 'wb') as tmp:
        tmp.write(c_str.raw)
        for char in data:
            tmp.write(char)


    output_file_stem = Path(subject_file).stem.replace('.nii', '').replace('.gz', '')
    

    if triangle_size=='small':
        facet_size=2.0
        facet_distance=0.70
    else:
        facet_size=6.0
        facet_distance=2.0
  
    mesh=pygalmesh.generate_from_inr(path, facet_angle=30.0, facet_size=facet_size, facet_distance=facet_distance, cell_radius_edge_ratio=3.0, cell_size=8.0)
    os.remove(path)

    meshio.write(output_file_stem + '.mesh', mesh)

    if freesurfer_color_map:
        color_map = ['' for i in range(len(unique_labels))]
        with open(freesurfer_color_map, 'r') as f:
            lines = f.readlines()
        for line in lines:
            row = [x.strip() for x in line.split()]
            if len(row) == 6 and row[0].isdigit() and int(row[0]) != 0 and int(row[0]) in label_dict:
                color_map[label_dict[int(row[0])]-1] = '#%02X%02X%02X' % (int(row[2]),int(row[3]),int(row[4]))
    else:
        r = lambda: random.randint(0, 255)
        color_map=['#%02X%02X%02X' % (r(),r(),r()) for i in range(len(unique_labels))]

    with open(output_file_stem + '_colors.txt', 'w') as f:
        for item in color_map:
            f.write(item + '\n')


def mesh2json(mesh_file, weights_file):
    print('reading mesh file...')
    mesh = meshio.read(mesh_file)

    tets = [sorted(tet) for tet in mesh.cells['tetra']]
    tet_labels = [label.item() for label in mesh.cell_data['tetra']['medit:ref']]
    
    with open(weights_file, 'r') as f:
        lines = f.readlines()
        weights = [float(line.strip()) for line in lines]
    
    tet_weights = [weights[label-1] for label in tet_labels]

    vertices_json = [list([comp.item() for comp in p]) for p in mesh.points]

    faces_dict = {}
    tets_json = []
    faces_json = []

    print('converting tetrahedrons to json...')
    for idx, tet in enumerate(tets):
        tet = [v.item() for v in tet]
        tets_json.append({'vertices': tet, 'neighbors':[], 'weight':tet_weights[idx], 'label': tet_labels[idx]})

        for i in range(4):
            face = [tet[j] for j in range(4) if j != i]
            str_face = ','.join([str(v) for v in face])
            if str_face in faces_dict:
                faces_dict[str_face].append(idx)
            else:
                faces_dict[str_face] = [idx]

    print('converting faces to json...')
    for k, v in faces_dict.items():
        if len(v) == 2:
            tets_json[v[0]]['neighbors'].append(v[1])
            tets_json[v[1]]['neighbors'].append(v[0])
        else:
            vertices = [int(vertex) for vertex in k.split(',')]
            faces_json.append({'vertices': vertices, 'tetrahedron': v[0], 'label': tet_labels[v[0]]})

    print('writing mesh to json file...')
    with open(Path(mesh_file).stem + '.json', 'w') as f:
        json.dump({'vertices': vertices_json,'tetrahedrons': tets_json, 'faces': faces_json}, f)


def generate_paths(mesh_file, target, num_slices):
    with open(mesh_file, 'r') as f:
        json_mesh=json.load(f)
    print(target)
    print('reading file into pathfinder mesh...')
    mesh=pathfinder.Mesh(num_vertices=len(json_mesh['vertices']), num_faces=len(json_mesh['faces']), num_tetrahedrons=len(json_mesh['tetrahedrons']))

    mesh.set_vertices(json_mesh['vertices'])

    for idx, tet in enumerate(json_mesh['tetrahedrons']):
        mesh.add_tetrahedron(tetrahedron_id=idx, neighbor_ids=tet['neighbors'], vertex_ids=tet['vertices'], weight=tet['weight'], label=tet['label'])

    for idx, face in enumerate(json_mesh['faces']):
        mesh.add_face(vertex_ids=face['vertices'], tetrahedron_id=face['tetrahedron'])

    
    start=time.time()
    if not mesh.set_target(target):
        print('error: mesh does not contain the target specified')
        return
    end=time.time()
    print('set mesh target in ' + str(end-start) + ' seconds')

    start=time.time()
    mesh.multiple_slices(epsilon=num_slices, threads=multiprocessing.cpu_count())
    end=time.time()
    print(end-start)



