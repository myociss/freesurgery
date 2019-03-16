#from .gui import app
import geometry_core

def main():
    #app()
    #print(geometry_core.add(1,1))
    geometry_core.mesh_nii('~/Downloads/liver.inr.gz')

if __name__=='__main__':
    main()
