from setuptools import setup

setup(name='freesurgery',
      version='0.0.1',
      description='surgery planning application',
      url='http://github.com/myociss/freesurgery',
      author='Megan Yociss',
      author_email='yocissms@gmail.com',
      license='MIT',
      packages=['freesurgery'],
      install_requires=[
          'numpy',
          'meshio',
          'nii2mesh',
      ],
      entry_points={
          'console_scripts':[
'freesurgery_check_parcellation=freesurgery.command_line:check_parcellation',
'freesurgery_mri2mesh3d=freesurgery.command_line:mri2mesh3d',
          ],
      },
      zip_safe=False)
