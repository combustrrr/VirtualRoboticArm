"""Shared constants for the PUMA 560 digital twin."""
from __future__ import annotations

import math
from typing import Tuple

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

# Denavit–Hartenberg parameters for the PUMA 560 (IIT KGP Virtual Labs)
DH_PARAMS = [
    (0.0, 0.0, 0.0, math.pi / 2),      # Joint 1
    (0.0, 0.0, 0.432, 0.0),            # Joint 2
    (0.0, 0.1495, 0.0203, -math.pi / 2),  # Joint 3
    (0.0, 0.432, 0.0, math.pi / 2),    # Joint 4
    (0.0, 0.0, 0.0, -math.pi / 2),     # Joint 5
    (0.0, 0.0, 0.0, 0.0),              # Joint 6
]
