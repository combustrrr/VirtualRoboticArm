"""Trajectory analytics helpers."""
from __future__ import annotations

import csv
import math
from io import StringIO
from typing import Any, Dict, List


def calculate_joint_velocities(current_angles: List[float], previous_angles: List[float], dt: float) -> List[float]:
    """Return joint angular velocities in degrees per second."""
    if dt <= 0:
        return [0.0] * len(current_angles)
    return [(curr - prev) / dt for curr, prev in zip(current_angles, previous_angles)]


def estimate_energy_consumption(joint_velocities: List[float], joint_angles: List[float]) -> float:
    """Estimate relative energy consumption using a simple weighted velocity proxy."""
    energy = 0.0
    joint_weights = [1.0, 1.2, 1.0, 0.8, 0.6, 0.4]

    for index, (velocity, angle, weight) in enumerate(zip(joint_velocities, joint_angles, joint_weights)):
        gravity_factor = abs(math.cos(math.radians(angle))) if index < 3 else 1.0
        energy += weight * (velocity ** 2) * gravity_factor

    return energy


def export_trajectory_csv(trajectory: List[Dict[str, Any]]) -> str:
    """Serialize collected trajectory data to CSV."""
    if not trajectory:
        return ""

    buffer = StringIO()
    fieldnames = list(trajectory[0].keys())
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(trajectory)
    return buffer.getvalue()


def create_trajectory_data_point(robot_state: Dict[str, Any]) -> Dict[str, float]:
    """Flatten the robot state snapshot into a trajectory record."""
    joints = robot_state["joint_angles"]
    position = robot_state["position"]
    orientation = robot_state["orientation"]
    joint_velocities = robot_state["joint_velocities"]

    data_point = {
        "time": robot_state["elapsed_time"],
        "velocity": robot_state["velocity"],
        "energy": robot_state["energy"],
    }

    data_point.update({f"theta{i + 1}": joints[i] for i in range(6)})
    data_point.update({f"pos_{axis}": position[idx] for idx, axis in enumerate(["x", "y", "z"])})
    data_point.update({axis: orientation[idx] for idx, axis in enumerate(["roll", "pitch", "yaw"])})
    data_point.update({f"joint_vel_{i + 1}": joint_velocities[i] for i in range(6)})

    return data_point
