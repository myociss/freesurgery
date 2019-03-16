#include <pybind11/pybind11.h>
#include "mesh_utils.hpp"

namespace py = pybind11;

PYBIND11_PLUGIN(geometry_core)
{
    py::module m("geometry_core");
    m.def("mesh_nii", &mesh_nii);
    return m.ptr();
}
