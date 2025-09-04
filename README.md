# Interactive 3D JCB Robotic Arm Mini Project

A comprehensive simulation system featuring a professional JCB-style robotic arm with an enhanced web-based interface that integrates all advanced features including physics simulation, workspace analysis, CAD processing, and realistic textures.

## 🚀 Quick Start

### Automatic Setup (Recommended)
```bash
python main.py
```

The application will automatically:
- ✅ Check for required dependencies 
- 🚀 Install missing packages automatically
- 🎉 Launch the web interface when ready

### Manual Setup (Alternative)
```bash
# Install dependencies manually
python setup.py

# Or using pip directly
pip install -r requirements.txt

# Then run the application
python main.py
```

Select the Enhanced Web-Based Interface for a comprehensive robotic arm simulation experience with all features integrated into a single, modern web interface.

## 🔧 Development Setup

### VS Code Integration
The project includes comprehensive VS Code launch configurations:
- **Launch Virtual Robotic Arm**: Main entry point with automatic dependency setup
- **Launch Web Interface Directly**: Skip menu and go straight to web interface  
- **Debug Virtual Robotic Arm**: Full debugging with breakpoints

### Port Management
- Automatic port detection (8080-8090 range)
- No more manual port closure needed between runs
- Clear feedback when ports are occupied

## 🌐 Enhanced Web Interface

The project now features a **single, comprehensive web-based interface** that consolidates all previously separate interfaces:

- **Real-time Physics Simulation** (PyBullet integration)
- **Interactive Workspace Analysis** (Matplotlib integration)
- **Professional CAD File Processing** (IGS, STEP, SLDPRT support)
- **Photorealistic Texture Enhancement** (JCB materials with weathering)
- **Advanced 3D Visualization** capabilities
- **Cross-platform browser compatibility** with touch-friendly mobile interface

## 🎮 Features

### Core Capabilities
- **4-DOF Control**: Boom, Stick, Bucket, Base Rotation with real-time sliders
- **Real-Time Physics**: Integrated PyBullet simulation engine
- **Multiple Camera Views**: Wide shot, operator view, dramatic angles
- **Interactive Tabbed Interface**: Control, Simulation, Analysis, and Processing tabs

### Visual Quality
- **VFX-Grade Rendering**: Professional lighting and shadows
- **Photorealistic Textures**: Authentic JCB materials with weathering effects
- **Authentic Styling**: Professional yellow/orange construction equipment design
- **Modern Web UI**: Responsive design with status indicators and real-time feedback

### Integrated Systems
- **Physics Simulation**: Real-time collision detection and gravity effects
- **Workspace Analysis**: Reachable area mapping and joint configuration studies
- **CAD Integration**: Professional CAD file processing with mesh generation
- **Texture Enhancement**: Weathering effects and material optimization

## 📁 Project Structure

```
VirtualRoboticArm/
├── src/                                    # Core source code
│   ├── web_interactive_arm.py             # Enhanced web interface (ALL FEATURES)
│   └── cad_file_processor.py              # CAD file processing utilities
├── assets/                                # Project assets
│   ├── realistic_textures/                # Realistic textures
│   ├── models/                            # 3D models and CAD files
│   └── texture_enhancement_demo/          # Texture demos
├── demos/                                 # Demonstration materials
│   └── enhanced_jcb_interactive_demo.gif  # Main demonstration
├── docs/                                  # Documentation
│   ├── README_CAD_INTEGRATION.md         # CAD integration guide
│   ├── README_ENHANCED.md                # Enhanced features
│   └── INTERACTIVE_USAGE_GUIDE.md        # Usage instructions
├── requirements.txt                       # Python dependencies
└── main.py                               # Main entry point
```

## 🔧 Dependencies

### Core Dependencies
```bash
pip install -r requirements.txt
```

### Optional Enhanced Features
- **PyBullet**: For physics simulation (`pip install pybullet`)
- **Matplotlib**: For workspace analysis (`pip install matplotlib`)
- **OpenCV & Pillow**: For texture enhancement (`pip install opencv-python pillow`)

## 🌐 Web Interface Features

### Tabbed Interface
1. **🎮 Control Tab**: Real-time joint and camera controls
2. **⚡ Simulation Tab**: Physics simulation canvas and controls
3. **📊 Analysis Tab**: Workspace analysis and visualization
4. **🔧 Processing Tab**: CAD file processing and texture enhancement

### API Endpoints
- `/api/physics` - Physics simulation control
- `/api/analysis` - Workspace analysis generation
- `/api/cad` - CAD file processing
- `/api/texture` - Texture enhancement

## 📋 Usage

### Enhanced Web Interface (Recommended)
```python
python main.py
# Select option 1 for Enhanced Web Interface
# Opens browser automatically to http://localhost:8080
```

### Direct Web Interface
```python
python src/web_interactive_arm.py
# Direct access to the enhanced web interface
```

## 🚜 JCB Technical Specifications

- **Max Reach**: 8.0 meters
- **Max Dig Depth**: 6.2 meters  
- **Bucket Capacity**: 1.2 cubic meters
- **Operating Weight**: 14,500 kg
- **Engine Power**: 100 kW
- **Degrees of Freedom**: 4 (Base, Boom, Stick, Bucket)

## 🎯 Purpose

Perfect for:
- **Computer Graphics Projects**: Professional-quality demonstrations
- **Virtual Robot Prototyping**: Complete simulation environment
- **Interactive Educational Tools**: Robotics visualization and learning
- **Web-Based Simulations**: Cross-platform accessibility
- **Research and Development**: Advanced robotics research platform

## 🔄 Migration from Multiple Interfaces

**Previous Version**: 5+ separate interfaces (Enhanced CAD, Matplotlib, Real CAD, Texture System, 3D Visualization)
**Current Version**: Single comprehensive web interface with all features integrated

**Benefits of Consolidation**:
- Unified user experience
- Reduced code duplication  
- Easier maintenance and updates
- Better performance through shared resources
- Modern web-based architecture

---

**Author**: Sarthak MDM23101B0019  
**Course**: Robotics Semester 5  
**Institution**: [University Name]