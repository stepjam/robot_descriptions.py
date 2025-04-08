"""UR5 with Robotiq 2F-85 gripper URDF description."""

from os import path as _path
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET
import robot_descriptions.ur5_description as ur5
import robot_descriptions.robotiq_2f85_description as robotiq

UR5_URDF_PATH = ur5.URDF_PATH
ROBOTIQ_2F85_URDF_PATH = robotiq.URDF_PATH

INVERTED_JOINTS = [
    "left_inner_finger_joint",
    "right_outer_knuckle_joint",
    "right_inner_knuckle_joint",
]

# Make tempdir to store the URDF
tempdir = tempfile.TemporaryDirectory()
tempdir_path = Path(tempdir.name) / "urdfs" 
tempdir_path.mkdir(parents=True, exist_ok=True)

REPOSITORY_PATH = ur5.REPOSITORY_PATH
PACKAGE_PATH: str = ur5.PACKAGE_PATH
URDF_PATH: str = str(Path(UR5_URDF_PATH).parent / "ur5_2f85.urdf")


def _add_gripper_joint(root: ET.Element) -> None:
    """Add fixed joint connecting arm to gripper."""
    joint = ET.SubElement(
        root, "joint", {"name": "tool0-robotiq_85_base_link", "type": "fixed"}
    )
    ET.SubElement(joint, "origin", {"rpy": "0 0 0", "xyz": "0 0 0"})
    ET.SubElement(joint, "parent", {"link": "tool0"})
    ET.SubElement(joint, "child", {"link": "robotiq_85_base_link"})

def _remove_ee_joint(root: ET.Element) -> None:
    """Remove incorrect ee_fixed_joint."""
    ee_fixed_joint = root.find(".//joint[@name='ee_fixed_joint']")
    if ee_fixed_joint is not None:
        root.remove(ee_fixed_joint)
    ee_link = root.find(".//link[@name='ee_link']")
    if ee_link is not None:
        root.remove(ee_link)

def _process_gripper_joints(tree: ET.ElementTree) -> None:
    """Process gripper joints and store limits."""
    for joint in tree.findall(".//joint"):
        if joint.attrib["type"] == "revolute":
            name = joint.attrib["name"]
            joint_limit = joint.find("limit")
            if name in INVERTED_JOINTS:
                joint_limit.attrib["lower"] = str(
                    -float(joint_limit.attrib["upper"])
                )


def _patch_urdf(urdf_path_to_patch: Path) -> Path:
    """Patch the URDF to combine arm and gripper."""
    arm_tree = ET.parse(urdf_path_to_patch)
    arm_root = arm_tree.getroot()
    gripper_tree = ET.parse(ROBOTIQ_2F85_URDF_PATH)
    arm_root.extend(gripper_tree.getroot())
    _add_gripper_joint(arm_root)
    _remove_ee_joint(arm_root)
    _process_gripper_joints(gripper_tree)
    arm_tree.write(URDF_PATH)

_patch_urdf(Path(UR5_URDF_PATH))