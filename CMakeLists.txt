cmake_minimum_required(VERSION 3.1)
project(freesurgery)

find_package(CGAL REQUIRED)
find_package(CGAL COMPONENTS ImageIO)
find_package(Eigen3 3.1.0 REQUIRED)
find_package(Boost 103400 REQUIRED)
find_package(pybind11 REQUIRED)

set(SOURCE_DIR "src/freesurgery/geometry_core")
include_directories("${SOURCE_DIR}")
set(SOURCES "${SOURCE_DIR}/mesh_utils/cgal_mesh_image.cpp")

pybind11_add_module(geometry_core ${SOURCES} "{SOURCE_DIR}/bindings.cpp")