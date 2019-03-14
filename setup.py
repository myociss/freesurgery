from setuptools import setup, find_packages

setup(
    name='freesurgery',
    version='0.1',
    install_requires=['nipy', 'pyqt5'],
    author='Megan Yociss',
    author_email='yocissms@gmail.com',
    description='surgery planning application written in python and c++',
    long_description='',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'':'src'},
    entry_points = {
        'console_scripts': ['freesurgery=freesurgery.command_line'],
    }
)