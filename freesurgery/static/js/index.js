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
        $.get('/getMesh', function(res){
            //var data = JSON.parse(res);
            //console.log(res);
        });
    }

    function render(){
	renderer.render(scene, camera);
    }
});
