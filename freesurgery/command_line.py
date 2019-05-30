import freesurgery
from sys import argv

def mri2mesh3d():
    if argv[2] not in ['small', 'large']:
        print('please specify small or large triangle size')
        return

    if len(argv)==4:
        color_table=argv[3]
    else:
        color_table=None
    freesurgery.mri2mesh3d(argv[1], argv[2], color_table)

def mesh2json():
    freesurgery.mesh2json(argv[1], argv[2])

def generate_paths():
    target=argv[2].split(',')
    if len(target)==3:
        try:
            target=[float(target[0]), float(target[1]), float(target[2])]
        except ValueError:
            print('target arguments are required to be numeric')
            return
    else:
        print('target argument requires 3 numeric values separated by a comma')
        return

    freesurgery.generate_paths(argv[1], target, int(argv[3]))

def view_mesh():
    freesurgery.view_mesh(argv[1], argv[2])
