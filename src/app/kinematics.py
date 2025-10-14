"""Kinematics and manipulability utilities for the PUMA 560 arm."""
from __future__ import annotations

import math
from typing import List, Tuple

import numpy as np

from .constants import DH_PARAMS


def _dh_transform(theta: float, d: float, a: float, alpha: float) -> np.ndarray:
    """Return the homogeneous transformation matrix for supplied DH parameters."""
    ct = math.cos(theta)
    st = math.sin(theta)
    ca = math.cos(alpha)
    sa = math.sin(alpha)

    return np.array([
        [ct, -st * ca, st * sa, a * ct],
        [st, ct * ca, -ct * sa, a * st],
        [0, sa, ca, d],
        [0, 0, 0, 1],
    ])


def forward_kinematics(joint_angles_deg: List[float]) -> Tuple[np.ndarray, np.ndarray]:
    """Compute end-effector position and rotation matrix for given joint angles."""
    joint_angles_rad = [math.radians(angle) for angle in joint_angles_deg]
    transform = np.eye(4)

    for i, (theta_offset, d, a, alpha) in enumerate(DH_PARAMS):
        theta = joint_angles_rad[i] + theta_offset
        transform = transform @ _dh_transform(theta, d, a, alpha)

    position = transform[:3, 3]
    rotation = transform[:3, :3]
    return position, rotation


def rotation_to_euler(rotation_matrix: np.ndarray) -> Tuple[float, float, float]:
    """Convert rotation matrix to roll, pitch, yaw in degrees."""
    sy = math.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2)
    singular = sy < 1e-6

    if not singular:
        roll = math.atan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
        pitch = math.atan2(-rotation_matrix[2, 0], sy)
        yaw = math.atan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    else:
        roll = math.atan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
        pitch = math.atan2(-rotation_matrix[2, 0], sy)
        yaw = 0.0

    return math.degrees(roll), math.degrees(pitch), math.degrees(yaw)


def calculate_velocity(current_pos: np.ndarray, previous_pos: np.ndarray, dt: float) -> float:
    """Return the magnitude of the linear velocity vector."""
    if dt <= 0:
        return 0.0
    velocity_vector = (current_pos - previous_pos) / dt
    return float(np.linalg.norm(velocity_vector))


def calculate_jacobian(joint_angles_deg: List[float]) -> np.ndarray:
    """Numerically approximate the Jacobian matrix for the current joint configuration."""
    epsilon = 0.1
    position_base, _ = forward_kinematics(joint_angles_deg)
    jacobian = np.zeros((3, 6))

    for idx in range(6):
        angles_plus = joint_angles_deg.copy()
        angles_minus = joint_angles_deg.copy()
        angles_plus[idx] += epsilon
        angles_minus[idx] -= epsilon

        pos_plus, _ = forward_kinematics(angles_plus)
        pos_minus, _ = forward_kinematics(angles_minus)
        jacobian[:, idx] = (pos_plus - pos_minus) / (2 * epsilon)

    return jacobian


def calculate_manipulability(jacobian: np.ndarray) -> float:
    """Return the Yoshikawa manipulability index for the supplied Jacobian."""
    try:
        jjt = jacobian @ jacobian.T
        determinant = float(np.linalg.det(jjt))
        if determinant < 0:
            return 0.0
        return math.sqrt(determinant)
    except Exception:
        return 0.0
