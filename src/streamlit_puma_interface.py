"""Streamlit UI embedding the IIT KGP PUMA 560 Three.js model with Streamlit controls."""
from __future__ import annotations

from typing import Any, Dict, List
import logging
import time

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from app.assets import build_threejs_html
from app.constants import JOINT_LABELS, JOINT_LIMITS
from app.kinematics import (
    calculate_jacobian,
    calculate_manipulability,
    calculate_velocity,
    forward_kinematics,
    rotation_to_euler,
)
from app.logging_utils import configure_logging, get_logger
from app.trajectory import (
    calculate_joint_velocities,
    create_trajectory_data_point,
    estimate_energy_consumption,
    export_trajectory_csv,
)
from app.workspace import (
    analyze_workspace_statistics,
    create_workspace_heatmap_2d,
    create_workspace_heatmap_3d,
    generate_workspace_heatmap,
)

st.set_page_config(
    page_title="PUMA 560 Digital Twin",
    page_icon="P560",
    layout="wide",
    initial_sidebar_state="collapsed",
)


configure_logging("streamlit_app")
LOGGER = get_logger(__name__)



def _initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    LOGGER.debug("Initializing session state")
    session_defaults = {
        'prev_position': np.zeros(3),
        'prev_time': time.time(),
        'prev_joint_angles': [0.0] * 6,
        'trajectory_data': [],
        'recording': False,
        'recording_start_time': 0.0
    }
    
    for key, default_value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

    for joint_index in range(6):
        joint_key = f"joint_{joint_index}"
        if joint_key not in st.session_state:
            st.session_state[joint_key] = 0


def _inject_performance_hints() -> None:
    """Inject preconnect hints and layout-stabilizing CSS."""
    if st.session_state.get("_perf_hints_injected"):
        return

    st.session_state["_perf_hints_injected"] = True
    LOGGER.debug("Injecting performance hints")
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <style>
            body, button, input, textarea {
                font-family: "Segoe UI", "Roboto", "Helvetica Neue", Arial, sans-serif !important;
            }
            [data-testid="stAppViewContainer"] > .main {
                padding-top: 1rem;
            }
            [data-testid="stHeader"] {
                height: 4.5rem;
                padding: 0 1.5rem;
            }
            [data-testid="stHeader"] h1 {
                line-height: 3.5rem;
            }
            div[data-testid="stVerticalBlock"] {
                min-height: 3rem;
            }
            div[data-testid="column"] > div:first-child {
                min-height: 760px;
            }
            .joint-layout-placeholder {
                min-height: 760px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_performance_status(start_time: float) -> None:
    """Render performance optimization status."""
    render_time = (time.time() - start_time) * 1000
    LOGGER.info("Render cycle completed in %.1f ms", render_time)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.success(f"Performance Optimized | Render: {render_time:.1f}ms")
    with col2:
        st.info("Lazy Loading Enabled")
    with col3:
        st.info("Cached Assets Active")

def _render_header_and_sidebar() -> None:
    """Render application header and sidebar information."""
    # Header with navigation
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("PUMA 560 Digital Twin - IIT KGP Virtual Labs Integration")
        st.markdown("*Professional-grade robotic simulation with real-time kinematics*")
    with col2:
        if st.button("Reset Robot"):
            LOGGER.info("Reset robot requested")
            for i in range(6):
                st.session_state[f"joint_{i}"] = 0
            st.rerun()


def _render_recording_controls() -> None:
    """Render trajectory recording control buttons."""
    st.header("Trajectory Recording")
    rec_col1, rec_col2, rec_col3, rec_col4 = st.columns(4)
    
    with rec_col1:
        if st.button("Start Recording" if not st.session_state.recording else "Stop Recording"):
            if not st.session_state.recording:
                LOGGER.info("Trajectory recording started")
                st.session_state.recording = True
                st.session_state.recording_start_time = time.time()
                st.session_state.trajectory_data = []
                st.success("Recording started!")
            else:
                LOGGER.info(
                    "Trajectory recording stopped with %s points",
                    len(st.session_state.trajectory_data),
                )
                st.session_state.recording = False
                st.success(f"Recording stopped! Captured {len(st.session_state.trajectory_data)} data points.")
    
    with rec_col2:
        if st.button("Clear Data"):
            LOGGER.info("Trajectory data cleared")
            st.session_state.trajectory_data = []
            st.success("Trajectory data cleared!")
    
    with rec_col3:
        if st.session_state.trajectory_data:
            csv_data = export_trajectory_csv(st.session_state.trajectory_data)
            LOGGER.debug(
                "Providing trajectory CSV download (%s rows)",
                len(st.session_state.trajectory_data),
            )
            st.download_button(
                "Download CSV",
                csv_data,
                "puma560_trajectory.csv",
                "text/csv"
            )
    
    with rec_col4:
        if st.session_state.recording:
            st.markdown("**RECORDING ACTIVE**")
        else:
            st.markdown(f"**Data Points: {len(st.session_state.trajectory_data)}**")


def _render_joint_controls() -> List[float]:
    """Render joint control sliders and return current joint angles."""
    st.header("Joint Controls")
    columns = st.columns(3)
    joint_angles = []
    
    for idx, (label, limits) in enumerate(zip(JOINT_LABELS, JOINT_LIMITS)):
        column = columns[idx % 3]
        with column:
            default_angle = int(st.session_state.get(f"joint_{idx}", 0))
            angle = st.slider(
                f"{label} (θ{idx + 1})",
                min_value=limits[0],
                max_value=limits[1],
                value=default_angle,
                step=1,
                key=f"joint_{idx}",
            )
            joint_angles.append(float(angle))
    
    LOGGER.debug("Joint angles updated: %s", joint_angles)
    return joint_angles


def _render_analytics_panel(joint_angles: List[float]) -> None:
    """Render the end-effector analytics panel."""
    st.header("End-Effector Analytics")
    
    # Performance optimization: Only compute analytics if expanded
    with st.expander("View Analytics", expanded=True):
        try:
            position, rotation = forward_kinematics(joint_angles)
            roll, pitch, yaw = rotation_to_euler(rotation)

            current_time = time.time()
            dt = current_time - st.session_state.prev_time
            velocity = calculate_velocity(position, st.session_state.prev_position, dt)
            joint_velocities = calculate_joint_velocities(
                joint_angles, st.session_state.prev_joint_angles, dt
            )
            energy = estimate_energy_consumption(joint_velocities, joint_angles)

            if st.session_state.recording and dt > 0:
                robot_state = {
                    'joint_angles': joint_angles,
                    'position': position,
                    'orientation': (roll, pitch, yaw),
                    'velocity': velocity,
                    'energy': energy,
                    'joint_velocities': joint_velocities,
                    'elapsed_time': current_time - st.session_state.recording_start_time,
                }
                trajectory_data = create_trajectory_data_point(robot_state)
                _record_trajectory_point_if_needed(trajectory_data)

            st.session_state.prev_position = position.copy()
            st.session_state.prev_joint_angles = joint_angles.copy()
            st.session_state.prev_time = current_time

            _display_position_metrics(position)
            _display_orientation_metrics(roll, pitch, yaw)
            _display_motion_metrics(velocity, energy, position)
            _display_joint_configuration(joint_angles)
            LOGGER.debug(
                "Analytics updated | position=%s velocity=%.3f energy=%.3f",
                position,
                velocity,
                energy,
            )
        except Exception as error:
            LOGGER.exception("Failed to compute analytics")
            st.error(f"Analytics unavailable: {error}")

def _record_trajectory_point_if_needed(trajectory_data: Dict[str, float]) -> None:
    """Record trajectory data point if recording is active."""
    if st.session_state.recording:
        st.session_state.trajectory_data.append(trajectory_data)


def _display_position_metrics(position: np.ndarray) -> None:
    """Display position metrics in the analytics panel."""
    st.markdown("**Position (meters)**")
    pos_cols = st.columns(3)
    with pos_cols[0]:
        st.metric("X", f"{position[0]:.3f}")
    with pos_cols[1]:
        st.metric("Y", f"{position[1]:.3f}")
    with pos_cols[2]:
        st.metric("Z", f"{position[2]:.3f}")
        
    distance = np.linalg.norm(position)
    st.metric("Distance from Base", f"{distance:.3f} m")


def _display_orientation_metrics(roll: float, pitch: float, yaw: float) -> None:
    """Display orientation metrics in the analytics panel."""
    st.markdown("**Orientation (degrees)**")
    ori_cols = st.columns(3)
    with ori_cols[0]:
        st.metric("Roll", f"{roll:.1f}°")
    with ori_cols[1]:
        st.metric("Pitch", f"{pitch:.1f}°")
    with ori_cols[2]:
        st.metric("Yaw", f"{yaw:.1f}°")


def _display_motion_metrics(velocity: float, energy: float, position: np.ndarray) -> None:
    """Display motion analysis metrics."""
    st.markdown("**Motion Analysis**")
    vel_cols = st.columns(2)
    with vel_cols[0]:
        st.metric("Linear Velocity", f"{velocity:.3f} m/s")
    with vel_cols[1]:
        st.metric("Energy Proxy", f"{energy:.1f}")
    
    # Workspace utilization and status
    distance = np.linalg.norm(position)
    workspace_utilization = min((distance / 1.0) * 100, 100)
    st.metric("Workspace Utilization", f"{workspace_utilization:.1f}%")
    
    if distance > 0.9:
        st.warning("WARNING: Near workspace boundary")
    elif distance < 0.1:
        st.info("INFO: Close to base - limited mobility")
    else:
        st.success("STATUS: Good working position")


def _display_joint_configuration(joint_angles: List[float]) -> None:
    """Display current joint configuration."""
    st.markdown("**Joint Configuration**")
    joint_data = {f"θ{i+1}": f"{angle}°" for i, angle in enumerate(joint_angles)}
    st.json(joint_data)


def _render_main_interface() -> List[float]:
    """Render the main robot interface and return joint angles."""
    # Create main layout
    left_col, right_col = st.columns([1.2, 0.8])
    
    with left_col:
        joint_angles = _render_joint_controls()
        components.html(build_threejs_html(tuple(joint_angles)), height=760, scrolling=False)

    with right_col:
        _render_analytics_panel(joint_angles)
    
    return joint_angles


def _render_sidebar_summary(joint_angles: List[float]) -> None:
    """Render sidebar joint summary."""
    st.sidebar.markdown("---")
    st.sidebar.json({f"θ{idx + 1}": angle for idx, angle in enumerate(joint_angles)})


def render_app() -> None:
    """Main application rendering function with performance optimizations."""
    # Performance tracking
    start_time = time.time()
    
    # Initialize application state
    _initialize_session_state()
    _inject_performance_hints()
    _render_header_and_sidebar()
    _render_performance_status(start_time)
    _render_recording_controls()

    # Render main interface
    joint_angles = _render_main_interface()

    # Render additional sections
    _render_trajectory_analysis()
    _render_workspace_analysis(joint_angles)
    _render_sidebar_summary(joint_angles)

def _render_trajectory_analysis() -> None:
    """Render trajectory analysis section with charts and metrics."""
    if not st.session_state.trajectory_data:
        return
        
    st.header("Trajectory Analysis")
    df = pd.DataFrame(st.session_state.trajectory_data)
    
    # Trajectory visualization tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Joint Angles", "End-Effector Path", "Velocities", "Energy Analysis"])
    
    with tab1:
        _render_joint_angles_chart(df)
    
    with tab2:
        _render_end_effector_path_charts(df)
    
    with tab3:
        _render_velocity_charts(df)
    
    with tab4:
        _render_energy_analysis_chart(df)


def _render_joint_angles_chart(df: pd.DataFrame) -> None:
    """Render joint angles timeline chart."""
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


def _render_end_effector_path_charts(df: pd.DataFrame) -> None:
    """Render end-effector position and 3D path charts."""
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
        x=df['pos_x'], y=df['pos_y'], z=df['pos_z'],
        mode='lines+markers',
        marker=dict(size=3, color=df['time'], colorscale='Viridis', showscale=True),
        line=dict(color='darkblue', width=4),
        name='End-Effector Path'
    )])
    
    fig_3d.update_layout(
        title="3D End-Effector Trajectory",
        scene=dict(xaxis_title="X (m)", yaxis_title="Y (m)", zaxis_title="Z (m)"),
        height=500
    )
    st.plotly_chart(fig_3d, use_container_width=True)


def _render_velocity_charts(df: pd.DataFrame) -> None:
    """Render joint and linear velocity charts."""
    st.markdown("**Joint Velocities**")
    fig_vel = go.Figure()
    
    for i in range(6):
        fig_vel.add_trace(go.Scatter(
            x=df['time'], y=df[f'joint_vel_{i+1}'],
            mode='lines', name=f'θ{i+1} velocity', line=dict(width=2)
        ))
    
    fig_vel.update_layout(
        title="Joint Angular Velocities",
        xaxis_title="Time (s)", yaxis_title="Angular Velocity (deg/s)",
        height=400, hovermode='x unified'
    )
    st.plotly_chart(fig_vel, use_container_width=True)
    
    # Linear velocity
    fig_lin_vel = go.Figure()
    fig_lin_vel.add_trace(go.Scatter(
        x=df['time'], y=df['velocity'],
        mode='lines', name='Linear Velocity',
        line=dict(color='purple', width=3)
    ))
    
    fig_lin_vel.update_layout(
        title="End-Effector Linear Velocity",
        xaxis_title="Time (s)", yaxis_title="Velocity (m/s)",
        height=300
    )
    st.plotly_chart(fig_lin_vel, use_container_width=True)


def _render_energy_analysis_chart(df: pd.DataFrame) -> None:
    """Render energy consumption analysis."""
    st.markdown("**Energy Consumption Analysis**")
    fig_energy = go.Figure()
    fig_energy.add_trace(go.Scatter(
        x=df['time'], y=df['energy'],
        mode='lines', name='Energy Proxy',
        line=dict(color='orange', width=3), fill='tonexty'
    ))
    
    fig_energy.update_layout(
        title="Estimated Energy Consumption",
        xaxis_title="Time (s)", yaxis_title="Energy Proxy (arbitrary units)",
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
def _render_workspace_analysis(joint_angles: List[float]) -> None:
    """Render workspace analysis section with heatmaps and statistics."""
    st.header("Workspace Analysis & Heatmaps")
    
    # Workspace analysis controls
    ws_col1, ws_col2, ws_col3 = st.columns(3)
    
    with ws_col1:
        sample_size = st.selectbox(
            "Sample Size", [1000, 5000, 10000, 20000], index=1,
            help="Number of random configurations to sample"
        )
    
    with ws_col2:
        if st.button("Generate Workspace Analysis"):
            st.session_state.workspace_data = generate_workspace_heatmap(sample_size)
            st.success(f"Generated workspace with {st.session_state.workspace_data['num_samples']} valid samples!")
    
    with ws_col3:
        if 'workspace_data' in st.session_state:
            st.metric("Valid Samples", f"{st.session_state.workspace_data['num_samples']}")
    
    # Display workspace analysis if available
    if 'workspace_data' in st.session_state:
        _render_workspace_tabs(st.session_state.workspace_data, joint_angles)
    else:
        st.info("Click 'Generate Workspace Analysis' to create workspace heatmaps and manipulability analysis.")


def _render_workspace_tabs(workspace_data: Dict[str, Any], joint_angles: List[float]) -> None:
    """Render workspace analysis tabs."""
    ws_tab1, ws_tab2, ws_tab3, ws_tab4 = st.tabs(["2D Heatmaps", "3D Workspace", "Statistics", "Export"])
    
    with ws_tab1:
        _render_2d_heatmaps(workspace_data, joint_angles)
    
    with ws_tab2:
        _render_3d_workspace(workspace_data)
    
    with ws_tab3:
        _render_workspace_statistics(workspace_data)
    
    with ws_tab4:
        _render_workspace_export(workspace_data)


def _render_2d_heatmaps(workspace_data: Dict[str, Any], joint_angles: List[float]) -> None:
    """Render 2D workspace heatmaps and current configuration analysis."""
    st.markdown("**2D Workspace Projections with Manipulability Analysis**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_xy = create_workspace_heatmap_2d(workspace_data, 'xy')
        st.plotly_chart(fig_xy, use_container_width=True)
        
        fig_xz = create_workspace_heatmap_2d(workspace_data, 'xz')
        st.plotly_chart(fig_xz, use_container_width=True)
    
    with col2:
        fig_yz = create_workspace_heatmap_2d(workspace_data, 'yz')
        st.plotly_chart(fig_yz, use_container_width=True)
        
        # Current position analysis
        current_pos, _ = forward_kinematics(joint_angles)
        current_jacobian = calculate_jacobian(joint_angles)
        current_manipulability = calculate_manipulability(current_jacobian)
        
        st.markdown("**Current Configuration Analysis**")
        st.metric("Current Manipulability", f"{current_manipulability:.3f}")
        
        if current_manipulability < 0.001:
            st.warning("WARNING: Near singularity - Low manipulability!")
        elif current_manipulability > 0.1:
            st.success("STATUS: Good manipulability")
        else:
            st.info("INFO: Moderate manipulability")


def _render_3d_workspace(workspace_data: Dict[str, Any]) -> None:
    """Render 3D workspace visualization."""
    st.markdown("**3D Workspace Visualization**")
    fig_3d_workspace = create_workspace_heatmap_3d(workspace_data)
    st.plotly_chart(fig_3d_workspace, use_container_width=True)
    
    st.markdown("**Interpretation Guide:**")
    st.markdown("""
    - **Color Scale**: Represents manipulability index (darker = lower manipulability)
    - **Point Density**: Shows reachable workspace regions
    - **Sparse Regions**: Areas with limited reachability or high singularity risk
    - **Dense Regions**: Optimal working areas with good manipulability
    """)


def _render_workspace_statistics(workspace_data: Dict[str, Any]) -> None:
    """Render workspace statistics and analysis."""
    st.markdown("**Workspace Statistics and Analysis**")
    stats = analyze_workspace_statistics(workspace_data)
    
    # Reachability statistics
    st.markdown("**Reachability Analysis**")
    reach_col1, reach_col2, reach_col3 = st.columns(3)
    with reach_col1:
        st.metric("Max Reach", f"{stats['max_reach']:.3f} m")
    with reach_col2:
        st.metric("Min Reach", f"{stats['min_reach']:.3f} m")
    with reach_col3:
        st.metric("Avg Reach", f"{stats['avg_reach']:.3f} m")
    
    # Manipulability statistics
    st.markdown("**Manipulability Analysis**")
    manip_col1, manip_col2, manip_col3 = st.columns(3)
    with manip_col1:
        st.metric("Max Manipulability", f"{stats['max_manipulability']:.3f}")
    with manip_col2:
        st.metric("Min Manipulability", f"{stats['min_manipulability']:.3f}")
    with manip_col3:
        st.metric("Avg Manipulability", f"{stats['avg_manipulability']:.3f}")
    
    # Workspace dimensions
    st.markdown("**Workspace Dimensions**")
    dim_col1, dim_col2, dim_col3 = st.columns(3)
    with dim_col1:
        st.metric("X Range", f"{stats['x_range']:.3f} m")
    with dim_col2:
        st.metric("Y Range", f"{stats['y_range']:.3f} m")
    with dim_col3:
        st.metric("Z Range", f"{stats['z_range']:.3f} m")
    
    # Workspace volume
    if stats['volume'] > 0:
        st.metric("Approx. Workspace Volume", f"{stats['volume']:.3f} m³")


def _render_workspace_export(workspace_data: Dict[str, Any]) -> None:
    """Render workspace data export section."""
    st.markdown("**Export Workspace Data**")
    
    if st.button("Export Workspace CSV"):
        positions = workspace_data['positions']
        manipulabilities = workspace_data['manipulabilities']
        joint_configs = workspace_data['joint_configs']
        
        workspace_df_data = []
        for i, (pos, manip, joints) in enumerate(zip(positions, manipulabilities, joint_configs)):
            row = {
                'sample_id': i, 'pos_x': pos[0], 'pos_y': pos[1], 'pos_z': pos[2],
                'manipulability': manip, 'reach_distance': np.linalg.norm(pos)
            }
            # Add joint angles
            for j, angle in enumerate(joints):
                row[f'theta_{j+1}'] = angle
            workspace_df_data.append(row)
        
        workspace_df = pd.DataFrame(workspace_df_data)
        csv_workspace = workspace_df.to_csv(index=False)
        
        st.download_button(
            "Download Workspace Data CSV", csv_workspace,
            "puma560_workspace_analysis.csv", "text/csv"
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


if __name__ == "__main__":
    render_app()
