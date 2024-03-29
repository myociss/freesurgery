$(document).ready(function(){

    var camera, scene, renderer, controls, geometry, material, mesh, localPlane, cuttingPlane, paths;

    var cameraX = 0;
    var cameraY = -300;
    var cameraZ = 0;
    
    initScene();
    $('#loading').modal({
        backdrop: "static",
        keyboard: false,
        show: true
    });
    initMesh();
    
    function initScene() {
    
        camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 1, 1000 );
    
        camera.position.set(cameraX, cameraY, cameraZ);
        camera.up = new THREE.Vector3(0, 0, 1);
        camera.lookAt(new THREE.Vector3(0,0,0));
    
        scene = new THREE.Scene();
    
        scene.background = new THREE.Color( 0xf0f0f0 );

        var light = new THREE.DirectionalLight( 0xefefff, 1.5 );
        light.position.set( 1, 1, 1 ).normalize();
        scene.add( light );
        var light = new THREE.DirectionalLight( 0xffefef, 1.5 );
        light.position.set( -1, -1, -1 ).normalize();
        scene.add( light );
    
    
        renderer = new THREE.WebGLRenderer( { antialias: true } );
        renderer.setSize( window.innerWidth, window.innerHeight );
        renderer.localClippingEnabled = true;
    
        document.body.appendChild( renderer.domElement );
    
        controls = new THREE.OrbitControls( camera, renderer.domElement );
        controls.addEventListener( 'change', render );
        render();
    }
    
    function initMesh(){
        var brainGeometry = new THREE.Geometry();
        $.get('/getMesh', function(res){
            $.each(res.vertices, function(i, e){
                var vertex = new THREE.Vector3(e[0], e[1], e[2]);
                brainGeometry.vertices.push(vertex);
            });

            $.each(res.faces, function(i, e){
                var face = new THREE.Face3(e.vertices[0], e.vertices[1], e.vertices[2]);
		        face.color.set(res.color_map[e.label-1]);
                brainGeometry.faces.push(face);
            });
	    brainGeometry.computeFaceNormals();
	    geometry = new THREE.BufferGeometry().fromGeometry( brainGeometry );

            material = new THREE.MeshPhongMaterial( {
		        color: 0xffffff,
                vertexColors: THREE.FaceColors,
                side: THREE.DoubleSide} );

            mesh = new THREE.Mesh(geometry, material);
            scene.add(mesh);
            $('#loading').modal('hide');
            render();
        });
    }

    function render(){
	    renderer.render(scene, camera);
    }

    $('body').on('click', '.plane-bttn', function(){
        var alpha = $('#alpha').val();
        var theta = $('#theta').val();

	$('#loading .modal-body').text('Retrieving slice...');

	$('#loading').modal({
            backdrop: "static",
            keyboard: false,
            show: true
    	});
    
        $.get('/getPlane', {alpha: alpha, theta: theta}, function(res){
            //console.log(res);
            var selectedObject = scene.getObjectByName('currentPlane');
            scene.remove( selectedObject );
            var selectedObject = scene.getObjectByName('currentPaths');
            scene.remove( selectedObject );

            var normalOffset = setClippingPlane(res.normal, res.offset_target_dist, res.offset_target);

            cuttingPlane = new THREE.Geometry();
	    paths = new THREE.Geometry();

	    $.each(res.paths, function(i, e){
		paths.vertices.push(new THREE.Vector3(e[0]-normalOffset.x, e[1]-normalOffset.y, e[2]-normalOffset.z));
		paths.vertices.push(new THREE.Vector3(res.offset_target[0]-normalOffset.x, res.offset_target[1]-normalOffset.y, res.offset_target[2]-normalOffset.z));

	    });

	    var lineMaterial = new THREE.LineBasicMaterial( {color: 0xff0000} );
	    var pathMesh = new THREE.Line(paths, lineMaterial);
	    pathMesh.name = 'currentPaths';
	    scene.add(pathMesh);

            var counter = 0;
	    
	    /*$.each(res.paths, function(i, e){
		var v0 = e.pt0;
		var v1 = e.pt1;
		var v2 = res.offset_target;
		
		cuttingPlane.vertices.push(new THREE.Vector3(v0[0]-normalOffset.x, v0[1]-normalOffset.y, v0[2]-normalOffset.z));

		cuttingPlane.vertices.push(new THREE.Vector3(v1[0]-normalOffset.x, v1[1]-normalOffset.y, v1[2]-normalOffset.z));

		cuttingPlane.vertices.push(new THREE.Vector3(v2[0]-normalOffset.x, v2[1]-normalOffset.y, v2[2]-normalOffset.z));

		var face = new THREE.Face3(counter, counter+1, counter+2);
                face.color.setHex(0xff0000);

		cuttingPlane.faces.push(face);

		counter += 3;

	    });*/

            $.each(res.shapes, function(i, e){
                var shape_vertices = e.vertices;
                var v0 = shape_vertices[0];
                var v1 = shape_vertices[1];
                var v2 = shape_vertices[2];

		//var colorConvert = convertHex(e.color_label);
		//var color = new THREE.Color(colorConvert[0]/255, colorConvert[1]/255, colorConvert[2]/255);

                cuttingPlane.vertices.push(new THREE.Vector3(v0[0], v0[1], v0[2]));
                cuttingPlane.vertices.push(new THREE.Vector3(v1[0], v1[1], v1[2]));
                cuttingPlane.vertices.push(new THREE.Vector3(v2[0], v2[1], v2[2]));

                var face = new THREE.Face3(counter, counter+1, counter+2);

                face.color.set(e.color_label);
		//face.color.set(color);
                cuttingPlane.faces.push(face);

                counter+=3;

                if(shape_vertices.length == 4){
                    var v3 = shape_vertices[3];
                    cuttingPlane.vertices.push(new THREE.Vector3(v0[0], v0[1], v0[2]));
                    cuttingPlane.vertices.push(new THREE.Vector3(v3[0], v3[1], v3[2]));
                    cuttingPlane.vertices.push(new THREE.Vector3(v2[0], v2[1], v2[2]));

                    var face = new THREE.Face3(counter, counter+1, counter+2);
                    face.color.set(e.color_label);
		    //face.color.set(color);
                    cuttingPlane.faces.push(face);

                    counter+=3;
                }

            });
	    cuttingPlane.computeFaceNormals();
            var planeMaterial = new THREE.MeshBasicMaterial( {
		        color: 0xffffff,
                vertexColors: THREE.FaceColors,
                side: THREE.DoubleSide} );

            var crossSection = new THREE.Mesh( cuttingPlane, planeMaterial );
	    //crossSection.rotation.x = Math.PI/2;
            crossSection.name = 'currentPlane';
            scene.add( crossSection );
	    $('#loading').modal('hide');
	    render();
        });

    });

    function setClippingPlane(normal, dist, target){
        var normalVector;
        if (facingCamera(normal, [target[0], target[1], target[2]])){
            normalVector = new THREE.Vector3(-normal[0], -normal[1], -normal[2]);
            normalDist = dist;
        } else {
            normalVector = new THREE.Vector3(normal[0], normal[1], normal[2]);
            normalDist = -dist;
        }
    
        localPlane = new THREE.Plane(normalVector, normalDist);
        material.clippingPlanes = [localPlane];
	return normalVector;
    
    }

    function facingCamera(normal, planeOrigin){
        var endpointDiff = normal;
        var endpointDot = (endpointDiff[0] * endpointDiff[0]) + 
            (endpointDiff[1] * endpointDiff[1]) +
            (endpointDiff[2] * endpointDiff[2]);
    
        var cameraDiff = [cameraX - planeOrigin[0], cameraY - planeOrigin[1], 
            cameraZ - planeOrigin[2]];
        var cameraDot = (normal[0] * cameraDiff[0]) + (normal[1] * cameraDiff[1]) +
            (normal[2] * cameraDiff[2]);
    
        if (cameraDot * endpointDot < 0){
            return false;
        } else {
            return true;
        }
    }

function convertHex(hex){
    hex = hex.replace('#','');
    r = parseInt(hex.substring(0,2), 16);
    g = parseInt(hex.substring(2,4), 16);
    b = parseInt(hex.substring(4,6), 16);

    //r_percentage = r/255;
    //g_percentage = g/255;
    //b_percentage = b/255;

    random_one = Math.random();
    random_two = Math.random();
    if(random_one > 0.5){
	return([r*random_two, g*random_two, b*random_two]);
    } else{
	return([r+((255-r)*random_two),g+((255-g)*random_two),b+((255-b)*random_two)]);
    }
}

});
