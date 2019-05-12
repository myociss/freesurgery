//alert('here');
$(document).ready(function(){
    var camera, scene, renderer, controls, geometry, material, mesh, localPlane;

    var cameraX = -400;
    var cameraY = 0;
    var cameraZ = 0;
    
    initScene();
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
	    console.log(res)
            $.each(res.vertices, function(i, e){
                var vertex = new THREE.Vector3(e[0], e[1], e[2]);
                brainGeometry.vertices.push(vertex);
            });

            $.each(res.faces, function(i, e){
                var face = new THREE.Face3(e.vertices[0], e.vertices[1], e.vertices[2]);
		face.color.set(res.color_map[e.label]);
                brainGeometry.faces.push(face);
            });
	    brainGeometry.computeFaceNormals();
	    geometry = new THREE.BufferGeometry().fromGeometry( brainGeometry );

            var material = new THREE.MeshPhongMaterial( {
		color: 0xffffff,
                vertexColors: THREE.FaceColors,
                side: THREE.DoubleSide} );

            mesh = new THREE.Mesh(geometry, material);
            scene.add(mesh);
            render();
        });
    }

    function render(){
	renderer.render(scene, camera);
    }
});
