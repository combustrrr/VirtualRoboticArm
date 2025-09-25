"""
Web Interactive Arm - Browser-based controls
Cross-platform web interface for robotic arm control
"""
import sys
import os
import threading
import time
import logging
try:
    import http.server
    import socketserver
    import webbrowser
    WEB_SERVER_AVAILABLE = True
except ImportError:
    WEB_SERVER_AVAILABLE = False


logger = logging.getLogger("web_interactive_arm")


def main():
    """Main function for Web Interactive Arm"""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
    )
    print("=" * 60)
    print("WEB INTERACTIVE ARM")
    print("=" * 60)
    print("Browser-based controls for Virtual Robotic Arm")
    print()
    
    if not WEB_SERVER_AVAILABLE:
        print("❌ Web server components not available")
        logger.error("Required web server modules missing; cannot start web interface")
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
            logger.info("Incoming request: %s", self.path)
            if self.path in ('/', '/index.html'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode())
                logger.info("Served simulator HTML for path %s", self.path)
            elif self.path == '/favicon.ico':
                # Respond with no content to avoid 404 noise
                self.send_response(204)
                self.end_headers()
                logger.debug("Ignored favicon request")
            else:
                logger.debug("Delegating static asset request to SimpleHTTPRequestHandler: %s", self.path)
                super().do_GET()
    
        def log_message(self, format, *args):
            # Route default logging through our logger for consistency
            logger.info("HTTP %s - %s", self.address_string(), format % args)

    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    try:
        with ReusableTCPServer(("", PORT), CustomHandler) as httpd:
            logger.info("Server listening at http://localhost:%s", PORT)
            print(f"🌍 Server started at http://localhost:{PORT}")
            print("🔧 Implementation Status:")
            print("Serving PUMA 560 Forward Kinematics Simulator")
            print("The simulator includes:")
            print("- 3D visualization with Three.js")
            print("- Forward kinematics calculations")
            print("- Interactive joint controls")
            print("- Workspace plotting")
            print("- Real-time transformation matrix display")
            print()
            print("Opening web browser...")
            
            # Open browser in a separate thread
            def open_browser():
                time.sleep(1)  # Give server time to start
                launch_url = f'http://localhost:{PORT}'
                logger.info("Opening default browser to %s", launch_url)
                try:
                    webbrowser.open(launch_url)
                except Exception:  # pragma: no cover - best effort logging
                    logger.exception("Failed to open browser automatically")
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            print(f"Press Ctrl+C to stop the server")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        logger.info("Server shutdown requested via keyboard interrupt")
    except OSError as e:
        print(f"❌ Error starting server: {e}")
        print("Port 8080 might already be in use")
        logger.exception("Failed to bind server socket on port %s", PORT)


def create_web_interface():
    """Create PUMA 560 simulator web interface"""
    try:
        # Read the PUMA simulator HTML file
        html_file_path = os.path.join(os.path.dirname(__file__), '..', 'puma560_simulator.html')
        logger.debug("Attempting to read simulator HTML from %s", html_file_path)
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        logger.info("Successfully loaded simulator HTML (%d characters)", len(html_content))
        return html_content
    except FileNotFoundError:
        print("❌ PUMA simulator HTML file not found. Using basic interface.")
        logger.error("Simulator HTML not found at expected path: %s", html_file_path)
        # Fallback to basic interface
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Virtual Robotic Arm - Web Interface</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #333; text-align: center; }
        .message { background: #f0f0f0; padding: 20px; border-radius: 8px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Virtual Robotic Arm</h1>
        <div class="message">
            <h2>🔧 PUMA 560 Simulator</h2>
            <p>The PUMA 560 forward kinematics simulator HTML file was not found.</p>
            <p>Please ensure <code>puma560_simulator.html</code> exists in the project root.</p>
        </div>
    </div>
</body>
</html>"""


if __name__ == "__main__":
    main()
