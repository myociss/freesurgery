cmake_minimum_required(VERSION 3.1)
project(freesurgery)

add_subdirectory(lib/pybind11)


pybind11_add_module(freesurgery src/freesurgery/bindings.cpp)


#set(SOURCE_DIR "src/freesurgery")
#include_directories(${SOURCE_DIR})
#set(SOURCES "${SOURCE_DIR}/math.cpp")


#pybind11_add_module(freesurgery ${SOURCES} "${SOURCE_DIR}/bindings.cpp")
