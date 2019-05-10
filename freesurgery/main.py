import meshio, json, pathfinder, os
from flask import Flask
from flask import render_template

app = Flask('freesurgery', template_folder='web')

@app.route('/')
def mesh_view():
    path = os.path.dirname(os.path.realpath(__file__))
    print(os.path.join(path, 'web/index.html'))
    return render_template('index.html')

def view_brain_mesh(json_file, paths_file=None):
    '''
    with open(json_file, 'r') as f:
        mesh = json.load(mesh_file)
    mesh=pathfinder.Mesh(num_vertices=len(self.test_mesh['vertices']), num_faces=len(self.test_mesh['faces']), num_tetrahedrons=len(self.test_mesh['tetrahedrons']))

    mesh.set_vertices(self.test_mesh['vertices'])

    for idx, tet in enumerate(self.test_mesh['tetrahedrons']):
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
        
# these need to be moved into a different file
def check_parcellation(parcellation_labels):
    print('to do: add code to check if parcellation edges can be kept')

def mri2mesh3d(subject_file, keep_parcellation=False, triangle_size='medium'):
    print('to do: add code to mesh mri data and get 3d objects')

def mesh2json(mesh_file, weights, outfile):
    print('this method reads mesh into json format expected by pathfinder')

def get_3d_objects(mesh_file):
    mesh = meshio.read(mesh_file)

