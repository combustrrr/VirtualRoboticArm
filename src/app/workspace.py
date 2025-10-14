"""Workspace analysis helpers."""
from __future__ import annotations

import random
from typing import Any, Dict

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from .constants import JOINT_LIMITS
from .kinematics import calculate_jacobian, calculate_manipulability, forward_kinematics


@st.cache_data(show_spinner="Generating workspace heatmap...")
def generate_workspace_heatmap(num_samples: int = 10000) -> Dict[str, Any]:
    """Sample the workspace to build reachability and manipulability datasets."""
    positions = []
    manipulabilities = []
    joint_configs = []

    np.random.seed(42)
    random.seed(42)

    progress_bar = st.progress(0, text="Sampling workspace...")

    for index in range(num_samples):
        joint_angles = [float(np.random.uniform(limits[0], limits[1])) for limits in JOINT_LIMITS]

        try:
            position, _ = forward_kinematics(joint_angles)
            jacobian = calculate_jacobian(joint_angles)
            manipulability = calculate_manipulability(jacobian)
        except Exception:
            continue

        positions.append(position)
        manipulabilities.append(manipulability)
        joint_configs.append(joint_angles)

        if index % max(1, (num_samples // 20)) == 0:
            progress_bar.progress((index + 1) / num_samples, text=f"Sampling workspace... {index + 1}/{num_samples}")

    progress_bar.empty()

    positions_array = np.array(positions)
    manipulability_array = np.array(manipulabilities)

    return {
        "positions": positions_array,
        "manipulabilities": manipulability_array,
        "joint_configs": joint_configs,
        "num_samples": len(positions_array),
    }


def create_workspace_heatmap_2d(workspace_data: Dict[str, Any], plane: str = "xy") -> go.Figure:
    """Build a 2D scatter heatmap for the requested plane."""
    positions = workspace_data["positions"]
    manipulabilities = workspace_data["manipulabilities"]

    if plane == "xy":
        x, y = positions[:, 0], positions[:, 1]
        x_label, y_label, title = "X (m)", "Y (m)", "XY Plane Workspace"
    elif plane == "xz":
        x, y = positions[:, 0], positions[:, 2]
        x_label, y_label, title = "X (m)", "Z (m)", "XZ Plane Workspace"
    else:
        x, y = positions[:, 1], positions[:, 2]
        x_label, y_label, title = "Y (m)", "Z (m)", "YZ Plane Workspace"

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=dict(
                size=3,
                color=manipulabilities,
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Manipulability Index"),
                opacity=0.6,
            ),
            name="Reachable Points",
            hovertemplate=f"{x_label}: %{{x:.3f}}<br>{y_label}: %{{y:.3f}}<br>Manipulability: %{{marker.color:.3f}}<extra></extra>",
        )
    )

    figure.update_layout(
        title=f"{title} - Reachability and Manipulability",
        xaxis_title=x_label,
        yaxis_title=y_label,
        width=600,
        height=500,
        showlegend=True,
    )

    return figure


def create_workspace_heatmap_3d(workspace_data: Dict[str, Any]) -> go.Figure:
    """Construct a 3D scatter plot showing the sampled workspace."""
    positions = workspace_data["positions"]
    manipulabilities = workspace_data["manipulabilities"]

    figure = go.Figure(
        data=[
            go.Scatter3d(
                x=positions[:, 0],
                y=positions[:, 1],
                z=positions[:, 2],
                mode="markers",
                marker=dict(
                    size=2,
                    color=manipulabilities,
                    colorscale="Plasma",
                    showscale=True,
                    colorbar=dict(title="Manipulability Index"),
                    opacity=0.6,
                ),
                hovertemplate="X: %{x:.3f}m<br>Y: %{y:.3f}m<br>Z: %{z:.3f}m<br>Manipulability: %{marker.color:.3f}<extra></extra>",
            )
        ]
    )

    figure.update_layout(
        title="3D Workspace - Reachability and Manipulability",
        scene=dict(
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Z (m)",
            aspectmode="data",
        ),
        width=700,
        height=600,
    )

    return figure


def analyze_workspace_statistics(workspace_data: Dict[str, Any]) -> Dict[str, float]:
    """Compute workspace reach and manipulability statistics."""
    positions = workspace_data["positions"]
    manipulabilities = workspace_data["manipulabilities"]

    try:
        from scipy.spatial import ConvexHull

        hull = ConvexHull(positions)
        volume = float(hull.volume)
    except Exception:
        volume = 0.0

    reach = np.linalg.norm(positions, axis=1)
    x_range = float(np.max(positions[:, 0]) - np.min(positions[:, 0]))
    y_range = float(np.max(positions[:, 1]) - np.min(positions[:, 1]))
    z_range = float(np.max(positions[:, 2]) - np.min(positions[:, 2]))

    return {
        "volume": volume,
        "max_reach": float(np.max(reach)),
        "min_reach": float(np.min(reach)),
        "avg_reach": float(np.mean(reach)),
        "max_manipulability": float(np.max(manipulabilities)),
        "min_manipulability": float(np.min(manipulabilities)),
        "avg_manipulability": float(np.mean(manipulabilities)),
        "x_range": x_range,
        "y_range": y_range,
        "z_range": z_range,
        "num_samples": int(workspace_data["num_samples"]),
    }
