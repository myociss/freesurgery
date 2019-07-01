import os, json, pathfinder, random, math
import numpy as np

from flask import Flask
from flask import render_template, send_from_directory, jsonify, request

app = Flask('freesurgery')

@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/')
def mesh_view():
    return render_template('index.html')

@app.route('/getMesh')
def send_mesh():
    return jsonify({'vertices': app.config['vertices'], 'faces': app.config['faces'], 'color_map': app.config['color_map']})


@app.route('/getPlane')
def send_plane():
    alpha = int(request.args.get('alpha'))
    theta = int(request.args.get('theta'))
    rotation = [math.pi * alpha / len(app.config['plane_ids']), math.pi * theta / len(app.config['plane_ids'])]
    rotation_x=np.array([[1,0,0], [0,math.cos(rotation[0]),math.sin(rotation[0])], [0,-math.sin(rotation[0]),math.cos(rotation[0])]])
    rotation_y=np.array([[math.cos(rotation[1]),0,math.sin(rotation[1])], [0,1,0], [-math.sin(rotation[1]),0,math.cos(rotation[1])]])
    normal = (np.matmul(rotation_x, rotation_y))[2]
    
    offset_target_dist = np.dot(normal, app.config['offset_target'])

    plane_intersection=app.config['mesh'].slice(rotation=rotation)
    color_map=app.config['color_map']
    offsets = np.array(app.config['vertex_offsets'])

    shapes = [{'vertices': [list(v-offsets) for v in shape.vertices()], 'color_label': color_map[shape.label()-1]} for shape in plane_intersection]

    #print(app.config['paths'][alpha*len(app.config['plane_ids']) + theta])

    return jsonify({'shapes': shapes, 'paths': app.config['paths'][alpha*len(app.config['plane_ids']) + theta], 'offset_target': app.config['offset_target'], 'normal': list(normal), 'offset_target_dist': offset_target_dist})


def view_mesh(mesh_file, color_map_file, paths_file):
    print('reading mesh file...')
    with open(mesh_file, 'r') as f:
        json_mesh = json.load(f)
    
    vertex_mins = [min(map(lambda vertex: vertex[i], json_mesh['vertices'])) for i in range(3)]
    vertex_maxs = [max(map(lambda vertex: vertex[i], json_mesh['vertices'])) for i in range(3)]
    vertex_mids = [(vertex_maxs[i] - vertex_mins[i]) / 2 for i in range(3)]

    app.config['vertex_offsets'] = vertex_mids
    app.config['vertices'] = [[v[i] - vertex_mids[i] for i in range(3)] for v in json_mesh['vertices']]

    with open(color_map_file, 'r') as f:
        color_map = [line.strip() for line in f.readlines()]

    app.config['color_map'] = color_map
    app.config['faces'] = json_mesh['faces']
    app.config['mesh']=load_pathfinder_mesh(json_mesh)

    print('reading paths file...')
    with open(paths_file, 'r') as f:
        json_paths = json.load(f)

    target=json_paths['target']
    app.config['mesh'].set_target(target)
    app.config['offset_target'] = [target[0] - vertex_mids[0], target[1] - vertex_mids[1], target[2] - vertex_mids[2]]

    num_slices=json_paths['num_slices']
    #check [100,100,150] at 2, 0
    app.config['plane_ids']=[i for i in range(num_slices)]

    paths=[[] for i in range(num_slices*num_slices)]
    offsets = np.array(app.config['vertex_offsets'])

    for path in json_paths['paths']:
        plane_id=path['alpha_id'] * num_slices + path['theta_id']
        view_path={'pt0': list(path['point_0']-offsets), 'pt1': list(path['point_1']-offsets)}
        paths[plane_id].append(view_path)

    for plane_id, path_group in enumerate(paths):
        if len(path_group) > 0:
            print(f'{len(path_group)} paths in plane ({plane_id//num_slices}, {plane_id%num_slices})')

    app.config['paths']=paths

    os.environ['FLASK_ENV'] = 'development'
    app.run()

def load_pathfinder_mesh(json_mesh):
    mesh=pathfinder.Mesh(num_vertices=len(json_mesh['vertices']), num_faces=len(json_mesh['faces']), num_tetrahedrons=len(json_mesh['tetrahedrons']))

    mesh.set_vertices(json_mesh['vertices'])

    for idx, tet in enumerate(json_mesh['tetrahedrons']):
        mesh.add_tetrahedron(tetrahedron_id=idx, neighbor_ids=tet['neighbors'], vertex_ids=tet['vertices'], weight=tet['weight'], label=tet['label'])

    for face in json_mesh['faces']:
        mesh.add_face(vertex_ids=face['vertices'], tetrahedron_id=face['tetrahedron'])
    return mesh

