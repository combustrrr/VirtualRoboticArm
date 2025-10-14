/**
 * 
 *  Document     : scene.js
 *  Created on   : 13 April, 2016, 4:45:25 PM
 *  Author       : Ujjal Dey
 *  Organization : IIT Khatagpur
 *  
 */
var PUMA560 = {
    scene: null,
    camera: null,
    container: null,
    stats: null,
    controls: null,
    renderer: null,
    CONTAINER_WIDTH: null,
    CONTAINER_HEIGHT: null,
    link2Mesh: null,
    Link3Mesh: null,
    Link4Mesh: null,
    CylinderL2: null,
    CylinderL6: null,
    Cylinder4L5: null,
    Cylinder3L5: null,
    BoxL5: null,
    init: function () {
// create main scene
        this.scene = new THREE.Scene();
        this.container = document.getElementById("canvas3d-view");
        this.scene.position.set(60, -500, 0);
        this.CONTAINER_WIDTH = this.container.offsetWidth;
        this.CONTAINER_HEIGHT = this.container.offsetHeight;
//  renderer
        this.renderer = new THREE.WebGLRenderer({antialias: true, alpha: false});
        this.renderer.setSize(this.CONTAINER_WIDTH, this.CONTAINER_HEIGHT);
        this.renderer.setClearColor(0x000000, 1); // Set the background color of the canvas to black
        this.renderer.shadowMapEnabled = true;
        this.renderer.shadowMapSoft = true;
        this.container.appendChild(this.renderer.domElement);
// camera
        var VIEW_ANGLE = 45, ASPECT = this.CONTAINER_WIDTH / this.CONTAINER_HEIGHT, NEAR = 1, FAR = 10000;
        this.camera = new THREE.PerspectiveCamera(VIEW_ANGLE, ASPECT, NEAR, FAR);
        //this.camera.position.z = 500;
        this.camera.position.set(1000, 100, 1500);   //
        //this.camera.lookAt(new THREE.Vector3(0, 0, 0));
        this.camera.lookAt(this.scene.position);
//        this.scene.add(this.camera);
        var dirLight = new THREE.DirectionalLight(0xffffff, 2);
        dirLight.position.set(500, 0, 500);
        this.scene.add(dirLight);

        var dirLight1 = new THREE.DirectionalLight(0xffffff, 1);
        dirLight1.position.set(0, 150, -500);
        this.scene.add(dirLight1);

        this.controls = new THREE.TrackballControls(this.camera);
        this.controls.rotateSpeed = 1.0;
        this.controls.zoomSpeed = 1.2;
        this.controls.panSpeed = 0.8;
        this.controls.noZoom = false;
        this.controls.noPan = false;
        this.controls.staticMoving = true;
        this.controls.dynamicDampingFactor = 0.3;
        this.controls.keys = [65, 83, 68];
        this.controls.enabled = false;
        // this.controls.addEventListener('change', render);
// Stats preparing
        this.stats = new Stats();
        this.stats.domElement.style.position = 'absolute';
        this.stats.domElement.style.top = '180px';
        this.container.appendChild(this.stats.domElement);
// scene
// Add axes, The X axis is red. The Y axis is green. The Z axis is blue.
        axes = buildAxes(200);
        //axes.position = mesh.position;
        this.scene.add(axes);

        gridX = new THREE.GridHelper(600, 10);    //green
        gridX.setColors(new THREE.Color(0x660000), new THREE.Color(0x660000));
        gridX.position.set(0, 0, 0);
        this.scene.add(gridX);

        gridZ = new THREE.GridHelper(600, 10);
        gridZ.position.set(0, 600, -600);
        gridZ.rotation.x = Math.PI / 2;
        gridZ.setColors(new THREE.Color(0x000066), new THREE.Color(0x000066));
        this.scene.add(gridZ);

        gridY = new THREE.GridHelper(600, 10);
        gridY.position.set(-600, 600, 0);
        gridY.rotation.z = Math.PI / 2;
        gridY.setColors(new THREE.Color(0x006600), new THREE.Color(0x006600));
        this.scene.add(gridY);
// create geometries 
//create link1
        Cylinder1 = new THREE.Mesh(new THREE.CylinderGeometry(140, 150, 30, 100), new THREE.MeshNormalMaterial());
        Cylinder1.position.set(0, 15, 0);
        Cylinder2L1 = new THREE.Mesh(new THREE.CylinderGeometry(45, 45, 600, 100), new THREE.MeshNormalMaterial());
        Cylinder2L1.position.set(0, 300, 0);
        link1 = new THREE.Geometry();
        THREE.GeometryUtils.merge(link1, Cylinder1);
        THREE.GeometryUtils.merge(link1, Cylinder2L1);
        link1Mesh = new THREE.Mesh(link1, new THREE.MeshPhongMaterial({color: "#3E3E3C"}));
        this.scene.add(link1Mesh);

//create Link2
        this.CylinderL2 = new THREE.Mesh(new THREE.CylinderGeometry(47, 47, 200, 100), new THREE.MeshNormalMaterial());
        this.CylinderL2.position.set(40, 210, 0);
        this.CylinderL2.rotation.z += Math.PI / 2;
        //this.CylinderL2.rotation.y += Math.PI / 2;
        Cylinder2L2 = new THREE.Mesh(new THREE.CylinderGeometry(46.5, 46.5, 60, 100), new THREE.MeshNormalMaterial());
        Cylinder2L2.position.set(0, 170, 0);

        link2 = new THREE.Geometry();
        this.CylinderL2.updateMatrix(); // as needed
        link2.merge(this.CylinderL2.geometry, this.CylinderL2.matrix);
        Cylinder2L2.updateMatrix(); // as needed
        link2.merge(Cylinder2L2.geometry, Cylinder2L2.matrix);
        this.link2Mesh = new THREE.Mesh(link2, new THREE.MeshPhongMaterial({color: "#859D9D"}));
        this.link2Mesh.position.set(0, 375, 0);
        //this.link2Mesh.rotation.x = Math.PI / 2;
        link1Mesh.add(this.link2Mesh);
//create Link3
        CylinderL3 = new THREE.Mesh(new THREE.CylinderGeometry(81.7, 81.7, 70, 100), new THREE.MeshBasicMaterial({color: 0xffff00}));
        CylinderL3.position.set(0, 11, 0);
        CylinderL3.rotation.z += Math.PI / 2;
//CylinderL3.rotation.y += Math.PI / 2;
        BoxL3 = new THREE.Mesh(new THREE.BoxGeometry(70, 90, 163), new THREE.MeshNormalMaterial());
        BoxL3.position.set(0, 50, 0);
        // BoxL3.overdraw=true;
        materialFront = new THREE.MeshBasicMaterial({color: 0xff0000});
        materialSide = new THREE.MeshBasicMaterial({color: 0x000088});
        materialArray = [materialFront, materialSide];
        textGeom = new THREE.TextGeometry("PUMA", {size: 30, height: 4, curveSegments: 3, font: "helvetiker", weight: "bold", style: "normal", bevelThickness: 1, bevelSize: 2, bevelEnabled: false, material: 0, extrudeMaterial: 7});
        textMaterial = new THREE.MeshFaceMaterial(materialArray);
        textMesh = new THREE.Mesh(textGeom, textMaterial);
        textGeom.computeBoundingBox();
        textMesh.position.set(35, 200, 0);
        textMesh.rotation.z = -Math.PI / 2;
        textMesh.rotation.y = +Math.PI / 2;

        Box2L3 = new THREE.Mesh(new THREE.BoxGeometry(70, 80, 250), new THREE.MeshNormalMaterial());
        Box2L3.position.set(0, 211.3, -20.95);
        Box2L3.rotation.x += Math.PI / 2;
        Box2L3.rotation.x += 0.17;

        Box3L3 = new THREE.Mesh(new THREE.BoxGeometry(70, 80, 250), new THREE.MeshNormalMaterial());
        Box3L3.position.set(0, 211.3, 20.95);
        Box3L3.rotation.x += Math.PI / 2;
        Box3L3.rotation.x -= 0.17;

        Cylinder2L3 = new THREE.Mesh(new THREE.CylinderGeometry(50, 50, 30, 100), new THREE.MeshNormalMaterial());
        Cylinder2L3.position.set(-40, 0, 0);
        Cylinder2L3.rotation.z += Math.PI / 2;
        //Cylinder2L3.rotation.y+= Math.PI / 2;
        //this.scene.add(Cylinder2L3);

        Cylinder3L3 = new THREE.Mesh(new THREE.CylinderGeometry(40.6, 40.6, 70, 100), new THREE.MeshNormalMaterial());
        Cylinder3L3.position.set(0, 330, 0);
        Cylinder3L3.rotation.z += Math.PI / 2;
        Cylinder3L3.overdraw = false;
//Link3
        this.Cylinderextra = new THREE.Mesh(new THREE.CylinderGeometry(40.6, 40.6, 10, 100), new THREE.MeshNormalMaterial());
        this.Cylinderextra.position.set(0, 210, 0)
        this.Cylinderextra.rotation.x += Math.PI / 2;
        this.link2Mesh.add(this.Cylinderextra);
        Link3 = new THREE.Geometry();
        //THREE.GeometryUtils.merge(Link3, this.link2Mesh);
        THREE.GeometryUtils.merge(Link3, Cylinder2L3);
        THREE.GeometryUtils.merge(Link3, CylinderL3);
        THREE.GeometryUtils.merge(Link3, BoxL3);
        THREE.GeometryUtils.merge(Link3, Box2L3);
        THREE.GeometryUtils.merge(Link3, Box3L3);
        THREE.GeometryUtils.merge(Link3, Cylinder3L3);
        THREE.GeometryUtils.merge(Link3, textMesh);
        this.Link3Mesh = new THREE.Mesh(Link3, new THREE.MeshPhongMaterial({color: "#7E8274"}));
        this.Link3Mesh.position.set(190, 0, 0);
        //PUMA560.Link3Mesh.rotation.z= Math.PI / 2;
        // PUMA560.Link3Mesh.rotation.x= Math.PI / 2;
        //this.scene.add(axes);
        this.Cylinderextra.add(this.Link3Mesh);

        //create Link 4
        Box2L4 = new THREE.Mesh(new THREE.BoxGeometry(60, 60, 180), new THREE.MeshNormalMaterial());
        Box2L4.position.set(-70, 90, -19);
        Box2L4.rotation.x += Math.PI / 2;
        Box2L4.rotation.x += 0.072;

        Box3L4 = new THREE.Mesh(new THREE.BoxGeometry(60, 60, 180), new THREE.MeshNormalMaterial());
        Box3L4.position.set(-70, 90, 19);
        Box3L4.rotation.x += Math.PI / 2;
        Box3L4.rotation.x -= 0.072;

        CylinderL4 = new THREE.Mesh(new THREE.CylinderGeometry(55, 55, 60, 100), new THREE.MeshNormalMaterial());
        CylinderL4.position.set(-70, 5, 0);
        CylinderL4.rotation.z += Math.PI / 2;

        Cylinder2L4 = new THREE.Mesh(new THREE.CylinderGeometry(20, 20, 40, 100), new THREE.MeshNormalMaterial());
        Cylinder2L4.position.set(-30, 0, 0);
        Cylinder2L4.rotation.z += Math.PI / 2;
        // Cylinder2L4.rotation.x += Math.PI / 2;
        //Box3L4.add(Cylinder2L4);

        this.Cylinderextra1 = new THREE.Mesh(new THREE.CylinderGeometry(10, 10, 10, 100), new THREE.MeshNormalMaterial());
        //this.Cylinderextra1.position.set(0,210,0)
        this.Cylinderextra1.rotation.x += Math.PI / 2;
        this.Link3Mesh.add(this.Cylinderextra1);
        Link4 = new THREE.Geometry();
        THREE.GeometryUtils.merge(Link4, Cylinder2L4);
        THREE.GeometryUtils.merge(Link4, Box2L4);
        THREE.GeometryUtils.merge(Link4, Box3L4);
        THREE.GeometryUtils.merge(Link4, CylinderL4);
        this.Link4Mesh = new THREE.Mesh(Link4, new THREE.MeshPhongMaterial({color: "#859595", transparent: false, blending: THREE.AdditiveBlending}));
        this.Link4Mesh.position.set(0, 0, -320);
        this.Cylinderextra1.add(this.Link4Mesh);

        // Create Link 5
        Box2L5 = new THREE.Mesh(new THREE.BoxGeometry(60.05, 5, 85.95), new THREE.MeshPhongMaterial({color: "#6A736B"}));
        Box2L5.position.set(-70, 181, 0);
        this.Link4Mesh.add(Box2L5);

        this.BoxL5 = new THREE.Mesh(new THREE.BoxGeometry(60, 40, 80), new THREE.MeshPhongMaterial({color: "#6A736B"}));
        this.BoxL5.position.set(0, 22, 0);
        Box2L5.add(this.BoxL5);

        Cylinder2L5 = new THREE.Mesh(new THREE.CylinderGeometry(40, 40, 20, 100), new THREE.MeshPhongMaterial({color: "#6A736B"}));
        Cylinder2L5.position.set(-20, 50, 0);
        Cylinder2L5.rotation.z += Math.PI / 2;
        this.BoxL5.add(Cylinder2L5);

        this.Cylinder3L5 = new THREE.Mesh(new THREE.CylinderGeometry(40, 40, 20, 100), new THREE.MeshBasicMaterial({color: "pink", transparent: false, blending: THREE.AdditiveBlending}));
        this.Cylinder3L5.position.set(0, 50, 0);
        this.Cylinder3L5.rotation.z += Math.PI / 2;
        this.BoxL5.add(this.Cylinder3L5);

        this.Cylinder4L5 = new THREE.Mesh(new THREE.CylinderGeometry(40, 40, 20, 100), new THREE.MeshPhongMaterial({color: "#6A736B"}));
        this.Cylinder4L5.position.set(20, 50, 0);
        this.Cylinder4L5.rotation.z += Math.PI / 2;
        this.BoxL5.add(this.Cylinder4L5);

        Cylinder5L5 = new THREE.Mesh(new THREE.CylinderGeometry(20, 20, 60, 10), new THREE.MeshPhongMaterial({color: "#6A736B"}));
        this.BoxL5.add(Cylinder5L5);
        Cylinder5L5.rotation.z += Math.PI / 2;
        Cylinder5L5.position.set(0, 20, 20);

        Cylinder6L5 = new THREE.Mesh(new THREE.CylinderGeometry(20, 20, 60, 10), new THREE.MeshPhongMaterial({color: "#6A736B"}));
        this.BoxL5.add(Cylinder6L5);
        Cylinder6L5.rotation.z += Math.PI / 2;
        Cylinder6L5.position.set(0, 20, -20);

        // create Link 6
        this.CylinderL6 = new THREE.Mesh(new THREE.CylinderGeometry(12, 12, 50, 100), new THREE.MeshPhongMaterial({color: "#6A736B"}));
        this.Cylinder3L5.add(this.CylinderL6);
        this.CylinderL6.position.set(35, 0, 0);
        this.CylinderL6.rotation.z -= Math.PI / 2;

        Cylinder2L6 = new THREE.Mesh(new THREE.CylinderGeometry(20, 20, 10, 100), new THREE.MeshPhongMaterial({color: "#6A736B"}));
        this.CylinderL6.add(Cylinder2L6);
        Cylinder2L6.position.set(0, 20, 0);
        //this.CylinderL6.rotation.z -= Math.PI / 2;

        BoxL6 = new THREE.Mesh(new THREE.BoxGeometry(50, 5, 50), new THREE.MeshPhongMaterial({color: "#6A736B"}));
        BoxL6.position.set(0, 20, 0);
        this.CylinderL6.add(BoxL6);

        Box2L6 = new THREE.Mesh(new THREE.BoxGeometry(50, 3, 50), new THREE.MeshPhongMaterial({color: "#6A736B"}));
        Box2L6.position.set(24, 23, 0);
        Box2L6.rotation.z += Math.PI / 2;
        BoxL6.add(Box2L6);

        Box3L6 = new THREE.Mesh(new THREE.BoxGeometry(50, 3, 50), new THREE.MeshPhongMaterial({color: "#6A736B"}));
        Box3L6.position.set(-24, 23, 0);
        Box3L6.rotation.z += Math.PI / 2;
        BoxL6.add(Box3L6);

        this.container.addEventListener('mouseover', onContainerMouseOver, false);
        this.container.addEventListener('mouseout', onContainerMouseOut, false);
        //     this.container.addEventListener('keydown', onContainerKeyDown, false);
//        document.addEventListener('mousemove', onContainerMouseMove, false);
//        document.addEventListener('mousedown', onContainerMouseDown, false);
//        document.addEventListener('keydown', onContainerKeyDown, false);
//        document.addEventListener('keyup', onContainerKeyUp, false);
//        document.addEventListener('touchstart', onDocumentTouchStart, false);
//        document.addEventListener('touchmove', onDocumentTouchMove, false);
    }
};

function onContainerMouseOver() {
    PUMA560.controls.enabled = true;
}
function onContainerMouseOut() {
    PUMA560.controls.enabled = false;
}
// Animate the scene
function animate() {
    requestAnimationFrame(animate);
    update();
    render();
}
// Update controls and stats
function update() {
//    AXISCubeScene.controls.update(AXISCubeScene.clock.getDelta());
    PUMA560.controls.update();
    PUMA560.stats.update();
}
// Render the scene
function render() {
    if (PUMA560.renderer) {
	        PUMA560.renderer.render(PUMA560.scene, PUMA560.camera);
    }
}

