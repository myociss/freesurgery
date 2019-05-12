import os, json, pathfinder, random

from flask import Flask
from flask import render_template, send_from_directory, jsonify

app = Flask('freesurgery')
#json_mesh = None
#mesh = None

@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/')
def mesh_view():
    return render_template('index.html')

@app.route('/getMesh')
def send_mesh():
    return jsonify({'vertices': app.config['vertices'], 'faces': app.config['faces'], 'color_map': app.config['color_map']})

#def get_json_mesh():
#    return json_mesh

def view_brain_mesh(mesh_file, color_map_file=None, paths_file=None):
    print('reading mesh file...')
    with open(mesh_file, 'r') as f:
        json_mesh = json.load(f)

    #mesh=load_pathfinder_mesh(json_mesh)
    
    vertex_mins = [min(map(lambda vertex: vertex[i], json_mesh['vertices'])) for i in range(3)]
    vertex_maxs = [max(map(lambda vertex: vertex[i], json_mesh['vertices'])) for i in range(3)]
    vertex_mids = [(vertex_maxs[i] - vertex_mins[i]) / 2 for i in range(3)]

    app.config['vertices'] = [[v[i] - vertex_mids[i] for i in range(3)] for v in json_mesh['vertices']]

    if color_map_file:
        color_map = color_map_file
    else:
        labels = [tet['label'] for tet in json_mesh['tetrahedrons']]
        num_labels = max(labels)
        color_map = []
        r = lambda: random.randint(0, 255)
        for i in range(num_labels):
            color_map.append('#%02X%02X%02X' % (r(),r(),r()))
    app.config['color_map'] = color_map
    app.config['faces'] = json_mesh['faces']

    os.environ['FLASK_ENV'] = 'development'
    app.run()

def load_pathfinder_mesh(json_mesh):
    mesh=pathfinder.Mesh(num_vertices=len(json_mesh['vertices']), num_faces=len(json_mesh['faces']), num_tetrahedrons=len(json_mesh['tetrahedrons']))

    mesh.set_vertices(json_mesh['vertices'])

    for idx, tet in enumerate(json_mesh['tetrahedrons']):
        mesh.add_tetrahedron(tetrahedron_id=idx, neighbor_ids=tet['neighbors'], vertex_ids=tet['vertices'], weight=tet['weight'])

    for face in json_mesh['faces']:
        mesh.add_face(vertex_ids=face['vertices'], tetrahedron_id=face['tetrahedron'])
    return mesh

    #if paths_file:
     #   print('this happens')
        # execute find path code
    #else:
