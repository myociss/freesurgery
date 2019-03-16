#include "mesh_utils.hpp"
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>

#include <CGAL/Mesh_triangulation_3.h>
#include <CGAL/Mesh_complex_3_in_triangulation_3.h>
#include <CGAL/Mesh_criteria_3.h>

#include <CGAL/Labeled_mesh_domain_3.h>
#include <CGAL/make_mesh_3.h>
#include <CGAL/Image_3.h>

// Domain
typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef CGAL::Labeled_mesh_domain_3<K> Mesh_domain;

typedef CGAL::Sequential_tag Concurrency_tag;

// Triangulation
typedef CGAL::Mesh_triangulation_3<Mesh_domain,CGAL::Default,Concurrency_tag>::type Tr;

typedef CGAL::Mesh_complex_3_in_triangulation_3<Tr> C3t3;

// Criteria
typedef CGAL::Mesh_criteria_3<Tr> Mesh_criteria;

// To avoid verbose function and named parameters call
using namespace CGAL::parameters;


int mesh_nii(char* filename)
{
    CGAL::Image_3 image;
    if(!image.read(filename)){
	return 1;	
    }

    Mesh_domain domain = Mesh_domain::create_labeled_image_mesh_domain(image);
    /// [Domain creation]

    // Mesh criteria
    Mesh_criteria criteria(facet_angle=30, facet_size=6, facet_distance=4,
                         cell_radius_edge_ratio=3, cell_size=8);

    /// [Meshing]
    C3t3 c3t3 = CGAL::make_mesh_3<C3t3>(domain, criteria);
    /// [Meshing]

    // Output
    std::ofstream medit_file("out.mesh");
    c3t3.output_to_medit(medit_file);

    return 0;
}
}

