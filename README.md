# Virtual Robotic Arm - Interactive 3D JCB Simulation

A comprehensive robotic arm simulation system featuring a realistic JCB-style excavator arm with PyBullet physics, interactive web controls, and real-time 3D visualization.

## ✨ Key Features

- 🤖 **Real Physics Simulation** - PyBullet-powered robotic arm with accurate kinematics
- 🎮 **Interactive Web Interface** - Browser-based controls with real-time feedback  
- 🔧 **4 Degrees of Freedom** - Base rotation, boom, stick, and bucket control
- 📊 **Workspace Analysis** - Reachable area visualization and joint studies
- ⚙️ **Automatic Setup** - Intelligent dependency management and port handling
- 🎯 **JCB Specifications** - Realistic 8m reach, 6.2m dig depth, 1.2m³ bucket capacity

## 🚀 Quick Start

### Automatic Setup (Recommended)
```bash
python main.py
```

The application will automatically:
- ✅ Check and install missing dependencies (pybullet, numpy, matplotlib, opencv-python, pillow)
- 🚀 Find available port (8080-8090 range) to avoid conflicts
- 🌐 Launch web interface in your default browser
- 🎉 Provide real-time robot simulation

### Alternative Setup Methods
```bash
# Manual dependency installation first
python setup.py

# Install dependencies using pip directly  
pip install -r requirements.txt

# Then run the main application
python main.py
```

### Direct Web Interface Access
```bash
# Skip menu and launch web interface directly
python src/web_interactive_arm.py
```

## 🔧 Development Setup

### VS Code Integration
The project includes comprehensive VS Code launch configurations in `.vscode/launch.json`:

- **Launch Virtual Robotic Arm** - Main entry point with automatic dependency setup
- **Launch Web Interface Directly** - Skip menu and go straight to web interface  
- **Debug Virtual Robotic Arm** - Full debugging with breakpoints and step-through
- **Setup Dependencies** - Run dependency installation separately

### Port Management
- **Automatic Port Detection** - Finds available ports in 8080-8090 range
- **No Manual Port Closure** - Eliminates need to manually close ports between runs
- **Clear User Feedback** - Shows which port is being used when default is occupied

### Dependency Management
The application intelligently handles dependencies:
- **Automatic Detection** - Scans `requirements.txt` for missing packages
- **Smart Installation** - Installs only missing dependencies with timeout protection
- **Network Error Handling** - Graceful fallbacks for connectivity issues
- **Manual Fallback Instructions** - Clear guidance when automatic installation fails

## 🌐 Web Interface

The application features a **comprehensive web-based interface** that provides all functionality through your browser:

### Main Features
- **Real-time Physics Simulation** - PyBullet integration with collision detection
- **Interactive Joint Controls** - 4-DOF arm control with real-time sliders
- **3D Robot Visualization** - Live 2D representation with hydraulic cylinders
- **Workspace Analysis** - Reachable area mapping and joint studies
- **Export Functionality** - Save robot configurations as JSON
- **Cross-platform Compatibility** - Works on desktop, tablet, and mobile

### Technical Specifications
- **Realistic JCB Model** - 8m max reach, 6.2m dig depth, 1.2m³ bucket capacity
- **4 Degrees of Freedom** - Base rotation (±180°), boom (-90° to 45°), stick (-135° to 45°), bucket (-120° to 60°)
- **Physics Engine** - Real-time PyBullet simulation with gravity and collision detection
- **End-effector Calculation** - Live position tracking and workspace monitoring

### Robot Controls
- **Base Rotation** - Full 360° rotation capability
- **Boom Control** - Primary lift arm with realistic hydraulic limits
- **Stick Control** - Secondary arm extension with joint constraints  
- **Bucket Control** - Digging bucket with tilt functionality
- **Camera Controls** - Adjustable viewing angle and position

## 🎮 Features

### Core Robot Simulation
- **4-DOF Control** - Boom, stick, bucket, and base rotation with real-time feedback
- **Physics Integration** - PyBullet simulation engine with gravity and collision detection
- **Realistic Kinematics** - Accurate joint constraints and movement limits
- **End-effector Tracking** - Live position calculation and workspace monitoring

### Interactive Interface
- **Web-based Controls** - Browser interface with responsive design
- **Real-time Sliders** - Precise joint control with immediate visual feedback
- **Visual Robot Display** - 2D representation showing current arm configuration
- **Status Monitoring** - Live display of joint angles and system status

### Advanced Features
- **Workspace Analysis** - Reachable area visualization using matplotlib
- **Configuration Export** - Save and load robot positions as JSON
- **Multiple Camera Views** - Adjustable viewing angles and positions
- **Mobile Support** - Touch-friendly interface for tablets and phones

## 📁 Project Structure

```
VirtualRoboticArm/
├── .vscode/                     # VS Code configuration
│   └── launch.json             # Debug and launch configurations
├── src/                        # Core source code
│   └── web_interactive_arm.py  # Main web interface with all features
├── assets/                     # Project assets
│   ├── realistic_textures/     # Texture files
│   ├── models/                 # 3D models and assets
│   └── texture_enhancement_demo/ # Demonstration materials
├── demos/                      # Demonstration videos and images
├── docs/                       # Documentation
│   ├── README_ENHANCED.md      # Enhanced features guide
│   ├── README_CAD_INTEGRATION.md # CAD integration documentation
│   └── INTERACTIVE_USAGE_GUIDE.md # Detailed usage instructions
├── requirements.txt            # Python dependencies
├── setup.py                   # Dependency installation script
├── main.py                    # Main entry point with auto-setup
└── README.md                  # This file
```

## 🔧 Dependencies

### Core Requirements
All dependencies are automatically managed through `requirements.txt`:

```txt
pybullet>=3.2.0      # Physics simulation engine
numpy>=1.21.0        # Numerical computations
matplotlib>=3.5.0    # Plotting and analysis
opencv-python>=4.5.0 # Image processing
Pillow>=8.3.0        # Image manipulation
```

### Installation Methods
1. **Automatic** - Run `python main.py` (recommended)
2. **Setup Script** - Run `python setup.py`  
3. **Manual** - Run `pip install -r requirements.txt`

## 📋 Usage

### Getting Started
1. **Clone the repository**
   ```bash
   git clone https://github.com/combustrrr/VirtualRoboticArm.git
   cd VirtualRoboticArm
   ```

2. **Run the application**
   ```bash
   python main.py
   ```
   
3. **Access the web interface**
   - Browser opens automatically to `http://localhost:8080` (or next available port)
   - Interface provides real-time robot control and visualization

### Web Interface Controls
- **Joint Sliders** - Control base rotation, boom, stick, and bucket angles
- **Camera Controls** - Adjust viewing position (X, Y, Z coordinates)
- **Reset Functions** - Return robot to default position
- **Export/Import** - Save and load robot configurations

### Advanced Usage
```python
# Direct access to web interface
python src/web_interactive_arm.py

# Setup dependencies only
python setup.py
```

## 🚜 JCB Technical Specifications

The robotic arm simulation is modeled after real JCB excavator specifications:

| Specification | Value |
|---------------|--------|
| **Max Reach** | 8.0 meters |
| **Max Dig Depth** | 6.2 meters |
| **Bucket Capacity** | 1.2 cubic meters |
| **Operating Weight** | 14,500 kg |
| **Engine Power** | 100 kW |
| **Degrees of Freedom** | 4 (Base, Boom, Stick, Bucket) |

### Joint Ranges
- **Base Rotation**: -180° to +180° (full rotation)
- **Boom**: -90° to +45° (primary lift arm)
- **Stick**: -135° to +45° (secondary extension)
- **Bucket**: -120° to +60° (digging bucket tilt)

## 🎯 Applications

Perfect for:
- **Robotics Education** - Interactive learning and visualization
- **Simulation Development** - Testing control algorithms and kinematics
- **Research Projects** - Workspace analysis and trajectory planning
- **Demonstration** - Professional-quality robotic arm simulation
- **Prototyping** - Virtual testing before physical implementation

## 🛠️ Development

### Extending the Application
The modular design allows for easy extension:

```python
# Add custom functionality to the web interface
from src.web_interactive_arm import EnhancedHandler

class CustomHandler(EnhancedHandler):
    def handle_custom_api(self):
        # Custom API endpoints
        pass
```

### Contributing
- **Report Issues** - Use GitHub issues for bugs and feature requests
- **Submit Pull Requests** - Contribute improvements and new features
- **Documentation** - Help improve guides and examples
- **Testing** - Test on different platforms and configurations

## 🔧 Troubleshooting

### Common Issues
- **Dependencies Missing** - Run `python main.py` for automatic installation
- **Port Conflicts** - Application automatically finds available ports (8080-8090)
- **Performance Issues** - Close unnecessary applications, update graphics drivers
- **Browser Compatibility** - Use modern browsers (Chrome, Firefox, Edge, Safari)

### Getting Help
1. Check browser console for error messages
2. Verify all dependencies are installed: `pip list`
3. Test with minimal setup: `python src/web_interactive_arm.py`
4. Review documentation in `docs/` directory

## 📄 License

This project is open source. See individual files for specific licensing information.

---

**Author**: Sarthak MDM23101B0019  
**Course**: Robotics Semester 5  
**Project**: Interactive 3D JCB Robotic Arm Simulation