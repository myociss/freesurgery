import freesurgery
from sys import argv

def check_parcellation():
    freesurgery.check_parcellation('')

def mri2mesh3d():
    freesurgery.mri2mesh3d(argv[1], argv[2], argv[3])

def mesh2json():
    freesurgery.mesh2json(argv[1])

def view_brain_mesh():
    freesurgery.view_brain_mesh(argv[1], argv[2])
