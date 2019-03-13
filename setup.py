from setuptools import setup, find_packages

setup(
    name='freesurgery',
    version='0.1',
    install_requires=['nipy'],
    author='Megan Yociss',
    author_email='yocissms@gmail.com',
    description='surgery planning application written in python and c++',
    long_description='',
    packages=find_packages('src'),
    package_dir={'':'src'},
)