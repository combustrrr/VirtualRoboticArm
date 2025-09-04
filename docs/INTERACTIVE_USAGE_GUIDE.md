# Interactive Usage Guide

## Getting Started

### Quick Start
1. **Install and Run (Automatic Setup)**
   ```bash
   git clone https://github.com/combustrrr/VirtualRoboticArm.git
   cd VirtualRoboticArm
   python main.py
   ```
   
   The application will automatically:
   - ✅ Check for missing dependencies (pybullet, numpy, matplotlib, opencv-python, pillow)
   - 🚀 Install missing packages with network error handling
   - 🔍 Find available port (8080-8090 range) to avoid conflicts  
   - 🌐 Launch web interface in your default browser

2. **Alternative Setup Methods**
   ```bash
   # Manual dependency installation first
   python setup.py
   
   # Install with pip directly
   pip install -r requirements.txt
   
   # Then run the application
   python main.py
   ```

3. **Direct Web Interface Access**
   ```bash
   # Skip menu and launch web interface directly
   python src/web_interactive_arm.py
   ```

## Comprehensive Web Interface

The project features a **single, unified web-based interface** that provides all robotic arm simulation functionality through your browser.

### Interface Overview
- **Real-time Robot Control** - Interactive sliders for all 4 joints
- **Live 2D Visualization** - Robot arm representation with hydraulic cylinders
- **Physics Integration** - PyBullet simulation with collision detection
- **Workspace Analysis** - Matplotlib-based reachable area visualization
- **Export/Import** - Save and load robot configurations as JSON
- **Cross-platform** - Works on desktop, tablet, and mobile devices

### Accessing the Interface
```bash
python main.py
# Browser opens automatically to http://localhost:8080 (or next available port)
```

**Direct Access:**
```bash
python src/web_interactive_arm.py
# Direct launch without menu system
```

## Complete Feature Guide

### Real-time Robot Control
**Interactive Joint Sliders:**
- **Base Rotation**: -180° to +180° (full 360° rotation capability)
- **Boom Control**: -90° to +45° (primary lift arm with hydraulic limits)  
- **Stick Control**: -135° to +45° (secondary arm extension with joint constraints)
- **Bucket Control**: -120° to +60° (digging bucket with realistic tilt range)

**Camera Controls:**
- **Camera X/Y Position**: -10 to +10 meters (adjust viewing angle)
- **Camera Z Distance**: 1 to 20 meters (zoom in/out for different perspectives)
- **Reset View**: Return camera to default position

**Visual Feedback:**
- **Real-time 2D Robot Display**: Shows current arm configuration with hydraulic cylinders
- **Live Joint Angle Display**: Current position of each joint in degrees
- **End-effector Position**: X, Y, Z coordinates of bucket tip
- **Status Indicators**: System status and simulation state

### Physics Simulation Integration
**PyBullet Physics Engine:**
- **Real-time Simulation**: Physics calculations with gravity and collision detection
- **Realistic Kinematics**: Accurate joint constraints and movement limits
- **Collision Avoidance**: Prevents impossible arm configurations
- **Dynamic Response**: Realistic movement behavior with inertia

**Simulation Controls:**
- **Initialize Physics**: Start PyBullet simulation engine
- **Reset Robot**: Return to default pose
- **Real-time Updates**: Continuous physics simulation during control

### Workspace Analysis
**Matplotlib Integration:**
- **Reachable Area Visualization**: 2D plot showing workspace boundary
- **Joint Configuration Studies**: Analysis of joint angle combinations
- **Performance Metrics**: Reach envelope and working area calculations
- **Interactive Plots**: Zoom, pan, and analyze workspace data

**Analysis Features:**
- **Generate Workspace**: Calculate and visualize reachable area
- **Boundary Mapping**: Show maximum reach envelope  
- **Joint Studies**: Analyze optimal joint configurations
- **Export Analysis**: Save workspace plots and data

### Configuration Management
**Export/Import Functionality:**
- **Save Configurations**: Export current robot pose as JSON
- **Load Configurations**: Import and apply saved poses
- **Multiple Presets**: Store and recall different arm positions
- **Batch Operations**: Save multiple configurations for sequences

**Configuration Format:**
```json
{
    "joints": {
        "base": 0,
        "boom": -30,
        "stick": 45,
        "bucket": -15
    },
    "camera": {
        "x": 0,
        "y": 0,  
        "z": 5
    },
    "timestamp": "2024-01-01T12:00:00"
}
```

## API Integration and Advanced Usage

The web interface provides API endpoints for programmatic control and integration:

### Robot Control API
```javascript
// Update joint positions
fetch('/api/robot/joints', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        base: 45,
        boom: -30, 
        stick: 45,
        bucket: -15
    })
});

// Get current robot status
fetch('/api/robot/status')
    .then(response => response.json())
    .then(data => console.log('Robot status:', data));
```

### Physics Simulation API
```javascript
// Initialize physics engine
fetch('/api/physics/init', {method: 'POST'});

// Reset robot to default pose
fetch('/api/physics/reset', {method: 'POST'});

// Get physics simulation state
fetch('/api/physics/status');
```

### Workspace Analysis API
```javascript
// Generate workspace analysis
fetch('/api/analysis/workspace', {method: 'POST'})
    .then(response => response.blob())
    .then(blob => {
        // Display workspace plot
        const img = document.createElement('img');
        img.src = URL.createObjectURL(blob);
        document.body.appendChild(img);
    });
```

### Configuration Management API
```javascript
// Export current configuration
fetch('/api/config/export')
    .then(response => response.json())
    .then(config => {
        // Save or process configuration
        localStorage.setItem('robotConfig', JSON.stringify(config));
    });

// Import configuration
const config = JSON.parse(localStorage.getItem('robotConfig'));
fetch('/api/config/import', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(config)
});
```

## Development Setup

### VS Code Integration
The project includes comprehensive development configurations:

**Launch Configurations (.vscode/launch.json):**
1. **Launch Virtual Robotic Arm** - Main entry point with auto-setup
2. **Launch Web Interface Directly** - Skip menu, direct web launch
3. **Debug Virtual Robotic Arm** - Full debugging with breakpoints
4. **Setup Dependencies** - Run dependency installation only

**Using VS Code:**
1. Open project folder in VS Code
2. Press F5 or go to Run and Debug panel
3. Select desired launch configuration
4. Start debugging/running

### Dependency Management
**Automatic Installation:**
```python
# main.py handles automatic dependency checking and installation
def check_and_install_dependencies():
    # Checks requirements.txt against installed packages
    # Installs missing dependencies with pip
    # Handles network timeouts gracefully
    # Provides manual installation instructions
```

**Manual Installation:**
```bash
# Individual package installation
pip install pybullet>=3.2.0
pip install numpy>=1.21.0  
pip install matplotlib>=3.5.0
pip install opencv-python>=4.5.0
pip install Pillow>=8.3.0

# Or install all at once
pip install -r requirements.txt
```

### Port Management
**Automatic Port Detection:**
```python
def find_available_port(start_port=8080, max_attempts=10):
    """Find available port to avoid conflicts"""
    # Scans ports 8080-8090
    # Returns first available port
    # Handles port conflicts automatically
```

**Benefits:**
- No manual port closure needed between runs
- Clear user feedback about which port is being used
- Eliminates "address already in use" errors

## System Requirements and Performance

### Hardware Requirements
- **Minimum**: Modern web browser, 4GB RAM, integrated graphics
- **Recommended**: Chrome/Firefox, 8GB RAM, dedicated graphics for smooth simulation
- **Optimal**: Latest browser, 16GB+ RAM, high-end GPU for complex workspace analysis
### Software Requirements
- **Modern Web Browser**: Chrome, Firefox, Edge, or Safari with JavaScript enabled
- **Python 3.7+**: For running the application and installing dependencies
- **Network Access**: For automatic dependency installation (optional)

### Performance Optimization
1. **Close unnecessary browser tabs** and applications before running simulation
2. **Update graphics drivers** for best WebGL rendering performance
3. **Use performance mode** on laptops for better frame rates
4. **Install all dependencies** for full feature access and optimal performance

### Browser Compatibility
- **Chrome/Chromium**: Full feature support with best performance
- **Firefox**: Full feature support with good performance
- **Edge**: Full feature support on modern versions
- **Safari**: Basic support (limited WebGL on older versions)
- **Mobile Browsers**: Touch-optimized interface with reduced features

## Configuration and Customization

### Robot Configuration
```python
# Customize robot parameters in web_interactive_arm.py
ROBOT_CONFIG = {
    'base_radius': 1.0,
    'boom_length': 3.5,
    'stick_length': 2.8,
    'bucket_length': 1.2,
    'joint_limits': {
        'base': (-180, 180),
        'boom': (-90, 45),
        'stick': (-135, 45),
        'bucket': (-120, 60)
    }
}
```

### Interface Configuration
```javascript
// Customize web interface behavior
const config = {
    'auto_update': true,           // Real-time robot updates
    'show_workspace': true,        // Display workspace analysis
    'enable_export': true,         // Configuration export/import
    'mobile_optimized': true,      // Touch-friendly controls
    'physics_enabled': true        // PyBullet physics simulation
}
```

### Advanced Customization
The application can be extended for custom applications:

```python
from src.web_interactive_arm import EnhancedHandler
import http.server

# Custom API endpoint handler
class CustomHandler(EnhancedHandler):
    def handle_api_request(self):
        if '/api/custom' in self.path:
            # Add custom functionality here
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "custom_api_success"}')
## Troubleshooting

### Common Issues and Solutions

1. **Automatic Setup Issues**
   ```bash
   # Problem: Dependencies fail to install automatically
   # Solution: Manual installation
   pip install -r requirements.txt
   python main.py
   ```

2. **Port Conflicts**
   ```bash
   # Problem: Port 8080 already in use
   # Solution: Application automatically finds next available port (8081-8090)
   # No manual intervention needed
   ```

3. **PyBullet Installation Issues**
   ```bash
   # Problem: PyBullet fails to install on Windows
   # Solution: Install Visual C++ redistributables first
   # Download from Microsoft website, then retry
   pip install pybullet
   ```

4. **Browser Compatibility**
   ```bash
   # Problem: Interface doesn't load properly
   # Solution: Use modern browser with JavaScript enabled
   # Recommended: Chrome, Firefox, Edge (latest versions)
   ```

5. **Performance Issues**
   - **High CPU Usage**: Close unnecessary applications and browser tabs
   - **Slow Response**: Disable physics simulation if not needed
   - **Rendering Problems**: Update graphics drivers, check WebGL support

### Debug Information

**Enable Debug Mode:**
```javascript
// In browser console (F12 -> Console tab)
localStorage.setItem('debug', 'true');
// Reload page to see debug information
```

**Check System Status:**
```python
# In Python console or add to main.py
import sys
print(f"Python version: {sys.version}")
import pybullet as p
print("PyBullet available")
import matplotlib
print(f"Matplotlib version: {matplotlib.__version__}")
```

**Browser Console Errors:**
1. Press F12 to open Developer Tools
2. Go to Console tab
3. Look for error messages in red
4. Common errors and solutions:
   - "Failed to fetch": Check if server is running
   - "WebGL not supported": Update browser or graphics drivers
   - "404 Not Found": Verify all files are present

## Additional Resources

### Documentation Files
- **README.md**: Main project overview and quick start guide
- **docs/README_ENHANCED.md**: Detailed feature documentation
- **docs/README_CAD_INTEGRATION.md**: CAD file processing guide
- **docs/INTERACTIVE_USAGE_GUIDE.md**: This comprehensive usage guide

### Getting Help
1. **Check Browser Console**: F12 → Console tab for detailed error messages
2. **Verify Dependencies**: Run `pip list` to check installed packages
3. **Test Basic Functionality**: Try `python src/web_interactive_arm.py` directly
4. **Review Documentation**: Most common issues are covered in the guides

### Contributing and Development
The application is designed for easy extension and contribution:

**Add New Features:**
```python
# Extend the web interface
class CustomHandler(EnhancedHandler):
    def do_GET(self):
        if '/custom' in self.path:
            # Custom functionality
            pass
        else:
            super().do_GET()
```

**Contribute to Project:**
- Report bugs and issues on GitHub
- Submit pull requests with improvements
- Add documentation and examples
- Test on different platforms and configurations

**Development Guidelines:**
- Follow existing code structure and style
- Add appropriate documentation for new features
- Test changes thoroughly before submitting
- Consider backward compatibility with existing configurations

---

This comprehensive guide covers all aspects of using the Virtual Robotic Arm simulation system. The unified web interface provides a powerful platform for robotics education, research, and development with professional-quality visualization and real-time physics simulation.

This comprehensive guide covers the enhanced web interface that consolidates all previous simulation modes into a single, powerful platform. The interface provides access to physics simulation, workspace analysis, CAD processing, and texture enhancement through an intuitive browser-based interface.

### Contributing
The project is designed to be extensible:
- Add new simulation modes in `src/`
- Contribute textures and models to `assets/`
- Improve documentation and examples
- Report issues and suggest enhancements

For technical details and API reference, see the individual module documentation.