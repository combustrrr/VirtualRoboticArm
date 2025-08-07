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

3. **Select Simulation Mode**
   Choose from the available options in the main menu.

## Simulation Modes

### 1. Enhanced CAD Interactive Arm (Recommended)
The most feature-complete simulation mode offering:
- Full 4-DOF control with realistic JCB specifications
- VFX-quality rendering with photorealistic textures
- Real-time physics simulation using PyBullet
- Multiple camera viewpoints and interactive controls

**Usage:**
```bash
python src/enhanced_cad_interactive_arm.py
```

**Controls:**
- **Mouse**: Camera navigation (pan, zoom, rotate)
- **Sliders**: Precise joint angle control
- **Keyboard**: Quick commands and view shortcuts
- **Menu**: Access to advanced features and settings

### 2. Web-Based Interface
Browser-based control system for cross-platform compatibility:
- Touch-friendly interface for mobile devices
- Real-time WebGL rendering
- Live control updates and feedback
- Export and sharing capabilities

**Usage:**
```bash
python src/web_interactive_arm.py
# Opens browser automatically to http://localhost:8080
```

**Features:**
- **Joint Sliders**: Control all 4 degrees of freedom
- **Camera Controls**: Adjust viewing angle and zoom
- **Status Display**: Real-time system information
- **Export Options**: Save configurations and screenshots

### 3. Real CAD Integration
Professional CAD file processing and integration:
- Support for IGS, STEP, and SLDPRT formats
- Automatic mesh generation and optimization
- Material property extraction
- Physics simulation integration

**Usage:**
```bash
python src/real_cad_integration.py
```

**Workflow:**
1. Place CAD files in `assets/models/` directory
2. Run the CAD integration system
3. Review processing results and quality analysis
4. Import into main simulation

### 4. Matplotlib Visualization
Interactive analysis and visualization using Matplotlib:
- Real-time plotting with slider controls
- Workspace analysis and reachability mapping
- Joint configuration studies
- Export-quality figures and animations

**Usage:**
```bash
python src/interactive_matplotlib_arm.py
```

**Features:**
- **Interactive Sliders**: Real-time parameter adjustment
- **Multiple Views**: 2D side view, 3D perspective, workspace analysis
- **Live Updates**: Immediate visual feedback
- **Export**: High-quality figure output

### 5. Realistic Texture Demo
Showcase of advanced texture enhancement capabilities:
- Photorealistic JCB materials
- Weathering and wear effects
- Before/after comparisons
- Texture library exploration

**Usage:**
```bash
python src/realistic_texture_system.py
```

## Advanced Usage

### Automation and Scripting
Create automated sequences for complex operations:

```python
from src.enhanced_cad_interactive_arm import RoboticArm

# Initialize arm
arm = RoboticArm()

# Define excavation sequence
sequence = [
    {'boom': -45, 'stick': 90, 'bucket': 0, 'duration': 2.0},
    {'boom': -30, 'stick': 45, 'bucket': -30, 'duration': 1.5},
    {'boom': 0, 'stick': 0, 'bucket': 0, 'duration': 2.0}
]

# Execute sequence
arm.execute_sequence(sequence)
```

### Custom Configuration
Modify system behavior with configuration files:

```python
# config.py
SYSTEM_CONFIG = {
    'physics': {
        'timestep': 1/240,
        'gravity': -9.81,
        'solver_iterations': 50
    },
    'rendering': {
        'resolution': (1920, 1080),
        'fps_target': 60,
        'quality': 'high'
    },
    'controls': {
        'mouse_sensitivity': 1.0,
        'keyboard_shortcuts': True,
        'touch_support': True
    }
}
```

### Performance Tuning
Optimize performance for your hardware:

```python
# For high-end systems
set_quality_profile('ultra')

# For balanced performance
set_quality_profile('medium')

# For mobile or low-end hardware
set_quality_profile('performance')
```

## Keyboard Shortcuts

### Global Commands
- **Escape**: Exit current mode
- **F11**: Toggle fullscreen
- **F12**: Take screenshot
- **Ctrl+S**: Save current configuration
- **Ctrl+O**: Load configuration

### Camera Controls
- **WASD**: Camera movement
- **Mouse Wheel**: Zoom in/out
- **Right Click + Drag**: Rotate view
- **Middle Click + Drag**: Pan view
- **Home**: Reset camera to default position

### Simulation Controls
- **Space**: Pause/resume simulation
- **R**: Reset arm to home position
- **1-5**: Quick preset positions
- **Ctrl+Z**: Undo last movement
- **Ctrl+Y**: Redo movement

## Tips and Best Practices

### Performance Optimization
1. **Close unnecessary applications** before running simulation
2. **Update graphics drivers** for best rendering performance
3. **Use performance mode** on laptops for better frame rates
4. **Reduce quality settings** if experiencing lag

### Effective Usage
1. **Start with Enhanced CAD mode** for full feature experience
2. **Use Web Interface** for demonstrations and presentations
3. **Matplotlib mode** for analysis and documentation
4. **Save configurations** for repeating specific setups

### Troubleshooting
1. **Dependencies missing**: Run `pip install -r requirements.txt`
2. **Poor performance**: Reduce quality settings or upgrade hardware
3. **Control issues**: Check mouse and keyboard sensitivity settings
4. **Rendering problems**: Verify graphics driver support for OpenGL

## Advanced Features

### Multi-Monitor Support
Configure multiple displays for enhanced workspace:
```python
display_config = {
    'primary': 'simulation_view',
    'secondary': 'control_panel',
    'tertiary': 'analysis_plots'
}
```

### VR Integration (Future)
Virtual reality support for immersive control:
- Hand tracking for natural interaction
- Stereoscopic 3D rendering
- Haptic feedback integration
- Room-scale workspace mapping

### Cloud Integration (Future)
Remote simulation and collaboration:
- Cloud-based physics computation
- Real-time collaboration features
- Remote monitoring and control
- Data synchronization across devices

## Support and Documentation

### Getting Help
- Check the documentation in `docs/` directory
- Review example configurations in `assets/`
- Examine source code in `src/` for implementation details
- Test different simulation modes to find the best fit

### Contributing
The project is designed to be extensible:
- Add new simulation modes in `src/`
- Contribute textures and models to `assets/`
- Improve documentation and examples
- Report issues and suggest enhancements

For technical details and API reference, see the individual module documentation.