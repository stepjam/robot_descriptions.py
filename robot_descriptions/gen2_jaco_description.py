"""Kinova Jaco Gen2 with 2 Finger gripper description."""

from os import path as _path

PACKAGE_PATH: str = _path.dirname(_path.abspath(__file__))
REPOSITORY_PATH = PACKAGE_PATH

URDF_PATH: str = _path.join(PACKAGE_PATH, "urdfs", "kinova", "j2n6s200.urdf")
