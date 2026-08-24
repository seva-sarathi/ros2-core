from setuptools import find_packages, setup
import os
from glob import glob

package_name = "seva_navigation"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(),

    data_files=[
        (
            "share/ament_index/resource_index/packages",
            [f"resource/{package_name}"],
        ),
        (
            f"share/{package_name}",
            ["package.xml"],
        ),
        (
            f"share/{package_name}/config",
            glob("config/*.yaml"),
        ),
    ],

    install_requires=[
        "setuptools",
        "PyYAML",
    ],

    zip_safe=True,

    maintainer="SevaSarathi",
    maintainer_email="dev@sevasarathi.local",

    description="SevaSarathi ROS 2 navigation graph and Dijkstra planner",

    license="Apache-2.0",

    entry_points={
        "console_scripts": [
            "graph_manager = seva_navigation.graph_manager:main",
            "path_planner = seva_navigation.path_planner:main",
        ],
    },
)