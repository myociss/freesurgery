#include <pybind11/pybind11.h>
#include "cgal_mesh_image.hpp"

namespace py = pybind11;

PYBIND11_PlUGIN(geometry_core) {
    py::module m("geometry_core");
    m.def("mesh_image", &mesh);
    return m.ptr();
}
