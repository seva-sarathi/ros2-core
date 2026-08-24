import os
from glob import glob

from setuptools import find_packages, setup

package_name = "seva_bringup"

setup(
    name=package_name,
    version="0.2.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            [f"resource/{package_name}"],
        ),
        (f"share/{package_name}", ["package.xml"]),
        (
            os.path.join("share", package_name, "launch"),
            glob("launch/*.launch.py"),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Anurag Chandra",
    maintainer_email="nrgchandra@gmail.com",
    description="Launch configurations for the Seva Sarathi MEC ROS 2 server core.",
    license="MIT",
)
