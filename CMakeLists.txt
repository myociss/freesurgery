cmake_minimum_required(VERSION 3.1)
project(geometry_core)

# CGAL and its components
find_package( CGAL QUIET COMPONENTS  )

if ( NOT CGAL_FOUND )

  message(STATUS "This project requires the CGAL library, and will not be compiled.")
  return()  

endif()

# include helper file
include( ${CGAL_USE_FILE} )


# Boost and its components
find_package( Boost REQUIRED )

if ( NOT Boost_FOUND )

  message(STATUS "This project requires the Boost library, and will not be compiled.")

  return()  

endif()



find_package(pybind11)

if (NOT pybind11_FOUND)
    message(STATUS "this package requires pybind11 to be installed")
    return()
endif()

#pybind11_add_module(geometry_core src/freesurgery/geometry_core/bindings.cpp)


set(SOURCE_DIR "src/freesurgery/geometry_core")
include_directories(${SOURCE_DIR})
set(SOURCES "${SOURCE_DIR}/mesh_utils.cpp")


pybind11_add_module(geometry_core ${SOURCES} "${SOURCE_DIR}/bindings.cpp")
