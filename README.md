# Interactive 3D JCB Robotic Arm Mini Project

A comprehensive simulation system featuring a professional JCB-style robotic arm with interactive controls, realistic physics, and VFX-quality rendering.

## 🚀 Quick Start

```bash
python main.py
```

This launches the JCB-themed browser experience instantly and opens `http://localhost:8080` with the refreshed Virtual Robotic Arm control center.

Need the legacy menu with every simulation mode? Launch it explicitly:

```bash
python main.py --menu
```

Legacy menu options include:
1. **Enhanced CAD Interactive Arm** (Recommended) - Full-featured 4-DOF control
2. **Web-Based Interface** - Browser-based controls
3. **Real CAD Integration** - Professional CAD file processing
4. **Matplotlib Visualization** - Interactive workspace analysis
5. **Realistic Texture Demo** - Photographic texture showcase

## 🎮 Features

### Core Capabilities
- **4-DOF Control**: Boom, Stick, Bucket, Base Rotation
- **Real-Time Physics**: PyBullet simulation engine
- **Multiple Camera Views**: Wide shot, operator view, dramatic angles
- **Interactive UI**: Sliders, keyboard controls, mouse navigation

### Visual Quality
- **VFX-Grade Rendering**: Professional lighting and shadows
- **Photorealistic Textures**: Authentic JCB materials with weathering
- **Authentic Styling**: Professional yellow/orange construction equipment design
- **High-Resolution Output**: 1920x1080 optimized rendering

### Technical Features
- **CAD Integration**: Support for IGS, STEP, SLDPRT file formats
- **Workspace Analysis**: Reachable area mapping and joint studies
- **Automated Sequences**: Complete excavation cycles
- **Cross-Platform Support**: Native and web-based interfaces

## 📁 Project Structure

```
VirtualRoboticArm/
├── src/                                    # Core source code
│   ├── enhanced_cad_interactive_arm.py     # Main interactive system
│   ├── cad_file_processor.py              # CAD file processing
│   ├── realistic_texture_system.py        # Texture enhancement
│   ├── web_interactive_arm.py             # Web interface
│   ├── interactive_3d_robotic_arm.py      # 3D visualization
│   ├── real_cad_integration.py            # CAD integration
│   └── interactive_matplotlib_arm.py      # Matplotlib interface
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

```bash
pip install -r requirements.txt
```

## 🎬 Demonstrations

The project includes professional demonstration materials:
- **Interactive GIF Demos**: Complete excavation sequences
- **Technical Analysis**: Workspace studies and joint configurations
- **Texture Showcases**: Before/after enhancement comparisons

## 🚜 JCB Specifications

- **Max Reach**: 8.0 meters
- **Max Dig Depth**: 6.2 meters  
- **Bucket Capacity**: 1.2 cubic meters
- **Operating Weight**: 14,500 kg
- **Engine Power**: 100 kW

## 📋 Usage Examples

### Enhanced Interactive Control
```python
python src/enhanced_cad_interactive_arm.py
```

### Web Interface
```python
python src/web_interactive_arm.py
# Opens the JCB Forward Kinematics hub at http://localhost:8080 automatically
```

### CAD Integration
```python
python src/real_cad_integration.py
# Place CAD files in assets/models/
```

## 🎯 Purpose

Perfect for:
- Computer graphics project demonstrations
- Virtual robot prototyping
- Interactive simulation showcases
- Educational robotics visualization
- VFX-quality animation generation

---

**Author**: Sarthak MDM23101B0019  
**Course**: Robotics Semester 5  
**Institution**: [University Name]