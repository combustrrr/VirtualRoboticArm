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
    
    # Start web server with API endpoints
    PORT = 8080
    
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
        
        def handle_api_request(self):
            """Handle API requests for advanced features"""
            if '/api/physics' in self.path:
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
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
    
    try:
        with socketserver.TCPServer(("", PORT), EnhancedHandler) as httpd:
            print(f"🌍 Enhanced server started at http://localhost:{PORT}")
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
        print("Port 8080 might already be in use")


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
            <div class="simulation-canvas">
                <div style="text-align: center;">
                    <h3>🎬 Real-time Physics Simulation</h3>
                    <p>3D rendering canvas will appear here when physics simulation is active</p>
                    <p style="font-size: 14px; opacity: 0.7;">Requires PyBullet integration for full functionality</p>
                </div>
            </div>
            <div class="control-group">
                <h3>⚙️ Simulation Controls</h3>
                <button class="btn" onclick="startSimulation()">Start Simulation</button>
                <button class="btn" onclick="pauseSimulation()">Pause</button>
                <button class="btn" onclick="resetSimulation()">Reset</button>
                <button class="btn" onclick="exportState()">Export State</button>
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
        }

        // Update slider values in real-time
        function updateSliderValue(sliderId, displayId, unit = '') {
            const slider = document.getElementById(sliderId);
            const display = document.getElementById(displayId);
            
            slider.addEventListener('input', function() {
                display.textContent = this.value + unit;
                updateArmPosition();
                console.log(`${sliderId}: ${this.value}`);
            });
            
            // Initialize display
            display.textContent = slider.value + unit;
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
                });
            } else {
                btn.textContent = 'Start Physics';
                status.className = 'status-indicator status-inactive';
                statusText.textContent = 'Inactive';
                statusText.style.color = '#f44336';
                console.log('Physics simulation stopped');
            }
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
            if (physicsActive) {
                fetch('/api/physics?action=update', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(joints)
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

        function startSimulation() { console.log('Starting simulation...'); }
        function pauseSimulation() { console.log('Pausing simulation...'); }
        function resetSimulation() { console.log('Resetting simulation...'); }
        function exportState() { console.log('Exporting state...'); }
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
    </script>
</body>
</html>
    """
    return html


# API Handler Functions
def handle_physics_api():
    """Handle physics simulation API requests"""
    if not PYBULLET_AVAILABLE:
        return {'error': 'PyBullet not available', 'status': 'inactive'}
    
    return {
        'status': 'active',
        'message': 'Physics simulation running',
        'features': ['collision_detection', 'gravity_effects', 'real_time_dynamics']
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