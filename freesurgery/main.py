import meshio

def check_parcellation(parcellation_labels):
    print('to do: add code to check if parcellation edges can be kept')

def mri2mesh3d(subject_file, keep_parcellation=False, triangle_size='medium'):
    print('to do: add code to mesh mri data and get 3d objects')

def mesh2json(mesh_file, weights):
    print('this method reads mesh into json format expected by pathfinder')

def get_3d_objects(mesh_file):
    mesh = meshio.read(mesh_file)
