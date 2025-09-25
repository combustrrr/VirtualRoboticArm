"""
PUMA 560 Forward Kinematics Implementation
Based on the IIT Kharagpur virtual labs implementation
"""

import numpy as np
import math


class PUMAKinematics:
    """
    Forward kinematics for PUMA 560 robotic manipulator
    Using Denavit-Hartenberg parameters
    """

    def __init__(self):
        # DH parameters for PUMA 560 (in meters and degrees)
        self.a2 = 0.432  # link length 2
        self.a3 = 0.0203  # link length 3
        self.d3 = 0.1495  # link offset 3
        self.d4 = 0.432  # link offset 4

        # Joint limits (degrees)
        self.joint_limits = {
            'theta1': (-160, 160),
            'theta2': (-225, 45),
            'theta3': (-225, 45),
            'theta4': (-110, 170),
            'theta5': (-100, 100),
            'theta6': (-266, 266)  # Note: code uses -225 to 225, but HTML shows -266 to 266
        }

    def dh_transform(self, theta, d, a, alpha):
        """
        Calculate Denavit-Hartenberg transformation matrix

        Parameters:
        theta: joint angle (degrees)
        d: link offset
        a: link length
        alpha: link twist (degrees)

        Returns:
        4x4 transformation matrix
        """
        theta_rad = math.radians(theta)
        alpha_rad = math.radians(alpha)

        ct = math.cos(theta_rad)
        st = math.sin(theta_rad)
        ca = math.cos(alpha_rad)
        sa = math.sin(alpha_rad)

        T = np.array([
            [ct, -st*ca,  st*sa, a*ct],
            [st,  ct*ca, -ct*sa, a*st],
            [0,      sa,     ca,    d],
            [0,       0,      0,    1]
        ])

        return T

    def forward_kinematics(self, theta1, theta2, theta3, theta4, theta5, theta6):
        """
        Calculate forward kinematics for PUMA 560
        Using the exact transformation matrices from the IIT Kharagpur implementation

        Parameters:
        theta1, theta2, theta3, theta4, theta5, theta6: joint angles in degrees

        Returns:
        T_06: 4x4 transformation matrix from base to end-effector
        position: [x, y, z] position of end-effector
        """
        # Convert to radians
        t1_rad = math.radians(theta1)
        t2_rad = math.radians(theta2)
        t3_rad = math.radians(theta3)
        t4_rad = math.radians(theta4)
        t5_rad = math.radians(theta5)
        t6_rad = math.radians(theta6)

        # Transformation matrices as implemented in JavaScript
        T1 = np.array([
            [math.cos(t1_rad), -math.sin(t1_rad), 0, 0],
            [math.sin(t1_rad),  math.cos(t1_rad), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        T2 = np.array([
            [math.cos(t2_rad), -math.sin(t2_rad), 0, 0],
            [0, 0, 1, 0],
            [-math.sin(t2_rad), -math.cos(t2_rad), 0, 0],
            [0, 0, 0, 1]
        ])

        T3 = np.array([
            [math.cos(t3_rad), -math.sin(t3_rad), 0, self.a2],
            [math.sin(t3_rad),  math.cos(t3_rad), 0, 0],
            [0, 0, 1, self.d3],
            [0, 0, 0, 1]
        ])

        T4 = np.array([
            [math.cos(t4_rad), -math.sin(t4_rad), 0, self.a3],
            [0, 0, 1, self.d4],
            [-math.sin(t4_rad), -math.cos(t4_rad), 0, 0],
            [0, 0, 0, 1]
        ])

        T5 = np.array([
            [math.cos(t5_rad), -math.sin(t5_rad), 0, 0],
            [0, 0, -1, 0],
            [math.sin(t5_rad),  math.cos(t5_rad), 0, 0],
            [0, 0, 0, 1]
        ])

        T6 = np.array([
            [math.cos(t6_rad), -math.sin(t6_rad), 0, 0],
            [0, 0, 1, 0],
            [-math.sin(t6_rad), -math.cos(t6_rad), 0, 0],
            [0, 0, 0, 1]
        ])

        # Calculate cumulative transformations
        T_06 = T1 @ T2 @ T3 @ T4 @ T5 @ T6

        # Extract position
        position = T_06[:3, 3]

        return T_06, position

    def validate_joint_angles(self, theta1, theta2, theta3, theta4, theta5, theta6):
        """
        Validate that joint angles are within limits

        Returns:
        True if all angles are valid, False otherwise
        error_msg: error message if validation fails
        """
        angles = [theta1, theta2, theta3, theta4, theta5, theta6]
        joint_names = ['theta1', 'theta2', 'theta3', 'theta4', 'theta5', 'theta6']

        for i, (angle, name) in enumerate(zip(angles, joint_names)):
            min_angle, max_angle = self.joint_limits[name]
            if angle < min_angle or angle > max_angle:
                return False, f"Joint {name} angle {angle}° is outside range [{min_angle}°, {max_angle}°]"

        return True, ""

    def get_joint_limits(self):
        """Return joint limits as a dictionary"""
        return self.joint_limits.copy()


def main():
    """Test the PUMA kinematics implementation"""
    puma = PUMAKinematics()

    # Test with zero angles
    print("Testing PUMA 560 Forward Kinematics")
    print("=" * 40)

    # Zero position
    T_06, pos = puma.forward_kinematics(0, 0, 0, 0, 0, 0)
    print("Zero position:")
    print(f"Position: [{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}]")
    print("Transformation Matrix:")
    print(T_06)
    print()

    # Test joint limits validation
    valid, msg = puma.validate_joint_angles(0, 0, 0, 0, 0, 0)
    print(f"Zero angles valid: {valid}")

    valid, msg = puma.validate_joint_angles(200, 0, 0, 0, 0, 0)
    print(f"Invalid theta1 (200°): {valid} - {msg}")

    # Test with some angles
    T_06, pos = puma.forward_kinematics(45, -90, 45, 0, 0, 0)
    print(f"\nPosition with angles [45°, -90°, 45°, 0°, 0°, 0°]:")
    print(f"Position: [{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}]")


if __name__ == "__main__":
    main()