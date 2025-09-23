"""
Web Interactive Arm - Browser-based controls
Cross-platform web interface for robotic arm control
"""
import sys
import os
import threading
import time
try:
    import http.server
    import socketserver
    import webbrowser
    WEB_SERVER_AVAILABLE = True
except ImportError:
    WEB_SERVER_AVAILABLE = False


def main():
    """Main function for Web Interactive Arm"""
    print("=" * 60)
    print("WEB INTERACTIVE ARM")
    print("=" * 60)
    print("Browser-based controls for Virtual Robotic Arm")
    print()
    
    if not WEB_SERVER_AVAILABLE:
        print("❌ Web server components not available")
        return
    
    print("🌐 Web Interface Features:")
    print("- Browser-based control interface")
    print("- Real-time joint control sliders")
    print("- Live 3D visualization")
    print("- Cross-platform compatibility")
    print("- Touch-friendly mobile interface")
    print()
    
    print("🚀 Starting web server...")
    
    # Create a simple web interface
    html_content = create_web_interface()
    
    # Start web server
    PORT = 8080
    
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path in ('/', '/index.html'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode())
            elif self.path == '/favicon.ico':
                # Respond with no content to avoid 404 noise
                self.send_response(204)
                self.end_headers()
            else:
                super().do_GET()
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            print(f"🌍 Server started at http://localhost:{PORT}")
            print("🔧 Implementation Status:")
            print("This is a basic placeholder web interface.")
            print("The full implementation would include:")
            print("- WebGL-based 3D rendering")
            print("- WebSocket communication for real-time control")
            print("- Advanced UI with joint controls")
            print("- Mobile-responsive design")
            print("- Integration with PyBullet simulation")
            print()
            print("Opening web browser...")
            
            # Open browser in a separate thread
            def open_browser():
                time.sleep(1)  # Give server time to start
                webbrowser.open(f'http://localhost:{PORT}')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            print(f"Press Ctrl+C to stop the server")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except OSError as e:
        print(f"❌ Error starting server: {e}")
        print("Port 8080 might already be in use")


def create_web_interface():
    """Create basic HTML web interface"""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Virtual Robotic Arm - Web Interface</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 30px;
            backdrop-filter: blur(10px);
        }
        h1 {
            text-align: center;
            color: #ffd700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .control-panel {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .control-group {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);

                <div class="control-group">
                    <h3>🛠️ End Effector</h3>
                    <div class="slider-container">
                        <label for="endEffector">Type</label>
                        <select id="endEffector" class="slider" style="height: 30px;">
                            <option value="bucket" selected>Bucket</option>
                            <option value="gripper">Gripper</option>
                        </select>
                    </div>
                    <div class="slider-container">
                        <label for="gripper">Gripper Open <span class="value-display" id="gripperValue">0%</span></label>
                        <input type="range" min="0" max="100" value="0" class="slider" id="gripper">
                    </div>
                </div>
        }
        .control-group h3 {
            color: #ffd700;
            margin-top: 0;
        }
        .slider-container {
            margin: 15px 0;
        }
        .slider-container label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .slider {
            width: 100%;
            height: 8px;
            border-radius: 5px;
            background: #ddd;
            outline: none;
            opacity: 0.7;
            transition: opacity 0.2s;
        }
        .slider:hover {
            opacity: 1;
        }
        .value-display {
            float: right;
            background: rgba(0,0,0,0.3);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
        }
        .status {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
        }
        .jcb-specs {
            background: rgba(255, 193, 7, 0.1);
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
        }
        .viewer {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            min-height: 420px;
            position: relative;
        }
        #threeContainer {
            width: 100%;
            height: 100%;
            min-height: 420px;
        }
    </style>
    <!-- Three.js module CDN -->
    <script type="module">
      import * as THREE from 'https://unpkg.com/three@0.158.0/build/three.module.js';
      window.THREE = THREE; // expose for inline scripts if needed
    </script>
</head>
<body>
    <div class="container">
        <h1>🚜 Virtual JCB Robotic Arm - Web Interface</h1>
        
        <div class="jcb-specs">
            <h3>🚜 JCB Specifications</h3>
            <p><strong>Max Reach:</strong> 8.0 meters | <strong>Max Dig Depth:</strong> 6.2 meters | <strong>Bucket Capacity:</strong> 1.2 cubic meters</p>
            <p><strong>Operating Weight:</strong> 14,500 kg | <strong>Engine Power:</strong> 100 kW</p>
        </div>
        
        <div class="grid">
            <div class="viewer">
                <div id="threeContainer"></div>
            </div>

            <div class="control-panel">
                <div class="control-group">
                    <h3>🎮 Joint Controls</h3>
                    <div class="slider-container">
                        <label for="base">Base Rotation <span class="value-display" id="baseValue">0°</span></label>
                        <input type="range" min="-180" max="180" value="0" class="slider" id="base">
                    </div>
                    <div class="slider-container">
                        <label for="boom">Boom <span class="value-display" id="boomValue">0°</span></label>
                        <input type="range" min="-90" max="45" value="0" class="slider" id="boom">
                    </div>
                    <div class="slider-container">
                        <label for="stick">Stick <span class="value-display" id="stickValue">0°</span></label>
                        <input type="range" min="-135" max="45" value="0" class="slider" id="stick">
                    </div>
                    <div class="slider-container">
                        <label for="bucket">Bucket <span class="value-display" id="bucketValue">0°</span></label>
                        <input type="range" min="-120" max="60" value="0" class="slider" id="bucket">
                    </div>
                </div>
                
                <div class="control-group">
                    <h3>📹 Camera Controls</h3>
                    <div class="slider-container">
                        <label for="camX">Camera X <span class="value-display" id="camXValue">0</span></label>
                        <input type="range" min="-10" max="10" value="0" class="slider" id="camX">
                    </div>
                    <div class="slider-container">
                        <label for="camY">Camera Y <span class="value-display" id="camYValue">0</span></label>
                        <input type="range" min="-10" max="10" value="0" class="slider" id="camY">
                    </div>
                    <div class="slider-container">
                        <label for="camZ">Camera Z <span class="value-display" id="camZValue">5</span></label>
                        <input type="range" min="1" max="20" value="5" class="slider" id="camZ">
                    </div>
                </div>

                <div class="control-group">
                    <h3>🎞️ Poses</h3>
                    <div class="slider-container">
                        <label for="poseName">Pose Name</label>
                        <input id="poseName" type="text" placeholder="e.g., scoop-start" style="width:100%; padding:6px; border-radius:6px; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.1); color: #fff;">
                    </div>
                    <div class="slider-container" style="display:flex; gap:10px; flex-wrap: wrap;">
                        <button id="savePose" style="flex:1; padding:8px 12px; border-radius:6px; border:none; background:#ffc107; color:#000; font-weight:600; cursor:pointer;">Save</button>
                        <button id="playSequence" style="flex:1; padding:8px 12px; border-radius:6px; border:none; background:#28a745; color:#fff; font-weight:600; cursor:pointer;">Play</button>
                        <button id="stopPlayback" style="flex:1; padding:8px 12px; border-radius:6px; border:none; background:#dc3545; color:#fff; font-weight:600; cursor:pointer;">Stop</button>
                    </div>
                    <div class="slider-container" style="display:flex; gap:10px; align-items:center;">
                        <select id="poseList" style="flex:1; height:34px; border-radius:6px; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.1); color:#fff;"></select>
                        <button id="loadPose" style="padding:8px 12px; border-radius:6px; border:none; background:#17a2b8; color:#fff; font-weight:600; cursor:pointer;">Load</button>
                        <button id="deletePose" style="padding:8px 12px; border-radius:6px; border:none; background:#6c757d; color:#fff; font-weight:600; cursor:pointer;">Delete</button>
                    </div>
                </div>

                <div class="control-group">
                    <h3>🔍 Debug</h3>
                    <label style="display:flex; align-items:center; gap:8px;">
                        <input type="checkbox" id="showGizmos">
                        <span>Show collision gizmos</span>
                    </label>
                </div>
            </div>
        </div>
        
        <div class="status">
            <h3>🔧 Implementation Status</h3>
            <p>This web interface displays a basic WebGL 3D robotic arm using Three.js. It includes a simple 3-joint robotic arm rendered in real-time with basic controls.</p>
            <p>Features:</p>
            <ul style="text-align: left; display: inline-block;">
                <li>WebGL-based 3D rendering of the robotic arm using Three.js</li>
                <li>Simple joint rotation controls</li>
                <li>Responsive canvas resizing</li>
                <li>Placeholder for real-time physics integration</li>
            </ul>
        </div>
        </div>

        <!-- Three.js app: wired controls, no auto-swing, procedural background -->
        <script type="module">
            import * as THREE from 'https://unpkg.com/three@0.158.0/build/three.module.js';

            // DOM
            const container = document.getElementById('threeContainer');
            const baseSlider = document.getElementById('base');
            const boomSlider = document.getElementById('boom');
            const stickSlider = document.getElementById('stick');
            const bucketSlider = document.getElementById('bucket');
            const camXSlider = document.getElementById('camX');
            const camYSlider = document.getElementById('camY');
            const camZSlider = document.getElementById('camZ');
            const baseValue = document.getElementById('baseValue');
            const boomValue = document.getElementById('boomValue');
            const stickValue = document.getElementById('stickValue');
            const bucketValue = document.getElementById('bucketValue');
            const camXValue = document.getElementById('camXValue');
            const camYValue = document.getElementById('camYValue');
            const camZValue = document.getElementById('camZValue');
            const effectorSelect = document.getElementById('endEffector');
            const gripperSlider = document.getElementById('gripper');
            const gripperValue = document.getElementById('gripperValue');

            const deg2rad = (d) => (Number(d) * Math.PI) / 180.0;

            // Scene & renderer
            const scene = new THREE.Scene();
            scene.background = createGradientBackground(0x1b1f2b, 0x3a4460);

            const camera = new THREE.PerspectiveCamera(
                60,
                container.clientWidth / container.clientHeight,
                0.1,
                1000
            );
            camera.position.set(Number(camXSlider.value), Number(camYSlider.value), Number(camZSlider.value));
            camera.lookAt(0, 0, 0);

            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.outputColorSpace = THREE.SRGBColorSpace;
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);

            // Lights
            const dirLight = new THREE.DirectionalLight(0xffffff, 0.9);
            dirLight.position.set(5, 10, 7);
            dirLight.castShadow = true;
            dirLight.shadow.mapSize.set(1024,1024);
            dirLight.shadow.camera.near = 0.1;
            dirLight.shadow.camera.far = 50;
            dirLight.shadow.camera.left = -10;
            dirLight.shadow.camera.right = 10;
            dirLight.shadow.camera.top = 10;
            dirLight.shadow.camera.bottom = -10;
            scene.add(dirLight);
            scene.add(new THREE.AmbientLight(0xffffff, 0.25));
            scene.add(new THREE.HemisphereLight(0x88bbff, 0x223344, 0.4));

            // Ground/grid
                    const ground = new THREE.Mesh(
                new THREE.PlaneGeometry(40, 40),
                new THREE.MeshStandardMaterial({ color: 0x222222, metalness: 0.1, roughness: 0.9 })
            );
            ground.rotation.x = -Math.PI / 2;
            ground.position.y = -0.25;
                    ground.receiveShadow = true;
            scene.add(ground);
            const grid = new THREE.GridHelper(40, 40, 0x888888, 0x444444);
            grid.position.y = -0.249;
            scene.add(grid);

            // Materials & geometry
            const mat = new THREE.MeshStandardMaterial({ color: 0xffa000, metalness: 0.2, roughness: 0.6 });
            const segmentGeom = new THREE.BoxGeometry(1, 0.2, 0.2);

            // Arm hierarchy
            const base = new THREE.Object3D();
            scene.add(base);
            const baseMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.2, 24), mat);
            baseMesh.position.y = -0.05;
            baseMesh.castShadow = true; baseMesh.receiveShadow = true;
            scene.add(baseMesh);

            const joint1 = new THREE.Object3D();
            base.add(joint1);
            const seg1 = new THREE.Mesh(segmentGeom, mat);
            seg1.position.x = 0.5;
            seg1.castShadow = true; seg1.receiveShadow = true;
            joint1.add(seg1);

            const joint2 = new THREE.Object3D();
            joint2.position.x = 1.0;
            joint1.add(joint2);
            const seg2 = new THREE.Mesh(segmentGeom, mat);
            seg2.position.x = 0.5;
            seg2.castShadow = true; seg2.receiveShadow = true;
            joint2.add(seg2);

                    const joint3 = new THREE.Object3D();
            joint3.position.x = 1.0;
            joint2.add(joint3);
                    const seg3 = new THREE.Mesh(segmentGeom, mat);
                    seg3.position.x = 0.5;
                    seg3.castShadow = true; seg3.receiveShadow = true;
                    joint3.add(seg3);

                    // Wrist node for end effector
                    const wrist = new THREE.Object3D();
                    wrist.position.x = 1.0; // at the end of seg3
                    joint3.add(wrist);

                    // Bucket (simple wedge-like box)
                            const bucket = new THREE.Mesh(
                        new THREE.BoxGeometry(0.6, 0.3, 0.5),
                        new THREE.MeshStandardMaterial({ color: 0x3a3a3a, metalness: 0.3, roughness: 0.7 })
                    );
                    bucket.position.x = 0.3;
                    bucket.position.y = -0.1;
                    bucket.rotation.z = -Math.PI / 6;
                            bucket.castShadow = true; bucket.receiveShadow = true;
                    wrist.add(bucket);

                    // Gripper (two opposing fingers)
                    const gripperGroup = new THREE.Group();
                    const fingerGeom = new THREE.BoxGeometry(0.3, 0.06, 0.12);
                    const fingerMat = new THREE.MeshStandardMaterial({ color: 0x2f2f2f, metalness: 0.3, roughness: 0.6 });
                    const leftHinge = new THREE.Object3D();
                    const rightHinge = new THREE.Object3D();
                    leftHinge.position.x = 0.05; leftHinge.position.z = 0.08;
                    rightHinge.position.x = 0.05; rightHinge.position.z = -0.08;
                            const leftFinger = new THREE.Mesh(fingerGeom, fingerMat);
                    leftFinger.position.x = 0.15;
                            const rightFinger = new THREE.Mesh(fingerGeom, fingerMat);
                    rightFinger.position.x = 0.15;
                            leftFinger.castShadow = rightFinger.castShadow = true;
                            leftFinger.receiveShadow = rightFinger.receiveShadow = true;
                    leftHinge.add(leftFinger);
                    rightHinge.add(rightFinger);
                    gripperGroup.add(leftHinge);
                    gripperGroup.add(rightHinge);
                    wrist.add(gripperGroup);

                            // Collision gizmos
                            const gizmoCheckbox = document.getElementById('showGizmos');
                            const helpers = [];
                            function addHelperFor(obj) {
                                const h = new THREE.BoxHelper(obj, 0x00ffff);
                                h.visible = false;
                                scene.add(h);
                                helpers.push({ obj, h });
                            }
                            [seg1, seg2, seg3, bucket, leftFinger, rightFinger].forEach(addHelperFor);
                            function updateHelpers() {
                                helpers.forEach(({obj, h}) => { h.visible = gizmoCheckbox.checked; h.update(); });
                            }

                    // Toggle end effector visibility
                    function applyEndEffectorVisibility() {
                        const useGripper = effectorSelect.value === 'gripper';
                        bucket.visible = !useGripper;
                        gripperGroup.visible = useGripper;
                    }
                    applyEndEffectorVisibility();

            // Wire sliders to values and joints
            function syncLabels() {
                baseValue.textContent = `${baseSlider.value}°`;
                boomValue.textContent = `${boomSlider.value}°`;
                stickValue.textContent = `${stickSlider.value}°`;
                bucketValue.textContent = `${bucketSlider.value}°`;
                camXValue.textContent = `${camXSlider.value}`;
                camYValue.textContent = `${camYSlider.value}`;
                camZValue.textContent = `${camZSlider.value}`;
                        gripperValue.textContent = `${gripperSlider.value}%`;
            }

            function applyArm() {
                base.rotation.y = deg2rad(baseSlider.value);
                joint1.rotation.z = deg2rad(boomSlider.value);
                joint2.rotation.z = deg2rad(stickSlider.value);
                joint3.rotation.z = deg2rad(bucketSlider.value);
            }

            function applyCamera() {
                camera.position.set(Number(camXSlider.value), Number(camYSlider.value), Number(camZSlider.value));
                camera.lookAt(0, 0, 0);
            }

                    function applyEndEffector() {
                        // Gripper open percentage maps to finger rotation around Z
                        const pct = Number(gripperSlider.value) / 100.0; // 0..1
                        const maxAngle = THREE.MathUtils.degToRad(30); // 30° max
                        leftHinge.rotation.z = -pct * maxAngle;
                        rightHinge.rotation.z = pct * maxAngle;
                    }

                    const onInput = () => {
                syncLabels();
                applyArm();
                applyCamera();
                        applyEndEffector();
                        applyEndEffectorVisibility();
                                updateHelpers();
            };

                    [baseSlider, boomSlider, stickSlider, bucketSlider, camXSlider, camYSlider, camZSlider, gripperSlider]
                .forEach(el => el.addEventListener('input', onInput));
                    effectorSelect.addEventListener('change', onInput);

            // Initial sync
            onInput();

            // Render loop without auto-swing
                    // Hydraulic pistons (visual only)
                    const steelMat = new THREE.MeshStandardMaterial({ color: 0xb0b0b0, metalness: 0.8, roughness: 0.2 });
                    function createPistonMesh() {
                        const cyl = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1, 16), steelMat);
                        cyl.castShadow = cyl.receiveShadow = false;
                        return cyl;
                    }
                    // Anchor helpers
                    const baseA = new THREE.Object3D(); base.add(baseA); baseA.position.set(0.0, 0.1, 0);
                    const boomA = new THREE.Object3D(); joint1.add(boomA); boomA.position.set(0.4, 0.12, 0);
                    const boomB = new THREE.Object3D(); joint1.add(boomB); boomB.position.set(0.9, 0.0, 0);
                    const stickA = new THREE.Object3D(); joint2.add(stickA); stickA.position.set(0.1, 0.05, 0);
                    const stickB = new THREE.Object3D(); joint2.add(stickB); stickB.position.set(0.7, -0.02, 0);
                    const wristA = new THREE.Object3D(); joint3.add(wristA); wristA.position.set(0.1, 0.02, 0);

                    const piston1 = createPistonMesh(); scene.add(piston1);
                    const piston2 = createPistonMesh(); scene.add(piston2);
                    const piston3 = createPistonMesh(); scene.add(piston3);

                    function updatePistonBetween(mesh, objA, objB) {
                        const a = new THREE.Vector3(); const b = new THREE.Vector3();
                        objA.getWorldPosition(a); objB.getWorldPosition(b);
                        const mid = new THREE.Vector3().addVectors(a, b).multiplyScalar(0.5);
                        const dir = new THREE.Vector3().subVectors(b, a);
                        const len = dir.length();
                        if (len < 1e-6) return;
                        mesh.position.copy(mid);
                        mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.clone().normalize());
                        mesh.scale.set(1, len, 1); // base geometry height = 1
                    }

                    function animate() {
                requestAnimationFrame(animate);
                        updatePistonBetween(piston1, baseA, boomA);
                        updatePistonBetween(piston2, boomB, stickA);
                        updatePistonBetween(piston3, stickB, wristA);
                                // Playback step
                                stepPlayback();
                                // Helpers update when animating too
                                updateHelpers();
                        renderer.render(scene, camera);
            }
            animate();

            // Resize handling
                    function onResize() {
                const w = container.clientWidth;
                const h = container.clientHeight;
                camera.aspect = w / h;
                camera.updateProjectionMatrix();
                renderer.setSize(w, h);
            }
            window.addEventListener('resize', onResize);
            onResize();

            // Procedural gradient background (stand-in for Gemini background generation)
            function createGradientBackground(topHex, bottomHex) {
                const canvas = document.createElement('canvas');
                canvas.width = 4;
                canvas.height = 256;
                const ctx = canvas.getContext('2d');
                const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
                grad.addColorStop(0, `#${topHex.toString(16).padStart(6, '0')}`);
                grad.addColorStop(1, `#${bottomHex.toString(16).padStart(6, '0')}`);
                ctx.fillStyle = grad;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                const tex = new THREE.CanvasTexture(canvas);
                tex.colorSpace = THREE.SRGBColorSpace;
                        return tex;
            }

                    // ===== Pose save/load/playback =====
                    const poseNameInput = document.getElementById('poseName');
                    const savePoseBtn = document.getElementById('savePose');
                    const loadPoseBtn = document.getElementById('loadPose');
                    const deletePoseBtn = document.getElementById('deletePose');
                    const playBtn = document.getElementById('playSequence');
                    const stopBtn = document.getElementById('stopPlayback');
                    const poseList = document.getElementById('poseList');

                    const LS_KEY = 'vraPoses';
                    function getPoses() {
                        try { return JSON.parse(localStorage.getItem(LS_KEY) || '[]'); } catch { return []; }
                    }
                    function setPoses(poses) { localStorage.setItem(LS_KEY, JSON.stringify(poses)); }
                    function refreshPoseList() {
                        const poses = getPoses();
                        poseList.innerHTML = '';
                        poses.forEach((p, i) => {
                            const opt = document.createElement('option');
                            opt.value = String(i); opt.textContent = p.name || `Pose ${i+1}`;
                            poseList.appendChild(opt);
                        });
                    }
                    function currentPoseFromUI() {
                        return {
                            name: poseNameInput.value.trim() || `Pose ${Date.now()}`,
                            joints: {
                                base: Number(baseSlider.value),
                                boom: Number(boomSlider.value),
                                stick: Number(stickSlider.value),
                                bucket: Number(bucketSlider.value),
                                gripper: Number(gripperSlider.value)
                            },
                            camera: {
                                x: Number(camXSlider.value),
                                y: Number(camYSlider.value),
                                z: Number(camZSlider.value)
                            },
                            effector: effectorSelect.value
                        };
                    }
                    function applyPose(p) {
                        if (!p) return;
                        effectorSelect.value = p.effector || 'bucket';
                        baseSlider.value = String(p.joints.base);
                        boomSlider.value = String(p.joints.boom);
                        stickSlider.value = String(p.joints.stick);
                        bucketSlider.value = String(p.joints.bucket);
                        gripperSlider.value = String(p.joints.gripper ?? 0);
                        camXSlider.value = String(p.camera.x);
                        camYSlider.value = String(p.camera.y);
                        camZSlider.value = String(p.camera.z);
                        onInput();
                    }
                    savePoseBtn.addEventListener('click', () => {
                        const p = currentPoseFromUI();
                        const poses = getPoses();
                        const idx = poses.findIndex(x => x.name === p.name);
                        if (idx >= 0) poses[idx] = p; else poses.push(p);
                        setPoses(poses);
                        refreshPoseList();
                    });
                    loadPoseBtn.addEventListener('click', () => {
                        const poses = getPoses();
                        const idx = Number(poseList.value);
                        applyPose(poses[idx]);
                        poseNameInput.value = poses[idx]?.name || '';
                    });
                    deletePoseBtn.addEventListener('click', () => {
                        const poses = getPoses();
                        const idx = Number(poseList.value);
                        if (idx >= 0 && idx < poses.length) {
                            poses.splice(idx, 1);
                            setPoses(poses);
                            refreshPoseList();
                        }
                    });

                    // Playback sequencing
                    let playback = { playing: false, i: 0, start: 0, dur: 1500, a: null, b: null };
                    function lerp(a, b, t) { return a + (b - a) * t; }
                    function startPlayback() {
                        const poses = getPoses();
                        if (poses.length < 2) return;
                        playback.playing = true; playback.i = 0; playback.start = performance.now();
                        playback.a = poses[0]; playback.b = poses[1];
                    }
                    function stopPlayback() { playback.playing = false; }
                    function stepPlayback() {
                        if (!playback.playing) return;
                        const poses = getPoses();
                        if (poses.length < 2) { stopPlayback(); return; }
                        const now = performance.now();
                        const t = Math.min(1, (now - playback.start) / playback.dur);
                        const a = playback.a, b = playback.b;
                        // Interpolate joints & camera; effector switches at end of segment
                        baseSlider.value = String(lerp(a.joints.base, b.joints.base, t));
                        boomSlider.value = String(lerp(a.joints.boom, b.joints.boom, t));
                        stickSlider.value = String(lerp(a.joints.stick, b.joints.stick, t));
                        bucketSlider.value = String(lerp(a.joints.bucket, b.joints.bucket, t));
                        gripperSlider.value = String(lerp(a.joints.gripper ?? 0, b.joints.gripper ?? 0, t));
                        camXSlider.value = String(lerp(a.camera.x, b.camera.x, t));
                        camYSlider.value = String(lerp(a.camera.y, b.camera.y, t));
                        camZSlider.value = String(lerp(a.camera.z, b.camera.z, t));
                        if (t >= 1) {
                            effectorSelect.value = b.effector || effectorSelect.value;
                            playback.i = (playback.i + 1) % poses.length;
                            const next = (playback.i + 1) % poses.length;
                            playback.a = poses[playback.i]; playback.b = poses[next];
                            playback.start = now;
                        }
                        onInput();
                    }
                    playBtn.addEventListener('click', startPlayback);
                    stopBtn.addEventListener('click', stopPlayback);
                    refreshPoseList();
        </script>
</body>
</html>
    """
    return html


if __name__ == "__main__":
    main()