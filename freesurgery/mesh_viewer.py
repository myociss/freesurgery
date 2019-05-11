import os

from flask import Flask
from flask import render_template, send_from_directory

app = Flask('freesurgery')
mesh = None

@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/')
def mesh_view():
    path = os.path.dirname(os.path.realpath(__file__))
    return render_template('index.html')

def view_brain_mesh(json_file, paths_file=None):
    '''
    with open(json_file, 'r') as f:
        json_mesh = json.load(mesh_file)
    mesh=pathfinder.Mesh(num_vertices=len(json_mesh['vertices']), num_faces=len(json_mesh['faces']), num_tetrahedrons=len(json_mesh['tetrahedrons']))

    mesh.set_vertices(json_mesh['vertices'])

    for idx, tet in enumerate(json_mesh['tetrahedrons']):
        mesh.add_tetrahedron(tetrahedron_id=idx, neighbor_ids=tet['neighbors'], vertex_ids=tet['vertices'], weight=tet['weight'])

    for face in self.test_mesh['faces']:
        mesh.add_face(vertex_ids=face['vertices'], tetrahedron_id=face['tetrahedron'])
    '''

    os.environ['FLASK_ENV'] = 'development'
    app.run()

    #if paths_file:
     #   print('this happens')
        # execute find path code
    #else:
