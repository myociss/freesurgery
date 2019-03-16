cmake_minimum_required(VERSION 3.1)
project(geometry_core)


find_package(CGAL COMPONENTS ImageIO)

if ( CGAL_FOUND )
  include( ${CGAL_USE_FILE} )

  find_package(Boost)

  
  # Use Eigen
  find_package(Eigen3 3.1.0 REQUIRED) #(3.1.0 or greater)
  if (NOT EIGEN3_FOUND)
    message(STATUS "This project requires the Eigen library, and will not be compiled.")
    return()
  else()
    include( ${EIGEN3_USE_FILE} )
  endif()
  
 set(VTK_LIBS "")
      find_package(VTK QUIET COMPONENTS vtkImagingGeneral  vtkIOImage NO_MODULE)
      if(VTK_FOUND)
          include(${VTK_USE_FILE})
          if ("${VTK_VERSION_MAJOR}" GREATER "5")
            message(STATUS "VTK found")
            set( VTK_LIBS vtkImagingGeneral vtkIOImage )
          else()
            message(STATUS "VTK version 6.0 or greater is required")
          endif()
      else()
        message(STATUS "VTK was not found")
      endif()


  if ( Boost_FOUND AND Boost_VERSION GREATER 103400 )

    
    if( WITH_CGAL_ImageIO )

      if( NOT CGAL_ImageIO_USE_ZLIB )
        message( STATUS "NOTICE: this program requires CGAL_ImageIO to be configured with ZLIB support, and will not be compiled." )
      endif()
    else()
      message( STATUS "NOTICE: Some examples need the CGAL_ImageIO library, and will not be compiled." )
    endif()


      else()
	message(STATUS "NOTICE: This program requires Boost >= 1.34.1, and will not be compiled.")
	return()
      endif()

else()
    message(STATUS "This program requires the CGAL library, and will not be compiled.")
    return()
endif()





find_package(pybind11)


#pybind11_add_module(freesurgery src/freesurgery/bindings.cpp)


set(SOURCE_DIR "src/freesurgery/geometry_core")
include_directories(${SOURCE_DIR})
set(SOURCES "${SOURCE_DIR}/mesh_utils.cpp")


pybind11_add_module(geometry_core ${SOURCES} "${SOURCE_DIR}/bindings.cpp")
