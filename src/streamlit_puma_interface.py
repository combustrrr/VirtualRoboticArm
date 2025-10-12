"""Streamlit UI embedding the IIT KGP PUMA 560 Three.js model with Streamlit controls."""
from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import List, Tuple, Dict, Any
import time
import csv
from io import StringIO
import pandas as pd

import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
from scipy.spatial.distance import cdist
from scipy import interpolate
import random

st.set_page_config(
    page_title="PUMA 560 Digital Twin",
    page_icon="🤖",
    layout="wide",
)

JOINT_LIMITS: Tuple[Tuple[int, int], ...] = (
    (-160, 160),
    (-225, 45),
    (-225, 45),
    (-110, 170),
    (-100, 100),
    (-226, 226),
)

JOINT_LABELS: Tuple[str, ...] = (
    "Waist",
    "Shoulder",
    "Elbow",
    "Wrist Roll",
    "Wrist Bend",
    "Wrist Swivel",
)

# DH parameters for PUMA 560 (from IIT KGP simulation)
DH_PARAMS = [
    (0.0, 0.0, 0.0, math.pi/2),      # Joint 1
    (0.0, 0.0, 0.432, 0.0),         # Joint 2
    (0.0, 0.1495, 0.0203, -math.pi/2), # Joint 3
    (0.0, 0.432, 0.0, math.pi/2),   # Joint 4
    (0.0, 0.0, 0.0, -math.pi/2),    # Joint 5
    (0.0, 0.0, 0.0, 0.0)            # Joint 6
]

ASSET_ROOT = (
    Path(__file__).resolve().parent.parent
    / "assets"
    / "models"
    / "puma560_vlab_mirror"
    / "exp"
    / "forward-kinematics"
    / "simulation"
)


@lru_cache(maxsize=None)
def _load_asset(path_relative: str) -> str:
    return (ASSET_ROOT / path_relative).read_text(encoding="utf-8")


def _dh_transform(theta: float, d: float, a: float, alpha: float) -> np.ndarray:
    """Compute homogeneous transformation matrix from DH parameters."""
    ct = math.cos(theta)
    st = math.sin(theta)
    ca = math.cos(alpha)
    sa = math.sin(alpha)
    
    return np.array([
        [ct, -st*ca, st*sa, a*ct],
        [st, ct*ca, -ct*sa, a*st],
        [0, sa, ca, d],
        [0, 0, 0, 1]
    ])


def _forward_kinematics(joint_angles_deg: List[float]) -> Tuple[np.ndarray, np.ndarray]:
    """Calculate end-effector pose from joint angles."""
    # Convert to radians
    joint_angles_rad = [math.radians(angle) for angle in joint_angles_deg]
    
    # Initialize transformation matrix
    T = np.eye(4)
    
    # Apply each joint transformation
    for i, (theta_offset, d, a, alpha) in enumerate(DH_PARAMS):
        theta = joint_angles_rad[i] + theta_offset
        T_i = _dh_transform(theta, d, a, alpha)
        T = T @ T_i
    
    # Extract position and rotation matrix
    position = T[:3, 3]
    rotation = T[:3, :3]
    
    return position, rotation


def _rotation_to_euler(R: np.ndarray) -> Tuple[float, float, float]:
    """Convert rotation matrix to roll, pitch, yaw (in degrees)."""
    sy = math.sqrt(R[0,0] * R[0,0] + R[1,0] * R[1,0])
    
    singular = sy < 1e-6
    
    if not singular:
        roll = math.atan2(R[2,1], R[2,2])
        pitch = math.atan2(-R[2,0], sy)
        yaw = math.atan2(R[1,0], R[0,0])
    else:
        roll = math.atan2(-R[1,2], R[1,1])
        pitch = math.atan2(-R[2,0], sy)
        yaw = 0
    
    return math.degrees(roll), math.degrees(pitch), math.degrees(yaw)


def _calculate_velocity(current_pos: np.ndarray, prev_pos: np.ndarray, dt: float) -> float:
    """Calculate linear velocity magnitude."""
    if dt <= 0:
        return 0.0
    velocity_vector = (current_pos - prev_pos) / dt
    return np.linalg.norm(velocity_vector)


def _calculate_joint_velocities(current_angles: List[float], prev_angles: List[float], dt: float) -> List[float]:
    """Calculate joint angular velocities in deg/s."""
    if dt <= 0:
        return [0.0] * len(current_angles)
    
    velocities = []
    for curr, prev in zip(current_angles, prev_angles):
        vel = (curr - prev) / dt
        velocities.append(vel)
    return velocities


def _estimate_energy_consumption(joint_velocities: List[float], joint_angles: List[float]) -> float:
    """Estimate relative energy consumption based on joint motion and loading."""
    # Simple energy proxy: sum of squared velocities weighted by joint position
    # This approximates motor power consumption
    energy = 0.0
    joint_weights = [1.0, 1.2, 1.0, 0.8, 0.6, 0.4]  # Heavier joints consume more
    
    for i, (vel, angle, weight) in enumerate(zip(joint_velocities, joint_angles, joint_weights)):
        # Energy increases with velocity^2 and joint loading (gravity effects)
        gravity_factor = abs(math.cos(math.radians(angle))) if i < 3 else 1.0
        energy += weight * (vel ** 2) * gravity_factor
    
    return energy


def _export_trajectory_csv(trajectory_data: List[Dict[str, Any]]) -> str:
    """Convert trajectory data to CSV format."""
    if not trajectory_data:
        return ""
    
    output = StringIO()
    fieldnames = trajectory_data[0].keys()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(trajectory_data)
    
    return output.getvalue()


def _calculate_jacobian(joint_angles_deg: List[float]) -> np.ndarray:
    """Calculate the Jacobian matrix for manipulability analysis."""
    # Simplified Jacobian calculation for PUMA 560
    # This is an approximation - in practice, you'd use proper symbolic differentiation
    epsilon = 0.1  # Small angle for numerical differentiation
    
    position_base, _ = _forward_kinematics(joint_angles_deg)
    jacobian = np.zeros((3, 6))  # 3D position, 6 joints
    
    for i in range(6):
        # Numerical differentiation
        angles_plus = joint_angles_deg.copy()
        angles_minus = joint_angles_deg.copy()
        angles_plus[i] += epsilon
        angles_minus[i] -= epsilon
        
        pos_plus, _ = _forward_kinematics(angles_plus)
        pos_minus, _ = _forward_kinematics(angles_minus)
        
        jacobian[:, i] = (pos_plus - pos_minus) / (2 * epsilon)
    
    return jacobian


def _calculate_manipulability(jacobian: np.ndarray) -> float:
    """Calculate manipulability index from Jacobian matrix."""
    # Manipulability = sqrt(det(J * J^T))
    try:
        jjt = jacobian @ jacobian.T
        det_jjt = np.linalg.det(jjt)
        if det_jjt < 0:
            return 0.0
        return math.sqrt(det_jjt)
    except:
        return 0.0


@st.cache_data(show_spinner="Generating workspace heatmap...")
def _generate_workspace_heatmap(num_samples: int = 10000) -> Dict[str, Any]:
    """Generate workspace heatmap data with reachability and manipulability analysis."""
    
    # Sample random joint configurations
    positions = []
    manipulabilities = []
    joint_configs = []
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    progress_bar = st.progress(0, text="Sampling workspace...")
    
    for i in range(num_samples):
        # Generate random joint angles within limits
        joint_angles = []
        for limits in JOINT_LIMITS:
            angle = np.random.uniform(limits[0], limits[1])
            joint_angles.append(angle)
        
        try:
            # Calculate forward kinematics
            position, _ = _forward_kinematics(joint_angles)
            
            # Calculate manipulability
            jacobian = _calculate_jacobian(joint_angles)
            manipulability = _calculate_manipulability(jacobian)
            
            positions.append(position)
            manipulabilities.append(manipulability)
            joint_configs.append(joint_angles)
            
        except:
            # Skip invalid configurations
            continue
        
        # Update progress
        if i % (num_samples // 20) == 0:
            progress_bar.progress((i + 1) / num_samples, text=f"Sampling workspace... {i+1}/{num_samples}")
    
    progress_bar.empty()
    
    positions = np.array(positions)
    manipulabilities = np.array(manipulabilities)
    
    return {
        'positions': positions,
        'manipulabilities': manipulabilities,
        'joint_configs': joint_configs,
        'num_samples': len(positions)
    }


def _create_workspace_heatmap_2d(workspace_data: Dict[str, Any], plane: str = 'xy') -> go.Figure:
    """Create 2D workspace heatmap for specified plane."""
    positions = workspace_data['positions']
    manipulabilities = workspace_data['manipulabilities']
    
    # Select coordinates based on plane
    if plane == 'xy':
        x, y = positions[:, 0], positions[:, 1]
        x_label, y_label = 'X (m)', 'Y (m)'
        title = 'XY Plane Workspace'
    elif plane == 'xz':
        x, y = positions[:, 0], positions[:, 2]
        x_label, y_label = 'X (m)', 'Z (m)'
        title = 'XZ Plane Workspace'
    else:  # yz plane
        x, y = positions[:, 1], positions[:, 2]
        x_label, y_label = 'Y (m)', 'Z (m)'
        title = 'YZ Plane Workspace'
    
    # Create density heatmap
    fig = go.Figure()
    
    # Add scatter plot with manipulability coloring
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(
            size=3,
            color=manipulabilities,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Manipulability Index"),
            opacity=0.6
        ),
        name='Reachable Points',
        hovertemplate=f'{x_label}: %{{x:.3f}}<br>{y_label}: %{{y:.3f}}<br>Manipulability: %{{marker.color:.3f}}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'{title} - Reachability & Manipulability',
        xaxis_title=x_label,
        yaxis_title=y_label,
        width=600,
        height=500,
        showlegend=True
    )
    
    return fig


def _create_workspace_heatmap_3d(workspace_data: Dict[str, Any]) -> go.Figure:
    """Create 3D workspace visualization."""
    positions = workspace_data['positions']
    manipulabilities = workspace_data['manipulabilities']
    
    fig = go.Figure(data=[go.Scatter3d(
        x=positions[:, 0],
        y=positions[:, 1],
        z=positions[:, 2],
        mode='markers',
        marker=dict(
            size=2,
            color=manipulabilities,
            colorscale='Plasma',
            showscale=True,
            colorbar=dict(title="Manipulability Index"),
            opacity=0.6
        ),
        hovertemplate='X: %{x:.3f}m<br>Y: %{y:.3f}m<br>Z: %{z:.3f}m<br>Manipulability: %{marker.color:.3f}<extra></extra>'
    )])
    
    fig.update_layout(
        title='3D Workspace - Reachability & Manipulability',
        scene=dict(
            xaxis_title='X (m)',
            yaxis_title='Y (m)',
            zaxis_title='Z (m)',
            aspectmode='data'
        ),
        width=700,
        height=600
    )
    
    return fig


def _analyze_workspace_statistics(workspace_data: Dict[str, Any]) -> Dict[str, float]:
    """Calculate workspace statistics for analysis."""
    positions = workspace_data['positions']
    manipulabilities = workspace_data['manipulabilities']
    
    # Calculate workspace volume (approximate using convex hull)
    try:
        from scipy.spatial import ConvexHull
        hull = ConvexHull(positions)
        volume = hull.volume
    except:
        volume = 0.0
    
    # Calculate reachability statistics
    max_reach = np.max(np.linalg.norm(positions, axis=1))
    min_reach = np.min(np.linalg.norm(positions, axis=1))
    avg_reach = np.mean(np.linalg.norm(positions, axis=1))
    
    # Calculate manipulability statistics
    max_manipulability = np.max(manipulabilities)
    min_manipulability = np.min(manipulabilities)
    avg_manipulability = np.mean(manipulabilities)
    
    # Calculate workspace dimensions
    x_range = np.max(positions[:, 0]) - np.min(positions[:, 0])
    y_range = np.max(positions[:, 1]) - np.min(positions[:, 1])
    z_range = np.max(positions[:, 2]) - np.min(positions[:, 2])
    
    return {
        'volume': volume,
        'max_reach': max_reach,
        'min_reach': min_reach,
        'avg_reach': avg_reach,
        'max_manipulability': max_manipulability,
        'min_manipulability': min_manipulability,
        'avg_manipulability': avg_manipulability,
        'x_range': x_range,
        'y_range': y_range,
        'z_range': z_range,
        'num_samples': workspace_data['num_samples']
    }


def _build_threejs_html(joint_angles: List[float]) -> str:
    base_url = "https://mr-iitkgp.vlabs.ac.in/exp/forward-kinematics/simulation"
    axis_js = _load_asset("js/axis.js")
    scene_js = _load_asset("js/PUMA_scene.js")
    angles_json = json.dumps(joint_angles)
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset=\"utf-8\" />
    <style>
        html, body {{ margin: 0; padding: 0; background: #000; }}
        #canvas3d-view {{ width: 100%; height: 720px; }}
    </style>
    <script src=\"{base_url}/js/threejs/three.min.js\"></script>
    <script src=\"{base_url}/js/threejs/TrackballControls.js\"></script>
    <script src=\"{base_url}/js/threejs/Detector.js\"></script>
    <script src=\"{base_url}/js/threejs/stats.min.js\"></script>
    <script src=\"{base_url}/fonts/gentilis_bold.typeface.js\"></script>
    <script src=\"{base_url}/fonts/gentilis_regular.typeface.js\"></script>
    <script src=\"{base_url}/fonts/optimer_bold.typeface.js\"></script>
    <script src=\"{base_url}/fonts/optimer_regular.typeface.js\"></script>
    <script src=\"{base_url}/fonts/helvetiker_bold.typeface.js\"></script>
    <script src=\"{base_url}/fonts/helvetiker_regular.typeface.js\"></script>
    <script src=\"{base_url}/fonts/droid_sans_regular.typeface.js\"></script>
    <script src=\"{base_url}/fonts/droid_sans_bold.typeface.js\"></script>
    <script src=\"{base_url}/fonts/droid_serif_regular.typeface.js\"></script>
    <script src=\"{base_url}/fonts/droid_serif_bold.typeface.js\"></script>
</head>
<body>
    <div id=\"canvas3d-view\"></div>
    <script>
    {axis_js}
    </script>
    <script>
    {scene_js}
    </script>
    <script>
    const JOINT_ANGLES = {angles_json};

    function degToRad(degrees) {{
        return degrees * Math.PI / 180;
    }}

    function applyJointAngles(angles) {{
        if (!window.PUMA560) {{
            return;
        }}
        PUMA560.link2Mesh.rotation.y = degToRad(angles[0] || 0);
        PUMA560.Link3Mesh.rotation.x = degToRad(angles[1] || 0);
        PUMA560.Link4Mesh.rotation.x = degToRad(angles[2] || 0);
        PUMA560.BoxL5.rotation.y = degToRad(angles[3] || 0);
        PUMA560.Cylinder3L5.rotation.x = degToRad(angles[4] || 0);
        PUMA560.CylinderL6.rotation.x = degToRad(angles[5] || 0);
        if (typeof render === 'function') {{
            render();
        }}
    }}

    window.addEventListener('load', () => {{
        if (typeof Detector !== 'undefined' && !Detector.webgl) {{
            document.body.innerHTML = '<p style="color:#fff;text-align:center;">WebGL is not supported in this browser.</p>';
            return;
        }}
        if (window.PUMA560 && typeof PUMA560.init === 'function') {{
            PUMA560.init();
            if (typeof animate === 'function') {{
                animate();
            }}
            applyJointAngles(JOINT_ANGLES);
        }}
    }});
    </script>
</body>
</html>"""


def render_app() -> None:
    st.title("PUMA 560 Virtual Robotic Arm")
    st.caption("Streamlit-driven controls linked to the IIT KGP Virtual Labs Three.js model.")

    # Initialize session state
    if 'prev_position' not in st.session_state:
        st.session_state.prev_position = np.zeros(3)
    if 'prev_time' not in st.session_state:
        st.session_state.prev_time = time.time()
    if 'prev_joint_angles' not in st.session_state:
        st.session_state.prev_joint_angles = [0.0] * 6
    if 'trajectory_data' not in st.session_state:
        st.session_state.trajectory_data = []
    if 'recording' not in st.session_state:
        st.session_state.recording = False
    if 'recording_start_time' not in st.session_state:
        st.session_state.recording_start_time = 0.0

    st.sidebar.header("Instructions")
    st.sidebar.markdown(
        """
        - Adjust the joint sliders to command the manipulator.
        - Use the mouse to orbit, pan, and zoom inside the Three.js canvas.
        - Refresh the page if the viewer does not appear immediately.
        """
    )

    # Recording controls
    st.subheader("📹 Trajectory Recording")
    rec_col1, rec_col2, rec_col3, rec_col4 = st.columns(4)
    
    with rec_col1:
        if st.button("🔴 Start Recording" if not st.session_state.recording else "⏹️ Stop Recording"):
            if not st.session_state.recording:
                st.session_state.recording = True
                st.session_state.recording_start_time = time.time()
                st.session_state.trajectory_data = []
                st.success("Recording started!")
            else:
                st.session_state.recording = False
                st.success(f"Recording stopped! Captured {len(st.session_state.trajectory_data)} data points.")
    
    with rec_col2:
        if st.button("🗑️ Clear Data"):
            st.session_state.trajectory_data = []
            st.success("Trajectory data cleared!")
    
    with rec_col3:
        if st.session_state.trajectory_data:
            csv_data = _export_trajectory_csv(st.session_state.trajectory_data)
            st.download_button(
                "📥 Download CSV",
                csv_data,
                "puma560_trajectory.csv",
                "text/csv"
            )
    
    with rec_col4:
        if st.session_state.recording:
            st.markdown("🔴 **RECORDING**")
        else:
            st.markdown(f"📊 **{len(st.session_state.trajectory_data)} points**")

    # Create main layout
    left_col, right_col = st.columns([1.2, 0.8])
    
    with left_col:
        st.subheader("Joint Controls")
        columns = st.columns(3)
        joint_angles: List[float] = []
        for idx, (label, limits) in enumerate(zip(JOINT_LABELS, JOINT_LIMITS)):
            column = columns[idx % 3]
            with column:
                angle = st.slider(
                    f"{label} (θ{idx + 1})",
                    min_value=limits[0],
                    max_value=limits[1],
                    value=0,
                    step=1,
                    key=f"joint_{idx}",
                )
                joint_angles.append(float(angle))

        components.html(_build_threejs_html(joint_angles), height=760, scrolling=False)

    with right_col:
        st.subheader("📊 End-Effector Analytics")
        
        # Calculate forward kinematics
        position, rotation = _forward_kinematics(joint_angles)
        roll, pitch, yaw = _rotation_to_euler(rotation)
        
        # Calculate velocities
        current_time = time.time()
        dt = current_time - st.session_state.prev_time
        velocity = _calculate_velocity(position, st.session_state.prev_position, dt)
        joint_velocities = _calculate_joint_velocities(joint_angles, st.session_state.prev_joint_angles, dt)
        
        # Calculate energy consumption
        energy = _estimate_energy_consumption(joint_velocities, joint_angles)
        
        # Record trajectory data if recording
        if st.session_state.recording and dt > 0:
            record_time = current_time - st.session_state.recording_start_time
            trajectory_point = {
                'time': record_time,
                'theta1': joint_angles[0],
                'theta2': joint_angles[1],
                'theta3': joint_angles[2],
                'theta4': joint_angles[3],
                'theta5': joint_angles[4],
                'theta6': joint_angles[5],
                'pos_x': position[0],
                'pos_y': position[1],
                'pos_z': position[2],
                'roll': roll,
                'pitch': pitch,
                'yaw': yaw,
                'velocity': velocity,
                'energy': energy,
                'joint_vel_1': joint_velocities[0],
                'joint_vel_2': joint_velocities[1],
                'joint_vel_3': joint_velocities[2],
                'joint_vel_4': joint_velocities[3],
                'joint_vel_5': joint_velocities[4],
                'joint_vel_6': joint_velocities[5]
            }
            st.session_state.trajectory_data.append(trajectory_point)
        
        # Update session state
        st.session_state.prev_position = position.copy()
        st.session_state.prev_joint_angles = joint_angles.copy()
        st.session_state.prev_time = current_time
        
        # Position metrics
        st.markdown("**🎯 Position (m)**")
        pos_cols = st.columns(3)
        with pos_cols[0]:
            st.metric("X", f"{position[0]:.3f}")
        with pos_cols[1]:
            st.metric("Y", f"{position[1]:.3f}")
        with pos_cols[2]:
            st.metric("Z", f"{position[2]:.3f}")
            
        # Distance from origin
        distance = np.linalg.norm(position)
        st.metric("Distance from Base", f"{distance:.3f} m")
        
        # Orientation metrics
        st.markdown("**🔄 Orientation (degrees)**")
        ori_cols = st.columns(3)
        with ori_cols[0]:
            st.metric("Roll", f"{roll:.1f}°")
        with ori_cols[1]:
            st.metric("Pitch", f"{pitch:.1f}°")
        with ori_cols[2]:
            st.metric("Yaw", f"{yaw:.1f}°")
            
        # Velocity and workspace analysis
        st.markdown("**⚡ Motion Analysis**")
        vel_cols = st.columns(2)
        with vel_cols[0]:
            st.metric("Linear Velocity", f"{velocity:.3f} m/s")
        with vel_cols[1]:
            st.metric("Energy Proxy", f"{energy:.1f}")
        
        # Workspace limits analysis
        workspace_utilization = (distance / 1.0) * 100  # Assuming ~1m max reach
        workspace_utilization = min(workspace_utilization, 100)
        
        st.metric("Workspace Utilization", f"{workspace_utilization:.1f}%")
        
        # Reachability indicator
        if distance > 0.9:
            st.warning("⚠️ Near workspace boundary")
        elif distance < 0.1:
            st.info("ℹ️ Close to base - limited mobility")
        else:
            st.success("✅ Good working position")
            
        # Joint configuration display
        st.markdown("**⚙️ Joint Configuration**")
        joint_data = {f"θ{i+1}": f"{angle}°" for i, angle in enumerate(joint_angles)}
        st.json(joint_data)

    # Trajectory Analysis Section
    if st.session_state.trajectory_data:
        st.subheader("📈 Trajectory Analysis")
        
        # Create DataFrame for analysis
        df = pd.DataFrame(st.session_state.trajectory_data)
        
        # Trajectory visualization tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Joint Angles", "End-Effector Path", "Velocities", "Energy Analysis"])
        
        with tab1:
            st.markdown("**Joint Angle Timeline**")
            fig_joints = go.Figure()
            
            for i in range(6):
                fig_joints.add_trace(go.Scatter(
                    x=df['time'],
                    y=df[f'theta{i+1}'],
                    mode='lines',
                    name=f'θ{i+1} ({JOINT_LABELS[i]})',
                    line=dict(width=2)
                ))
            
            fig_joints.update_layout(
                title="Joint Angles Over Time",
                xaxis_title="Time (s)",
                yaxis_title="Angle (degrees)",
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(fig_joints, use_container_width=True)
        
        with tab2:
            st.markdown("**End-Effector Position Timeline**")
            fig_pos = go.Figure()
            
            fig_pos.add_trace(go.Scatter(x=df['time'], y=df['pos_x'], mode='lines', name='X Position', line=dict(color='red')))
            fig_pos.add_trace(go.Scatter(x=df['time'], y=df['pos_y'], mode='lines', name='Y Position', line=dict(color='green')))
            fig_pos.add_trace(go.Scatter(x=df['time'], y=df['pos_z'], mode='lines', name='Z Position', line=dict(color='blue')))
            
            fig_pos.update_layout(
                title="End-Effector Position Over Time",
                xaxis_title="Time (s)",
                yaxis_title="Position (m)",
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(fig_pos, use_container_width=True)
            
            # 3D trajectory path
            st.markdown("**3D Trajectory Path**")
            fig_3d = go.Figure(data=[go.Scatter3d(
                x=df['pos_x'],
                y=df['pos_y'],
                z=df['pos_z'],
                mode='lines+markers',
                marker=dict(size=3, color=df['time'], colorscale='Viridis', showscale=True),
                line=dict(color='darkblue', width=4),
                name='End-Effector Path'
            )])
            
            fig_3d.update_layout(
                title="3D End-Effector Trajectory",
                scene=dict(
                    xaxis_title="X (m)",
                    yaxis_title="Y (m)",
                    zaxis_title="Z (m)"
                ),
                height=500
            )
            st.plotly_chart(fig_3d, use_container_width=True)
        
        with tab3:
            st.markdown("**Joint Velocities**")
            fig_vel = go.Figure()
            
            for i in range(6):
                fig_vel.add_trace(go.Scatter(
                    x=df['time'],
                    y=df[f'joint_vel_{i+1}'],
                    mode='lines',
                    name=f'θ{i+1} velocity',
                    line=dict(width=2)
                ))
            
            fig_vel.update_layout(
                title="Joint Angular Velocities",
                xaxis_title="Time (s)",
                yaxis_title="Angular Velocity (deg/s)",
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(fig_vel, use_container_width=True)
            
            # Linear velocity
            fig_lin_vel = go.Figure()
            fig_lin_vel.add_trace(go.Scatter(
                x=df['time'],
                y=df['velocity'],
                mode='lines',
                name='Linear Velocity',
                line=dict(color='purple', width=3)
            ))
            
            fig_lin_vel.update_layout(
                title="End-Effector Linear Velocity",
                xaxis_title="Time (s)",
                yaxis_title="Velocity (m/s)",
                height=300
            )
            st.plotly_chart(fig_lin_vel, use_container_width=True)
        
        with tab4:
            st.markdown("**Energy Consumption Analysis**")
            fig_energy = go.Figure()
            fig_energy.add_trace(go.Scatter(
                x=df['time'],
                y=df['energy'],
                mode='lines',
                name='Energy Proxy',
                line=dict(color='orange', width=3),
                fill='tonexty'
            ))
            
            fig_energy.update_layout(
                title="Estimated Energy Consumption",
                xaxis_title="Time (s)",
                yaxis_title="Energy Proxy (arbitrary units)",
                height=400
            )
            st.plotly_chart(fig_energy, use_container_width=True)
            
            # Energy statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Energy", f"{df['energy'].sum():.1f}")
            with col2:
                st.metric("Average Power", f"{df['energy'].mean():.2f}")
            with col3:
                st.metric("Peak Power", f"{df['energy'].max():.2f}")

    # Workspace Analysis Section
    st.subheader("🗺️ Workspace Analysis & Heatmaps")
    
    # Workspace analysis controls
    ws_col1, ws_col2, ws_col3 = st.columns(3)
    
    with ws_col1:
        sample_size = st.selectbox(
            "Sample Size",
            [1000, 5000, 10000, 20000],
            index=1,
            help="Number of random configurations to sample"
        )
    
    with ws_col2:
        if st.button("🔄 Generate Workspace Analysis"):
            st.session_state.workspace_data = _generate_workspace_heatmap(sample_size)
            st.success(f"Generated workspace with {st.session_state.workspace_data['num_samples']} valid samples!")
    
    with ws_col3:
        if 'workspace_data' in st.session_state:
            st.metric("Valid Samples", f"{st.session_state.workspace_data['num_samples']}")
    
    # Display workspace analysis if available
    if 'workspace_data' in st.session_state:
        workspace_data = st.session_state.workspace_data
        
        # Workspace visualization tabs
        ws_tab1, ws_tab2, ws_tab3, ws_tab4 = st.tabs(["2D Heatmaps", "3D Workspace", "Statistics", "Export"])
        
        with ws_tab1:
            st.markdown("**2D Workspace Projections with Manipulability Analysis**")
            
            # Create 2D projections
            col1, col2 = st.columns(2)
            
            with col1:
                fig_xy = _create_workspace_heatmap_2d(workspace_data, 'xy')
                st.plotly_chart(fig_xy, use_container_width=True)
                
                fig_xz = _create_workspace_heatmap_2d(workspace_data, 'xz')
                st.plotly_chart(fig_xz, use_container_width=True)
            
            with col2:
                fig_yz = _create_workspace_heatmap_2d(workspace_data, 'yz')
                st.plotly_chart(fig_yz, use_container_width=True)
                
                # Current position overlay
                current_pos, _ = _forward_kinematics(joint_angles)
                current_jacobian = _calculate_jacobian(joint_angles)
                current_manipulability = _calculate_manipulability(current_jacobian)
                
                st.markdown("**Current Configuration Analysis**")
                st.metric("Current Manipulability", f"{current_manipulability:.3f}")
                
                if current_manipulability < 0.001:
                    st.warning("⚠️ Near singularity - Low manipulability!")
                elif current_manipulability > 0.1:
                    st.success("✅ Good manipulability")
                else:
                    st.info("ℹ️ Moderate manipulability")
        
        with ws_tab2:
            st.markdown("**3D Workspace Visualization**")
            fig_3d_workspace = _create_workspace_heatmap_3d(workspace_data)
            st.plotly_chart(fig_3d_workspace, use_container_width=True)
            
            st.markdown("**Interpretation Guide:**")
            st.markdown("""
            - **Color Scale**: Represents manipulability index (darker = lower manipulability)
            - **Point Density**: Shows reachable workspace regions
            - **Sparse Regions**: Areas with limited reachability or high singularity risk
            - **Dense Regions**: Optimal working areas with good manipulability
            """)
        
        with ws_tab3:
            st.markdown("**Workspace Statistics & Analysis**")
            stats = _analyze_workspace_statistics(workspace_data)
            
            # Reachability statistics
            st.markdown("**🎯 Reachability Analysis**")
            reach_col1, reach_col2, reach_col3 = st.columns(3)
            with reach_col1:
                st.metric("Max Reach", f"{stats['max_reach']:.3f} m")
            with reach_col2:
                st.metric("Min Reach", f"{stats['min_reach']:.3f} m")
            with reach_col3:
                st.metric("Avg Reach", f"{stats['avg_reach']:.3f} m")
            
            # Manipulability statistics
            st.markdown("**🔧 Manipulability Analysis**")
            manip_col1, manip_col2, manip_col3 = st.columns(3)
            with manip_col1:
                st.metric("Max Manipulability", f"{stats['max_manipulability']:.3f}")
            with manip_col2:
                st.metric("Min Manipulability", f"{stats['min_manipulability']:.3f}")
            with manip_col3:
                st.metric("Avg Manipulability", f"{stats['avg_manipulability']:.3f}")
            
            # Workspace dimensions
            st.markdown("**📏 Workspace Dimensions**")
            dim_col1, dim_col2, dim_col3 = st.columns(3)
            with dim_col1:
                st.metric("X Range", f"{stats['x_range']:.3f} m")
            with dim_col2:
                st.metric("Y Range", f"{stats['y_range']:.3f} m")
            with dim_col3:
                st.metric("Z Range", f"{stats['z_range']:.3f} m")
            
            # Workspace volume (if available)
            if stats['volume'] > 0:
                st.metric("Approx. Workspace Volume", f"{stats['volume']:.3f} m³")
            
        with ws_tab4:
            st.markdown("**Export Workspace Data**")
            
            if st.button("📊 Export Workspace CSV"):
                # Create workspace DataFrame
                positions = workspace_data['positions']
                manipulabilities = workspace_data['manipulabilities']
                joint_configs = workspace_data['joint_configs']
                
                workspace_df_data = []
                for i, (pos, manip, joints) in enumerate(zip(positions, manipulabilities, joint_configs)):
                    row = {
                        'sample_id': i,
                        'pos_x': pos[0],
                        'pos_y': pos[1],
                        'pos_z': pos[2],
                        'manipulability': manip,
                        'reach_distance': np.linalg.norm(pos)
                    }
                    # Add joint angles
                    for j, angle in enumerate(joints):
                        row[f'theta_{j+1}'] = angle
                    workspace_df_data.append(row)
                
                workspace_df = pd.DataFrame(workspace_df_data)
                csv_workspace = workspace_df.to_csv(index=False)
                
                st.download_button(
                    "📥 Download Workspace Data CSV",
                    csv_workspace,
                    "puma560_workspace_analysis.csv",
                    "text/csv"
                )
                
                st.success(f"Workspace data ready for download ({len(workspace_df_data)} samples)")
            
            st.markdown("**Usage for Lab Reports:**")
            st.markdown("""
            - **Workspace Analysis**: Use heatmaps to show reachable regions
            - **Singularity Study**: Identify low-manipulability areas
            - **Design Optimization**: Compare different robot configurations
            - **Path Planning**: Avoid low-manipulability regions
            - **Performance Metrics**: Quantify workspace capabilities
            """)
    
    else:
        st.info("Click 'Generate Workspace Analysis' to create workspace heatmaps and manipulability analysis.")

    st.sidebar.markdown("---")
    st.sidebar.json({f"θ{idx + 1}": angle for idx, angle in enumerate(joint_angles)})


if __name__ == "__main__":
    render_app()
