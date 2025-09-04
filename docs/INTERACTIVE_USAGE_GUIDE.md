# Interactive Usage Guide

## Getting Started

### Quick Start
1. **Install Dependencies**
   ```bash
   pip install pybullet numpy matplotlib opencv-python pillow
   ```

2. **Run the Application**
   ```bash
   python main.py
   ```

3. **Select Enhanced Web Interface**
   Choose option 1 for the comprehensive web-based interface with all features.

## Enhanced Web Interface

The project now features a **single, comprehensive web-based interface** that consolidates all previously separate simulation modes into one powerful platform.

### Interface Overview
- **Modern Tabbed Design**: Organized into Control, Simulation, Analysis, and Processing tabs
- **Real-time Status Indicators**: Visual feedback for all subsystems
- **Cross-platform Compatibility**: Works on desktop, tablet, and mobile devices
- **API Integration**: RESTful endpoints for advanced functionality

### Usage
```bash
python main.py
# Select option 1: Enhanced Web-Based Interface
# Opens browser automatically to http://localhost:8080
```

**Direct Access:**
```bash
python src/web_interactive_arm.py
```

## Tab-by-Tab Guide

### 1. 🎮 Control Tab
**Purpose**: Real-time joint and camera control

**Features:**
- **Joint Control Sliders**: Control all 4 degrees of freedom (Base, Boom, Stick, Bucket)
- **Camera Controls**: Adjust viewing angle, position, and zoom
- **Real-time Value Display**: Live feedback for all parameters
- **Reset Functions**: Quick return to default positions

**Controls:**
- **Joint Ranges**: 
  - Base: -180° to +180°
  - Boom: -90° to +45°
  - Stick: -135° to +45°
  - Bucket: -120° to +60°
- **Camera**: X/Y positioning (-10 to +10), Z distance (1 to 20)

### 2. ⚡ Simulation Tab
**Purpose**: Physics simulation and real-time dynamics

**Features:**
- **Physics Engine Integration**: PyBullet-based real-time simulation
- **3D Visualization Canvas**: Live rendering of arm movements
- **Simulation Controls**: Start, pause, reset, and export functionality
- **Status Monitoring**: Real-time physics simulation feedback

**Requirements**: PyBullet installation for full functionality

### 3. 📊 Analysis Tab
**Purpose**: Workspace analysis and performance visualization

**Features:**
- **Workspace Mapping**: Reachable area visualization
- **Joint Configuration Studies**: Angle range analysis
- **Performance Metrics**: Speed and accuracy measurements
- **Interactive Plots**: Matplotlib-based analysis charts

**Available Analysis:**
- Workspace boundary mapping
- Joint angle configuration studies
- Reachability analysis
- Performance optimization visualizations

### 4. 🔧 Processing Tab
**Purpose**: CAD file processing and texture enhancement

**Features:**
- **CAD File Upload**: Support for IGS, STEP, SLDPRT formats
- **Mesh Generation**: Automatic collision detection mesh creation
- **Texture Enhancement**: Photorealistic JCB materials with weathering
- **Quality Optimization**: Performance-balanced texture processing

**Supported Formats:**
- IGS (Initial Graphics Exchange Specification)
- STEP (Standard for the Exchange of Product Data)
- SLDPRT (SolidWorks Part files)

## API Integration

The enhanced web interface provides RESTful API endpoints for advanced functionality:

### Physics API
```javascript
// Start physics simulation
fetch('/api/physics?action=start')

// Update joint positions
fetch('/api/physics?action=update', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        base: 45, boom: -30, stick: 45, bucket: -15
    })
})
```

### Analysis API
```javascript
// Generate workspace analysis
fetch('/api/analysis?type=workspace')

// Generate joint configuration study
fetch('/api/analysis?type=joints')
```

### CAD Processing API
```javascript
// Process uploaded CAD files
fetch('/api/cad?action=process')

// Generate collision mesh
fetch('/api/cad?action=mesh')
```

### Texture Enhancement API
```javascript
// Apply JCB textures
fetch('/api/texture?action=enhance')

// Add weathering effects
fetch('/api/texture?action=weather')
```

## Advanced Usage

### System Requirements
- **Minimum**: Web browser with JavaScript support
- **Recommended**: Modern browser with WebGL support
- **Enhanced Features**: Python dependencies for physics, analysis, and texture processing

### Performance Optimization
1. **Close unnecessary applications** before running simulation
2. **Update graphics drivers** for best rendering performance
3. **Use performance mode** on laptops for better frame rates
4. **Install optional dependencies** for full feature access

### Development Integration
The consolidated interface can be extended for custom applications:

```python
from src.web_interactive_arm import EnhancedHandler
import http.server

# Custom API endpoint
class CustomHandler(EnhancedHandler):
    def handle_api_request(self):
        if '/api/custom' in self.path:
            # Custom functionality
            pass
        else:
            super().handle_api_request()
```
SYSTEM_CONFIG = {
    'physics': {
        'timestep': 1/240,
        'gravity': -9.81,
        'solver_iterations': 50
## Configuration Options

The enhanced web interface supports various configuration options through URL parameters and JavaScript:

```javascript
// Configuration example
const config = {
    'physics': {
        'enabled': true,
        'gravity': -9.81,
        'time_step': 1/240
    },
    'rendering': {
        'resolution': 'auto',  // adapts to browser
        'quality': 'high',
        'mobile_optimized': true
    },
    'controls': {
        'touch_support': true,
        'real_time_updates': true,
        'auto_save': true
    }
}
```

## Browser Compatibility

### Supported Browsers
- **Chrome/Chromium**: Full feature support
- **Firefox**: Full feature support  
- **Safari**: Basic support (limited WebGL)
- **Edge**: Full feature support
- **Mobile Browsers**: Touch-optimized interface

### Feature Requirements
- **JavaScript**: Required for all functionality
- **WebGL**: For enhanced 3D visualization
- **Local Storage**: For saving configurations
- **Fetch API**: For backend communication

## Troubleshooting

### Common Issues
1. **Dependencies missing**: Run `pip install -r requirements.txt`
2. **Port 8080 in use**: Change port in web_interactive_arm.py
3. **Poor performance**: Reduce quality settings or upgrade hardware
4. **Browser compatibility**: Use a modern browser with WebGL support
5. **API errors**: Check console for detailed error messages

### Performance Issues
- **High CPU usage**: Disable physics simulation if not needed
- **Slow rendering**: Reduce browser zoom or close other tabs
- **Network timeouts**: Check localhost connectivity

### Debug Mode
Enable debug mode for additional information:
```javascript
// Add to browser console
localStorage.setItem('debug', 'true');
## Support and Documentation

### Additional Resources
- **Main README**: Project overview and quick start
- **Enhanced Features Guide**: Detailed feature documentation
- **CAD Integration Guide**: Professional CAD file processing
- **API Reference**: Developer documentation for extensions

### Getting Help
1. **Check the console**: Browser developer tools provide detailed error information
2. **Review documentation**: Most issues are covered in the guides
3. **Verify dependencies**: Ensure all required packages are installed
4. **Test with minimal setup**: Try basic functionality first

### Contributing
The consolidated web interface provides a foundation for further development:
- **Custom API endpoints**: Extend functionality
- **Enhanced visualizations**: Add new analysis types  
- **Additional file formats**: Expand CAD support
- **Mobile optimizations**: Improve touch interface

---

This comprehensive guide covers the enhanced web interface that consolidates all previous simulation modes into a single, powerful platform. The interface provides access to physics simulation, workspace analysis, CAD processing, and texture enhancement through an intuitive browser-based interface.

### Contributing
The project is designed to be extensible:
- Add new simulation modes in `src/`
- Contribute textures and models to `assets/`
- Improve documentation and examples
- Report issues and suggest enhancements

For technical details and API reference, see the individual module documentation.