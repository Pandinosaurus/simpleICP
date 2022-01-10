"""
Collection of utility functions used by > 1 modules.
"""

from typing import Tuple

import numpy as np


def euler_coord_to_homogeneous_coord(XE: np.array) -> np.array:
    """Convert Euler coordinates to homogeneous coordinates."""

    no_points = np.shape(XE)[0]
    XH = np.column_stack((XE, np.ones(no_points)))

    return XH


def homogeneous_coord_to_euler_coord(XH: np.array) -> np.array:
    """Convert homogeneous coordinates to Euler coordinates."""

    XE = np.column_stack(
        (XH[:, 0] / XH[:, 3], XH[:, 1] / XH[:, 3], XH[:, 2] / XH[:, 3])
    )

    return XE


def euler_angles_to_linearized_rotation_matrix(
    alpha1: float, alpha2: float, alpha3: float
) -> np.array:
    """Compute linearized rotation matrix from three Euler angles."""

    dR = np.array([[1, -alpha3, alpha2], [alpha3, 1, -alpha1], [-alpha2, alpha1, 1]])

    return dR


def euler_angles_to_rotation_matrix(
    alpha1: float, alpha2: float, alpha3: float
) -> np.array:

    R = np.array(
        [
            [
                np.cos(alpha2) * np.cos(alpha3),
                -np.cos(alpha2) * np.sin(alpha3),
                np.sin(alpha2),
            ],
            [
                np.cos(alpha1) * np.sin(alpha3)
                + np.sin(alpha1) * np.sin(alpha2) * np.cos(alpha3),
                np.cos(alpha1) * np.cos(alpha3)
                - np.sin(alpha1) * np.sin(alpha2) * np.sin(alpha3),
                -np.sin(alpha1) * np.cos(alpha2),
            ],
            [
                np.sin(alpha1) * np.sin(alpha3)
                - np.cos(alpha1) * np.sin(alpha2) * np.cos(alpha3),
                np.sin(alpha1) * np.cos(alpha3)
                + np.cos(alpha1) * np.sin(alpha2) * np.sin(alpha3),
                np.cos(alpha1) * np.cos(alpha2),
            ],
        ]
    )

    return R


def rotation_matrix_to_euler_angles(R: np.array) -> Tuple[float, float, float]:
    """Extract Euler angles from rotation matrix R."""

    alpha1 = np.arctan2(-R[1, 2], R[2, 2])
    alpha2 = np.arcsin(R[0, 2])
    alpha3 = np.arctan2(-R[0, 1], R[0, 0])

    return alpha1, alpha2, alpha3


def create_homogeneous_transformation_matrix(R: np.array, t: np.array) -> np.array:
    """Create homogeneous transformation matrix from rotation matrix R and translation vector t."""

    H = np.array(
        [
            [R[0, 0], R[0, 1], R[0, 2], t[0]],
            [R[1, 0], R[1, 1], R[1, 2], t[1]],
            [R[2, 0], R[2, 1], R[2, 2], t[2]],
            [0, 0, 0, 1],
        ]
    )

    return H
