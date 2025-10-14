# Virtual Robotic Arm – PUMA 560 Digital Twin

A Streamlit-powered control room for the classic Unimation PUMA 560 robot. Explore six-degrees-of-freedom kinematics, cinematic 3D rendering, and quick engineering insights from a modern web UI.

## ✨ Highlights
- **Authentic PUMA 560 geometry** with Craig DH parameters and accurate joint limits
- 🎨 **Official IIT KGP Virtual Labs model** with high-fidelity Three.js rendering and interactive controls
- **Streamlit control surface** featuring six joint sliders, pose metrics, and instant validation feedback
- **End-Effector Analytics** with real-time position, orientation, velocity, and energy consumption tracking
- **Trajectory Recording** with CSV export, joint angle timelines, and comprehensive motion analysis
- **Workspace Analysis** with manipulability heatmaps, reachability plots, and singularity detection
- **One-command startup** via `python main.py`, including dependency verification and port management

## 🚀 Quick Start
```bash
pip install -r requirements.txt
python main.py
```
The launcher installs missing packages, discovers a free port, and spawns the Streamlit experience in your browser. Prefer to bypass the menu? Run:
```bash
streamlit run src/streamlit_puma_interface.py
```

## 🧭 Interface Tour
- **Joint Console** – Six sliders with PUMA-safe limits, dual-column layout, and real-time numerical readouts
- **3D Robot Visualization** – Official IIT KGP Virtual Labs Three.js model with interactive camera controls
- **End-Effector Analytics** – Real-time position (X/Y/Z), orientation (roll/pitch/yaw), and velocity tracking
- **Trajectory Recording** – Record joint movements with CSV export and multi-tab analysis (angles, paths, velocities, energy)
- **Workspace Analysis** – Generate manipulability heatmaps with 2D/3D visualizations and statistical analysis
- **Real-time Feedback** – Singularity warnings and performance metrics for educational use

## Project Structure
```
VirtualRoboticArm/
├── main.py                     # CLI launcher with dependency checks
├── requirements.txt            # Python dependencies
├── src/
│   └── streamlit_puma_interface.py  # Streamlit UI + kinematics + rendering
├── assets/
│   └── models/
│       └── puma560_vlab_mirror/  # IIT KGP Virtual Labs PUMA 560 model
└── .vscode/                     # VS Code configuration and debug settings
```

## 📦 Dependencies
Core packages are listed in `requirements.txt`:
- `numpy` – numerical operations and DH transforms
- `plotly` – physically-inspired 3D rendering and camera control
- `streamlit` – reactive UI framework and caching primitives
- `pybullet`, `matplotlib`, `opencv-python`, `Pillow` – optional legacy modules retained for compatibility

Install everything with `pip install -r requirements.txt` or let `python main.py` handle it automatically.

## Development Notes
- The main application integrates the official IIT KGP Virtual Labs Three.js PUMA 560 model via HTML components
- Advanced analytics include real-time end-effector position/orientation tracking, velocity estimation, and energy consumption calculations
- Trajectory recording with CSV export supports joint angle timelines, end-effector paths, velocities, and energy analysis
- Workspace heatmaps provide manipulability analysis with 2D/3D visualizations and Monte Carlo sampling
- Scene lighting and camera controls are handled through the embedded Three.js interface
- Workspace sampling uses scipy for efficient manipulability calculations and reachability analysis

## Where to Go Next
1. Add trajectory optimization algorithms for smooth motion planning
2. Implement collision detection with workspace obstacles
3. Add support for custom DH parameters for different robot configurations
4. Integrate path planning algorithms (RRT, A*, etc.) for autonomous operation
5. Add export capabilities for simulation data and analysis reports

Enjoy exploring the reborn PUMA 560!
