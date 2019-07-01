# FreeSurgery

Computer-assisted brain surgery planning

## Getting Started

### Prerequisites

Python 3, git, pip3.

### Dependencies

Follow instructions to install [pathfinder](https://github.com/myociss/pathfinder).

Install CGAL.
```
sudo install libcgal-dev
```

### Installation

```
git clone https://github.com/myociss/freesurgery
pip3 install ./freesurgery
```

## Usage

To obtain a mesh and color map from a subject file: freesurgery_mri2mesh3d subject_file.nii facet_size

```
$ freesurgery_mri2mesh3d aparc_aseg.nii.gz small
```

To obtain a mesh from a subject file using FreeSurfer's color lookup table:

```
$ freesurgery_mri2mesh3d aparc_aseg.nii.gz small $FREESURFER_HOME/FreeSurferColorLUT.txt
```

To assign weights to a mesh and convert it to pathfinder's expected format: freesurgery_mesh2json mesh_file.mesh weights_file.txt

```
$ freesurgery_mesh2json aparc_aseg.mesh weights.txt
```

To generate a list of paths: freesurgery_generate_paths mesh_json.json target planes_to_search width_bound

```
$ freesurgery_generate_paths aparc_aseg.json “100,100,150” 16 0.01
```

To view a mesh with paths: freesurgery_view_mesh mesh_json.json color_map.txt paths.json

```
$ freesurgery_view_mesh aparc_aseg.json aparc_aseg_colors.txt aparc_aseg_paths.json
```