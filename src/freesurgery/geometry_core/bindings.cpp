#include <pybind11/pybind11.h>
#include "math.hpp"

namespace py = pybind11;

PYBIND11_PLUGIN(freesurgery)
{
    py::module m("freesurgery");
    m.def("add", &add);
    return m.ptr();
}
