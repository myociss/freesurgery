import meshio, json, pathfinder, os, nii2mesh, tempfile, random
from pathlib import Path
#from flask import Flask
#from flask import render_template

#app = Flask('freesurgery', template_folder='web')

# all this needs to be moved into a different file
#@app.route('/')
#def mesh_view():
#    path = os.path.dirname(os.path.realpath(__file__))
#    print(os.path.join(path, 'web/index.html'))
#    return render_template('index.html')

#def view_brain_mesh(json_file, paths_file=None):
#    '''
#    with open(json_file, 'r') as f:
#        mesh = json.load(mesh_file)
#    mesh=pathfinder.Mesh(num_vertices=len(self.test_mesh['vertices']), #num_faces=len(self.test_mesh['faces']), #num_tetrahedrons=len(self.test_mesh['tetrahedrons']))

#    mesh.set_vertices(self.test_mesh['vertices'])

#    for idx, tet in enumerate(self.test_mesh['tetrahedrons']):
#        mesh.add_tetrahedron(tetrahedron_id=idx, neighbor_ids=tet['neighbors'], vertex_ids=tet['vertices'], weight=tet['weight'])

#    for face in self.test_mesh['faces']:
#        mesh.add_face(vertex_ids=face['vertices'], tetrahedron_id=face['tetrahedron'])
#    '''

#    os.environ['FLASK_ENV'] = 'development'
#    app.run()

    #if paths_file:
     #   print('this happens')
        # execute find path code
    #else:
        
def check_parcellation(parcellation_labels):
    print('to do: add code to check if parcellation edges can be kept')

def mri2mesh3d(subject_file, keep_parcellation=False, triangle_size='medium'):
    fd, path = tempfile.mkstemp()
    print('writing subject file to binary....')
    nii2mesh.nii2inr(subject_file, fd)
    nii2mesh.generate_mesh(path, Path(subject_file).stem.replace('.nii', '').replace('.gz', '') + '.mesh', facet_distance=0.70, facet_size=2.0)
    os.remove(path)


# need to include weight information
def mesh2json(mesh_file):
    print('reading mesh file...')
    mesh = meshio.read(mesh_file)

    tets = [sorted(tet) for tet in mesh.cells['tetra']]
    tet_labels = [label.item() for label in mesh.cell_data['tetra']['medit:ref']]

    vertices_json = [list([comp.item() for comp in p]) for p in mesh.points]

    faces_dict = {}
    tets_json = []
    faces_json = []

    print('converting tetrahedrons to json...')
    for idx, tet in enumerate(tets):
        tet = [v.item() for v in tet]
        tets_json.append({'vertices': tet, 'neighbors':[], 'weight':random.random()})#, 'label': tet_labels[idx]})

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


def get_3d_objects(mesh_file):
    mesh = meshio.read(mesh_file)

