# FreeSurgery

Computer-assisted brain surgery planning

## Getting Started

If you are a Windows user, you can use FreeSurgery inside a virtual machine. Support for Windows may be available in future releases.

### Prerequisites

* Python 3
* Eigen
    ```
    sudo apt-get install libeigen3-dev
    ```
* CGAL>=4.13
    ```
    sudo apt-get install libcgal-dev=4.13-1ubuntu3
    ```
* Install pathfinder
    ```
    git clone https://github.com/myociss/pathfinder
    pip install ./pathfinder
    ```

### Installing

```
git clone https://github.com/myociss/freesurgery
pip install ./freesurgery
```

### Subject File Conversion
If  your subject files are not in NIFTI format, convert them to NIFTI using FreeSurfer's mri_convert utility. Example:
```
mri_convert sample-001.mgz sample-001.nii.gz
```