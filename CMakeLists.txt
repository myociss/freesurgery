cmake_minimum_required(VERSION 3.1)
project(geometry_core)

find_package(pybind11)


#pybind11_add_module(freesurgery src/freesurgery/bindings.cpp)


set(SOURCE_DIR "src/freesurgery/geometry_core")
include_directories(${SOURCE_DIR})
set(SOURCES "${SOURCE_DIR}/math.cpp")


pybind11_add_module(geometry_core ${SOURCES} "${SOURCE_DIR}/bindings.cpp")
