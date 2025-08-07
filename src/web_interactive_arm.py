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
            if self.path == '/' or self.path == '/index.html':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode())
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
    </style>
</head>
<body>
    <div class="container">
        <h1>🚜 Virtual JCB Robotic Arm - Web Interface</h1>
        
        <div class="jcb-specs">
            <h3>🚜 JCB Specifications</h3>
            <p><strong>Max Reach:</strong> 8.0 meters | <strong>Max Dig Depth:</strong> 6.2 meters | <strong>Bucket Capacity:</strong> 1.2 cubic meters</p>
            <p><strong>Operating Weight:</strong> 14,500 kg | <strong>Engine Power:</strong> 100 kW</p>
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
        </div>
        
        <div class="status">
            <h3>🔧 Implementation Status</h3>
            <p>This is a placeholder web interface for the Virtual Robotic Arm.</p>
            <p>The full implementation would include:</p>
            <ul style="text-align: left; display: inline-block;">
                <li>WebGL-based 3D rendering of the robotic arm</li>
                <li>Real-time communication with PyBullet simulation</li>
                <li>Live physics simulation in the browser</li>
                <li>Advanced controls and automation sequences</li>
                <li>Mobile-responsive touch controls</li>
            </ul>
        </div>
    </div>

    <script>
        // Update slider values in real-time
        function updateSliderValue(sliderId, displayId, unit = '') {
            const slider = document.getElementById(sliderId);
            const display = document.getElementById(displayId);
            
            slider.addEventListener('input', function() {
                display.textContent = this.value + unit;
                // Here you would send the value to the backend
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
    </script>
</body>
</html>
    """
    return html


if __name__ == "__main__":
    main()