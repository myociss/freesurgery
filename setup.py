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
          'flask',
          'meshio',
          'pygalmesh',
          'nibabel',
      ],
      entry_points={
          'console_scripts':[
'freesurgery_mri2mesh3d=freesurgery.command_line:mri2mesh3d',
'freesurgery_mesh2json=freesurgery.command_line:mesh2json',
'freesurgery_generate_paths=freesurgery.command_line:generate_paths',
'freesurgery_view_mesh=freesurgery.command_line:view_mesh',
          ],
      },
      include_package_data=True,
      zip_safe=False)
