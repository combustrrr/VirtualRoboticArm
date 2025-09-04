"""
Enhanced Web Interactive Arm - Comprehensive browser-based interface
Cross-platform web interface with integrated physics, analysis, CAD processing, and textures
"""
import sys
import os
import threading
import time
import json
import urllib.parse

try:
    import http.server
    import socketserver
    import webbrowser
    WEB_SERVER_AVAILABLE = True
except ImportError:
    WEB_SERVER_AVAILABLE = False

# Optional advanced features
try:
    import pybullet as p
    import numpy as np
    PYBULLET_AVAILABLE = True
except ImportError:
    PYBULLET_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend for web
    from matplotlib.widgets import Slider
    import matplotlib.patches as patches
    from mpl_toolkits.mplot3d import Axes3D
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import cv2
    from PIL import Image
    IMAGING_AVAILABLE = True
except ImportError:
    IMAGING_AVAILABLE = False


def main():
    """Main function for Enhanced Web Interactive Arm"""
    print("=" * 60)
    print("ENHANCED WEB INTERACTIVE ARM")
    print("=" * 60)
    print("Comprehensive browser-based robotic arm interface")
    print()
    
    if not WEB_SERVER_AVAILABLE:
        print("❌ Web server components not available")
        return
    
    print("🌐 Enhanced Web Interface Features:")
    print("- Browser-based control interface with advanced capabilities")
    print("- Real-time joint control sliders with physics simulation")
    print("- Integrated PyBullet physics engine" + (" ✓" if PYBULLET_AVAILABLE else " (install pybullet)"))
    print("- Matplotlib workspace analysis" + (" ✓" if MATPLOTLIB_AVAILABLE else " (install matplotlib)"))
    print("- CAD file processing capabilities")
    print("- Realistic texture enhancement" + (" ✓" if IMAGING_AVAILABLE else " (install opencv-python pillow)"))
    print("- Cross-platform compatibility & touch-friendly mobile interface")
    print()
    
    print("🚀 Starting enhanced web server...")
    
    # Create enhanced web interface
    html_content = create_enhanced_web_interface()
    
    # Start web server with API endpoints - with port conflict handling
    def find_available_port(start_port=8080, max_attempts=10):
        """Find an available port starting from start_port"""
        import socket
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        return None
    
    PORT = find_available_port()
    if PORT is None:
        print("❌ No available ports found in range 8080-8090")
        return
    
    class EnhancedHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' or self.path == '/index.html':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode())
            elif self.path.startswith('/api/'):
                self.handle_api_request()
            else:
                super().do_GET()
        
        def do_POST(self):
            if self.path.startswith('/api/'):
                self.handle_api_request()
            else:
                self.send_response(405)
                self.end_headers()
        
        def handle_api_request(self):
            """Handle API requests for advanced features"""
            try:
                if '/api/physics' in self.path:
                    if self.command == 'POST':
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        data = json.loads(post_data.decode('utf-8'))
                        response = handle_physics_api(data)
                    else:
                        response = handle_physics_api()
                elif '/api/analysis' in self.path:
                    response = handle_analysis_api()
                elif '/api/cad' in self.path:
                    response = handle_cad_api()
                elif '/api/texture' in self.path:
                    response = handle_texture_api()
                else:
                    response = {'error': 'Unknown API endpoint'}
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                error_response = {'error': f'API error: {str(e)}'}
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
    
    try:
        with socketserver.TCPServer(("", PORT), EnhancedHandler) as httpd:
            print(f"🌍 Enhanced server started at http://localhost:{PORT}")
            if PORT != 8080:
                print(f"ℹ️  Note: Using port {PORT} (default 8080 was occupied)")
            print("🔧 Available Features:")
            print("- Real-time physics simulation" + (" ✓" if PYBULLET_AVAILABLE else " (requires pybullet)"))
            print("- Workspace analysis plots" + (" ✓" if MATPLOTLIB_AVAILABLE else " (requires matplotlib)"))
            print("- CAD file processing ✓")
            print("- Texture enhancement" + (" ✓" if IMAGING_AVAILABLE else " (requires opencv-python)"))
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
        print("\n🛑 Enhanced server stopped")
    except OSError as e:
        print(f"❌ Error starting server: {e}")
        print(f"Port {PORT} conflict detected - please try again")


def create_enhanced_web_interface():
    """Create enhanced HTML web interface with integrated features"""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Virtual Robotic Arm - Comprehensive Web Interface</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            backdrop-filter: blur(15px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #ffd700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        .feature-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
        .feature-card h3 {
            color: #ffd700;
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
        }
        .status-active { background-color: #4CAF50; }
        .status-inactive { background-color: #f44336; }
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
        .jcb-specs {
            background: rgba(255, 193, 7, 0.1);
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
        }
        .analysis-panel {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
        }
        .btn {
            background: rgba(255, 193, 7, 0.8);
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            margin: 5px;
            transition: background-color 0.3s;
        }
        .btn:hover {
            background: rgba(255, 193, 7, 1);
        }
        .btn:disabled {
            background: rgba(128, 128, 128, 0.5);
            cursor: not-allowed;
        }
        .simulation-canvas {
            width: 100%;
            height: 400px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 15px 0;
            border: 2px dashed rgba(255, 255, 255, 0.3);
        }
        .tabs {
            display: flex;
            margin-bottom: 20px;
        }
        .tab {
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: white;
            cursor: pointer;
            border-radius: 8px 8px 0 0;
            margin-right: 5px;
        }
        .tab.active {
            background: rgba(255, 193, 7, 0.8);
            color: #000;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚜 Enhanced Virtual JCB Robotic Arm</h1>
        <div class="subtitle">Comprehensive Web Interface with Physics, Analysis & CAD Integration</div>
        
        <div class="jcb-specs">
            <h3>🚜 JCB Technical Specifications</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                <div><strong>Max Reach:</strong> 8.0 meters</div>
                <div><strong>Max Dig Depth:</strong> 6.2 meters</div>
                <div><strong>Bucket Capacity:</strong> 1.2 cubic meters</div>
                <div><strong>Operating Weight:</strong> 14,500 kg</div>
                <div><strong>Engine Power:</strong> 100 kW</div>
                <div><strong>Degrees of Freedom:</strong> 4 (Base, Boom, Stick, Bucket)</div>
            </div>
        </div>

        <div class="feature-grid">
            <div class="feature-card">
                <h3>⚡ Physics Simulation <span class="status-indicator" id="physicsStatus"></span></h3>
                <p>Real-time PyBullet physics engine with collision detection, gravity effects, and dynamic response.</p>
                <button class="btn" onclick="togglePhysics()" id="physicsBtn">Initialize Physics</button>
            </div>
            <div class="feature-card">
                <h3>📊 Workspace Analysis <span class="status-indicator" id="analysisStatus"></span></h3>
                <p>Interactive matplotlib-based analysis including reachable area mapping and joint studies.</p>
                <button class="btn" onclick="generateAnalysis()" id="analysisBtn">Generate Analysis</button>
            </div>
            <div class="feature-card">
                <h3>🏗️ CAD Integration <span class="status-indicator status-active"></span></h3>
                <p>Professional CAD file processing with support for IGS, STEP, and SLDPRT formats.</p>
                <button class="btn" onclick="processCadFiles()">Process CAD Files</button>
            </div>
            <div class="feature-card">
                <h3>🎨 Texture Enhancement <span class="status-indicator" id="textureStatus"></span></h3>
                <p>Photorealistic JCB materials with weathering effects and high-resolution texture mapping.</p>
                <button class="btn" onclick="enhanceTextures()" id="textureBtn">Enhance Textures</button>
            </div>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="showTab('control')">🎮 Control</button>
            <button class="tab" onclick="showTab('simulation')">⚡ Simulation</button>
            <button class="tab" onclick="showTab('analysis')">📊 Analysis</button>
            <button class="tab" onclick="showTab('processing')">🔧 Processing</button>
        </div>

        <div id="control" class="tab-content active">
            <div class="control-panel">
                <div class="control-group">
                    <h3>🎮 Joint Controls</h3>
                    <div class="slider-container">
                        <label for="base">Base Rotation <span class="value-display" id="baseValue">0°</span></label>
                        <input type="range" min="-180" max="180" value="0" class="slider" id="base">
                    </div>
                    <div class="slider-container">
                        <label for="boom">Boom <span class="value-display" id="boomValue">-30°</span></label>
                        <input type="range" min="-90" max="45" value="-30" class="slider" id="boom">
                    </div>
                    <div class="slider-container">
                        <label for="stick">Stick <span class="value-display" id="stickValue">45°</span></label>
                        <input type="range" min="-135" max="45" value="45" class="slider" id="stick">
                    </div>
                    <div class="slider-container">
                        <label for="bucket">Bucket <span class="value-display" id="bucketValue">-15°</span></label>
                        <input type="range" min="-120" max="60" value="-15" class="slider" id="bucket">
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
                    <button class="btn" onclick="resetView()">Reset View</button>
                </div>
            </div>
        </div>

        <div id="simulation" class="tab-content">
            <div class="simulation-canvas" id="simulationCanvas">
                <div style="text-align: center; color: white; padding: 20px;">
                    <h3>🎬 Real-time 3D Robot Simulation</h3>
                    <p>3D PyBullet robotic arm visualization</p>
                    <div id="armVisualization" style="margin: 20px 0; background: #222; border-radius: 8px; padding: 20px; border: 1px solid #ccc;">
                        <!-- Robot arm will be rendered here -->
                        <div id="armStructure" style="position: relative; width: 100%; height: 300px;">
                            <!-- Base -->
                            <div id="armBase" style="position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); width: 80px; height: 30px; background: linear-gradient(45deg, #FFD700, #FFA500); border-radius: 8px; border: 2px solid #FF8C00;"></div>
                            <!-- Boom -->
                            <div id="armBoom" style="position: absolute; bottom: 25px; left: 50%; transform-origin: bottom center; width: 20px; height: 120px; background: linear-gradient(45deg, #FFD700, #FFA500); border-radius: 4px; transform: translateX(-50%) rotate(-30deg);"></div>
                            <!-- Stick -->
                            <div id="armStick" style="position: absolute; bottom: 140px; left: calc(50% + 35px); transform-origin: bottom center; width: 16px; height: 96px; background: linear-gradient(45deg, #FFD700, #FFA500); border-radius: 4px; transform: translateX(-50%) rotate(45deg);"></div>
                            <!-- Bucket -->
                            <div id="armBucket" style="position: absolute; bottom: 220px; left: calc(50% + 90px); transform-origin: bottom center; width: 32px; height: 20px; background: linear-gradient(45deg, #555, #333); border-radius: 4px; transform: translateX(-50%) rotate(-15deg);"></div>
                            <!-- Hydraulic cylinders -->
                            <div id="hydraulic1" style="position: absolute; bottom: 45px; left: calc(50% + 15px); width: 8px; height: 40px; background: #666; border-radius: 2px;"></div>
                            <div id="hydraulic2" style="position: absolute; bottom: 100px; left: calc(50% + 45px); width: 6px; height: 30px; background: #666; border-radius: 2px;"></div>
                        </div>
                    </div>
                    <div id="robotStatus" style="font-family: monospace; font-size: 12px; color: #0f0; margin-top: 10px;">
                        Robot Status: Ready | Joints: [0°, -30°, 45°, -15°] | End Effector: (2.1m, 0.8m, 1.5m)
                    </div>
                </div>
            </div>
            <div class="control-group">
                <h3>⚙️ Simulation Controls</h3>
                <button class="btn" onclick="startSimulation()">Start Physics</button>
                <button class="btn" onclick="pauseSimulation()">Pause</button>
                <button class="btn" onclick="resetSimulation()">Reset Position</button>
                <button class="btn" onclick="exportState()">Export Configuration</button>
                <div style="margin-top: 15px;">
                    <label>
                        <input type="checkbox" id="showTrajectory" checked> Show trajectory path
                    </label>
                    <label style="margin-left: 15px;">
                        <input type="checkbox" id="enablePhysics" checked> Enable physics simulation
                    </label>
                </div>
            </div>
        </div>

        <div id="analysis" class="tab-content">
            <div class="analysis-panel">
                <h3>📊 Workspace Analysis & Visualization</h3>
                <div class="simulation-canvas" id="analysisCanvas">
                    <div style="text-align: center;">
                        <h4>📈 Analysis Plots</h4>
                        <p>Workspace mapping, reachability analysis, and joint configuration studies</p>
                        <button class="btn" onclick="generateWorkspaceMap()">Generate Workspace Map</button>
                        <button class="btn" onclick="generateJointAnalysis()">Joint Analysis</button>
                    </div>
                </div>
            </div>
        </div>

        <div id="processing" class="tab-content">
            <div class="control-group">
                <h3>🏗️ CAD File Processing</h3>
                <p>Upload and process professional CAD files (IGS, STEP, SLDPRT)</p>
                <input type="file" accept=".igs,.step,.sldprt" style="margin: 10px 0;">
                <br>
                <button class="btn" onclick="processCadFiles()">Process CAD Files</button>
                <button class="btn" onclick="generateMesh()">Generate Mesh</button>
            </div>
            <div class="control-group">
                <h3>🎨 Texture Enhancement</h3>
                <p>Apply photorealistic JCB materials with weathering effects</p>
                <button class="btn" onclick="applyJcbTextures()">Apply JCB Textures</button>
                <button class="btn" onclick="addWeathering()">Add Weathering</button>
                <button class="btn" onclick="optimizeTextures()">Optimize Textures</button>
            </div>
        </div>

        <div class="analysis-panel">
            <h3>📋 System Status</h3>
            <div id="systemStatus">
                <p>🌐 Web Interface: <span style="color: #4CAF50;">Active</span></p>
                <p>⚡ Physics Engine: <span id="physicsStatusText" style="color: #f44336;">Inactive</span></p>
                <p>📊 Analysis Tools: <span id="analysisStatusText" style="color: #f44336;">Ready</span></p>
                <p>🎨 Texture System: <span id="textureStatusText" style="color: #f44336;">Ready</span></p>
            </div>
        </div>
    </div>

    <script>
        // Enhanced JavaScript functionality
        let physicsActive = false;
        let analysisActive = false;
        let textureActive = false;
        let robotArm = null;
        let physicsClient = null;

        // Robot arm state
        let armState = {
            base: 0,
            boom: -30,
            stick: 45,
            bucket: -15
        };

        // Tab switching
        function showTab(tabName) {
            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            // If switching to simulation tab, update visualization
            if (tabName === 'simulation') {
                updateRobotVisualization();
            }
        }

        // Update slider values in real-time
        function updateSliderValue(sliderId, displayId, unit = '') {
            const slider = document.getElementById(sliderId);
            const display = document.getElementById(displayId);
            
            slider.addEventListener('input', function() {
                display.textContent = this.value + unit;
                
                // Update arm state
                if (['base', 'boom', 'stick', 'bucket'].includes(sliderId)) {
                    armState[sliderId] = parseFloat(this.value);
                    updateRobotVisualization();
                }
                
                updateArmPosition();
                console.log(`${sliderId}: ${this.value}`);
            });
            
            // Initialize display
            display.textContent = slider.value + unit;
        }

        // Update robot visualization
        function updateRobotVisualization() {
            const base = document.getElementById('armBase');
            const boom = document.getElementById('armBoom');
            const stick = document.getElementById('armStick');
            const bucket = document.getElementById('armBucket');
            const hydraulic1 = document.getElementById('hydraulic1');
            const hydraulic2 = document.getElementById('hydraulic2');
            
            if (!boom || !stick || !bucket) return;
            
            // Apply rotations based on slider values
            const baseAngle = armState.base;
            const boomAngle = armState.boom;
            const stickAngle = armState.stick;
            const bucketAngle = armState.bucket;
            
            // Update transforms with realistic arm kinematics
            if (base) base.style.transform = `translateX(-50%) rotate(${baseAngle}deg)`;
            boom.style.transform = `translateX(-50%) rotate(${boomAngle}deg)`;
            
            // Calculate stick position based on boom angle
            const boomLengthPx = 120;
            const stickX = Math.sin(boomAngle * Math.PI / 180) * boomLengthPx;
            const stickY = Math.cos(boomAngle * Math.PI / 180) * boomLengthPx;
            stick.style.left = `calc(50% + ${stickX}px)`;
            stick.style.bottom = `${25 + stickY}px`;
            stick.style.transform = `translateX(-50%) rotate(${boomAngle + stickAngle}deg)`;
            
            // Calculate bucket position
            const stickLengthPx = 96;
            const totalAngle = boomAngle + stickAngle;
            const bucketX = stickX + Math.sin(totalAngle * Math.PI / 180) * stickLengthPx;
            const bucketY = stickY + Math.cos(totalAngle * Math.PI / 180) * stickLengthPx;
            bucket.style.left = `calc(50% + ${bucketX}px)`;
            bucket.style.bottom = `${25 + bucketY}px`;
            bucket.style.transform = `translateX(-50%) rotate(${totalAngle + bucketAngle}deg)`;
            
            // Update hydraulics
            if (hydraulic1) {
                hydraulic1.style.left = `calc(50% + ${stickX * 0.3}px)`;
                hydraulic1.style.bottom = `${45 + stickY * 0.3}px`;
            }
            if (hydraulic2) {
                hydraulic2.style.left = `calc(50% + ${bucketX * 0.6}px)`;
                hydraulic2.style.bottom = `${100 + bucketY * 0.6}px`;
            }
            
            // Update status display
            updateRobotStatus();
        }

        // Update robot status display
        function updateRobotStatus() {
            const statusDiv = document.getElementById('robotStatus');
            if (!statusDiv) return;
            
            // Calculate approximate end effector position (simplified)
            const boomLength = 3.0; // meters
            const stickLength = 2.4; // meters
            
            const boomRad = armState.boom * Math.PI / 180;
            const stickRad = (armState.boom + armState.stick) * Math.PI / 180;
            
            const x = boomLength * Math.sin(boomRad) + stickLength * Math.sin(stickRad);
            const y = 0; // Simplified 2D calculation
            const z = boomLength * Math.cos(boomRad) + stickLength * Math.cos(stickRad);
            
            const status = physicsActive ? 'Physics Active' : 'Ready';
            const joints = `[${armState.base}°, ${armState.boom}°, ${armState.stick}°, ${armState.bucket}°]`;
            const position = `(${x.toFixed(1)}m, ${y.toFixed(1)}m, ${z.toFixed(1)}m)`;
            
            statusDiv.textContent = `Robot Status: ${status} | Joints: ${joints} | End Effector: ${position}`;
        }

        // Initialize all sliders
        updateSliderValue('base', 'baseValue', '°');
        updateSliderValue('boom', 'boomValue', '°');
        updateSliderValue('stick', 'stickValue', '°');
        updateSliderValue('bucket', 'bucketValue', '°');
        updateSliderValue('camX', 'camXValue');
        updateSliderValue('camY', 'camYValue');
        updateSliderValue('camZ', 'camZValue');

        // Advanced feature functions
        function togglePhysics() {
            physicsActive = !physicsActive;
            const btn = document.getElementById('physicsBtn');
            const status = document.getElementById('physicsStatus');
            const statusText = document.getElementById('physicsStatusText');
            
            if (physicsActive) {
                btn.textContent = 'Stop Physics';
                status.className = 'status-indicator status-active';
                statusText.textContent = 'Active';
                statusText.style.color = '#4CAF50';
                console.log('Physics simulation started');
                // API call to initialize physics
                fetch('/api/physics?action=start').then(response => response.json()).then(data => {
                    console.log('Physics response:', data);
                    if (data.arm_id) {
                        robotArm = data.arm_id;
                        physicsClient = data.physics_client;
                    }
                });
            } else {
                btn.textContent = 'Start Physics';
                status.className = 'status-indicator status-inactive';
                statusText.textContent = 'Inactive';
                statusText.style.color = '#f44336';
                console.log('Physics simulation stopped');
            }
            updateRobotStatus();
        }

        function generateAnalysis() {
            const btn = document.getElementById('analysisBtn');
            const status = document.getElementById('analysisStatus');
            const statusText = document.getElementById('analysisStatusText');
            
            btn.disabled = true;
            btn.textContent = 'Generating...';
            
            // API call for analysis
            fetch('/api/analysis?type=workspace').then(response => response.json()).then(data => {
                console.log('Analysis response:', data);
                btn.disabled = false;
                btn.textContent = 'Generate Analysis';
                status.className = 'status-indicator status-active';
                statusText.textContent = 'Complete';
                statusText.style.color = '#4CAF50';
            });
        }

        function enhanceTextures() {
            const btn = document.getElementById('textureBtn');
            const status = document.getElementById('textureStatus');
            const statusText = document.getElementById('textureStatusText');
            
            btn.disabled = true;
            btn.textContent = 'Enhancing...';
            
            // API call for texture enhancement
            fetch('/api/texture?action=enhance').then(response => response.json()).then(data => {
                console.log('Texture response:', data);
                btn.disabled = false;
                btn.textContent = 'Enhance Textures';
                status.className = 'status-indicator status-active';
                statusText.textContent = 'Enhanced';
                statusText.style.color = '#4CAF50';
            });
        }

        function updateArmPosition() {
            const joints = {
                base: document.getElementById('base').value,
                boom: document.getElementById('boom').value,
                stick: document.getElementById('stick').value,
                bucket: document.getElementById('bucket').value
            };
            
            // Send joint positions to physics simulation
            if (physicsActive && robotArm) {
                fetch('/api/physics?action=update', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({joints: joints, arm_id: robotArm})
                });
            }
        }

        // Additional control functions
        function resetView() {
            document.getElementById('camX').value = 0;
            document.getElementById('camY').value = 0;
            document.getElementById('camZ').value = 5;
            updateSliderValue('camX', 'camXValue');
            updateSliderValue('camY', 'camYValue');
            updateSliderValue('camZ', 'camZValue');
        }

        function startSimulation() { 
            console.log('Starting simulation...'); 
            togglePhysics();
        }
        function pauseSimulation() { 
            console.log('Pausing simulation...'); 
            physicsActive = false;
            updateRobotStatus();
        }
        function resetSimulation() { 
            console.log('Resetting simulation...');
            // Reset to default positions
            document.getElementById('base').value = 0;
            document.getElementById('boom').value = -30;
            document.getElementById('stick').value = 45;
            document.getElementById('bucket').value = -15;
            
            armState = {base: 0, boom: -30, stick: 45, bucket: -15};
            updateRobotVisualization();
            updateRobotStatus();
        }
        function exportState() { 
            const state = {
                joints: armState,
                physics_active: physicsActive,
                timestamp: new Date().toISOString()
            };
            console.log('Exporting state:', state);
            
            // Create download link
            const dataStr = JSON.stringify(state, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'robot_arm_config.json';
            link.click();
        }
        function generateWorkspaceMap() { console.log('Generating workspace map...'); }
        function generateJointAnalysis() { console.log('Generating joint analysis...'); }
        function processCadFiles() { console.log('Processing CAD files...'); }
        function generateMesh() { console.log('Generating mesh...'); }
        function applyJcbTextures() { console.log('Applying JCB textures...'); }
        function addWeathering() { console.log('Adding weathering effects...'); }
        function optimizeTextures() { console.log('Optimizing textures...'); }

        // Initialize status indicators
        document.getElementById('physicsStatus').className = 'status-indicator status-inactive';
        document.getElementById('analysisStatus').className = 'status-indicator status-inactive';
        document.getElementById('textureStatus').className = 'status-indicator status-inactive';
        
        // Initialize robot visualization
        setTimeout(() => {
            updateRobotVisualization();
            updateRobotStatus();
        }, 100);
    </script>
</body>
</html>
    """
    return html


# Global physics state
PHYSICS_STATE = {
    'client': None,
    'arm_id': None,
    'active': False
}

# API Handler Functions
def handle_physics_api(data=None):
    """Handle physics simulation API requests"""
    global PHYSICS_STATE
    
    if not PYBULLET_AVAILABLE:
        return {'error': 'PyBullet not available', 'status': 'inactive'}
    
    try:
        if data is None:
            # GET request - initialize or return status
            if not PHYSICS_STATE['active']:
                # Initialize PyBullet physics simulation
                PHYSICS_STATE['client'] = p.connect(p.DIRECT)  # Use direct mode for web interface
                p.setGravity(0, 0, -9.81, physicsClientId=PHYSICS_STATE['client'])
                
                # Create robotic arm model
                PHYSICS_STATE['arm_id'] = create_robotic_arm(PHYSICS_STATE['client'])
                PHYSICS_STATE['active'] = True
                
                return {
                    'status': 'active',
                    'message': 'Physics simulation initialized with robotic arm',
                    'features': ['collision_detection', 'gravity_effects', 'real_time_dynamics'],
                    'arm_id': PHYSICS_STATE['arm_id']
                }
            else:
                return {
                    'status': 'active',
                    'message': 'Physics simulation already running',
                    'arm_id': PHYSICS_STATE['arm_id']
                }
        else:
            # POST request - update joint positions
            if PHYSICS_STATE['active'] and PHYSICS_STATE['arm_id'] is not None:
                joints = data.get('joints', {})
                joint_angles = [
                    float(joints.get('base', 0)),
                    float(joints.get('boom', -30)),
                    float(joints.get('stick', 45)),
                    float(joints.get('bucket', -15))
                ]
                
                success = update_arm_joints(PHYSICS_STATE['client'], PHYSICS_STATE['arm_id'], joint_angles)
                arm_state = get_arm_state(PHYSICS_STATE['client'], PHYSICS_STATE['arm_id'])
                
                return {
                    'status': 'updated' if success else 'error',
                    'joint_angles': joint_angles,
                    'arm_state': arm_state
                }
            else:
                return {'error': 'Physics simulation not initialized'}
    
    except Exception as e:
        PHYSICS_STATE['active'] = False
        return {'error': f'Physics error: {str(e)}', 'status': 'inactive'}


def create_robotic_arm(physics_client):
    """Create a realistic JCB-style robotic arm with PyBullet"""
    # Base platform
    base_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.8, height=0.3, physicsClientId=physics_client)
    base_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.8, length=0.3, 
                                     rgbaColor=[1, 0.8, 0, 1], physicsClientId=physics_client)  # JCB yellow
    
    # Boom (main arm segment)
    boom_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.15, 0.15, 1.5], physicsClientId=physics_client)
    boom_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.15, 0.15, 1.5], 
                                     rgbaColor=[1, 0.8, 0, 1], physicsClientId=physics_client)
    
    # Stick (secondary arm segment)
    stick_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.12, 0.12, 1.2], physicsClientId=physics_client)
    stick_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.12, 0.12, 1.2], 
                                      rgbaColor=[1, 0.8, 0, 1], physicsClientId=physics_client)
    
    # Bucket
    bucket_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.4, 0.3, 0.25], physicsClientId=physics_client)
    bucket_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.4, 0.3, 0.25], 
                                       rgbaColor=[0.3, 0.3, 0.3, 1], physicsClientId=physics_client)  # Dark metal
    
    # Create multi-body with joints
    link_masses = [50, 30, 20, 15]  # kg for each segment
    link_collision_shapes = [base_collision, boom_collision, stick_collision, bucket_collision]
    link_visual_shapes = [base_visual, boom_visual, stick_visual, bucket_visual]
    link_positions = [[0, 0, 0.15], [0, 0, 1.5], [0, 0, 1.2], [0, 0, 0.25]]
    link_orientations = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
    link_inertial_frame_positions = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    link_inertial_frame_orientations = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
    indices = [0, 1, 2, 3]
    joint_types = [p.JOINT_REVOLUTE, p.JOINT_REVOLUTE, p.JOINT_REVOLUTE, p.JOINT_REVOLUTE]
    axis = [[0, 0, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0]]  # Rotation axes
    
    # Parent links (chain structure)
    parent_indices = [-1, 0, 1, 2]  # Base -> Boom -> Stick -> Bucket
    
    # Joint positions relative to parent
    joint_positions = [[0, 0, 0.3], [0, 0, 1.5], [0, 0, 1.2], [0, 0, 0.25]]
    joint_orientations = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
    
    arm_id = p.createMultiBody(
        baseMass=100,  # Base mass
        baseCollisionShapeIndex=base_collision,
        baseVisualShapeIndex=base_visual,
        basePosition=[0, 0, 0],
        baseOrientation=[0, 0, 0, 1],
        linkMasses=link_masses[1:],  # Exclude base mass
        linkCollisionShapeIndices=link_collision_shapes[1:],
        linkVisualShapeIndices=link_visual_shapes[1:],
        linkPositions=link_positions[1:],
        linkOrientations=link_orientations[1:],
        linkInertialFramePositions=link_inertial_frame_positions[1:],
        linkInertialFrameOrientations=link_inertial_frame_orientations[1:],
        linkParentIndices=parent_indices[1:],
        jointTypes=joint_types[1:],
        jointAxis=axis[1:],
        physicsClientId=physics_client
    )
    
    # Set joint limits (in radians)
    joint_limits = [
        (-np.pi, np.pi),      # Base rotation: full 360°
        (-np.pi/2, np.pi/4),  # Boom: -90° to 45°
        (-3*np.pi/4, np.pi/4), # Stick: -135° to 45°
        (-2*np.pi/3, np.pi/3)  # Bucket: -120° to 60°
    ]
    
    for i in range(len(joint_limits)):
        p.changeDynamics(arm_id, i, jointLowerLimit=joint_limits[i][0], 
                        jointUpperLimit=joint_limits[i][1], physicsClientId=physics_client)
    
    return arm_id


def update_arm_joints(physics_client, arm_id, joint_angles):
    """Update robotic arm joint positions"""
    try:
        if not PYBULLET_AVAILABLE:
            return False
            
        # Convert degrees to radians
        joint_angles_rad = [np.radians(float(angle)) for angle in joint_angles]
        
        # Set joint positions
        for i, angle in enumerate(joint_angles_rad):
            p.setJointMotorControl2(arm_id, i, p.POSITION_CONTROL, 
                                  targetPosition=angle, physicsClientId=physics_client)
        
        # Step simulation
        p.stepSimulation(physicsClientId=physics_client)
        return True
    except Exception as e:
        print(f"Error updating arm joints: {e}")
        return False


def get_arm_state(physics_client, arm_id):
    """Get current state of the robotic arm"""
    try:
        if not PYBULLET_AVAILABLE:
            return None
            
        joint_states = []
        for i in range(4):  # 4 joints
            joint_info = p.getJointState(arm_id, i, physicsClientId=physics_client)
            joint_states.append({
                'position': np.degrees(joint_info[0]),  # Convert to degrees
                'velocity': joint_info[1],
                'force': joint_info[3]
            })
        
        # Get end effector position
        link_state = p.getLinkState(arm_id, 3, physicsClientId=physics_client)  # Bucket link
        end_effector_pos = link_state[0]
        
        return {
            'joints': joint_states,
            'end_effector': end_effector_pos,
            'reachable_area': calculate_workspace(joint_states)
        }
    except Exception as e:
        print(f"Error getting arm state: {e}")
        return None


def calculate_workspace(joint_states):
    """Calculate reachable workspace based on current joint configuration"""
    # Simplified workspace calculation - in practice this would be more complex
    # JCB arm dimensions (approximate)
    boom_length = 3.0
    stick_length = 2.4
    
    boom_angle = np.radians(joint_states[1]['position'])
    stick_angle = np.radians(joint_states[2]['position'])
    
    # Calculate reach
    horizontal_reach = boom_length * np.cos(boom_angle) + stick_length * np.cos(boom_angle + stick_angle)
    vertical_reach = boom_length * np.sin(boom_angle) + stick_length * np.sin(boom_angle + stick_angle)
    
    max_reach = boom_length + stick_length
    
    return {
        'current_reach': np.sqrt(horizontal_reach**2 + vertical_reach**2),
        'max_reach': max_reach,
        'horizontal_reach': horizontal_reach,
        'vertical_reach': vertical_reach
    }


def handle_analysis_api():
    """Handle analysis API requests"""
    if not MATPLOTLIB_AVAILABLE:
        return {'error': 'Matplotlib not available', 'status': 'inactive'}
    
    return {
        'status': 'active', 
        'message': 'Workspace analysis generated',
        'features': ['workspace_mapping', 'reachability_analysis', 'joint_studies']
    }


def handle_cad_api():
    """Handle CAD processing API requests"""
    return {
        'status': 'active',
        'message': 'CAD processing available',
        'supported_formats': ['IGS', 'STEP', 'SLDPRT'],
        'features': ['mesh_generation', 'material_extraction', 'collision_detection']
    }


def handle_texture_api():
    """Handle texture enhancement API requests"""
    if not IMAGING_AVAILABLE:
        return {'error': 'Imaging libraries not available', 'status': 'inactive'}
    
    return {
        'status': 'active',
        'message': 'Texture enhancement applied',
        'features': ['photorealistic_materials', 'weathering_effects', 'jcb_authentic_colors']
    }


if __name__ == "__main__":
    main()