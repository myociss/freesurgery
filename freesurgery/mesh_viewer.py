import os, json, pathfinder, random, math
import numpy as np

from flask import Flask
from flask import render_template, send_from_directory, jsonify, request

app = Flask('freesurgery')
#json_mesh = None
#mesh = None

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
    shapes = []
    for shape in plane_intersection:
        vertices = [[v[i] - app.config['vertex_offsets'][i] for i in range(3)] for v in shape.vertices()]
        color_label = app.config['color_map'][shape.label()-1]
        shapes.append({'vertices': vertices, 'color_label': color_label})


    return jsonify({'shapes': shapes, 'offset_target': app.config['offset_target'], 'normal': list(normal), 'offset_target_dist': offset_target_dist})

def view_brain_mesh(mesh_file, color_map_file, paths_file=None):
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
    app.config['mesh'].set_target([100, 100, 150])
    app.config['offset_target'] = [100 - vertex_mids[0], 100 - vertex_mids[1], 150 - vertex_mids[2]]

    # this should not be hardcoded but read in from file
    app.config['plane_ids'] = [i for i in range(8)]

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

