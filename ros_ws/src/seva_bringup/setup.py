import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'seva_bringup'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Anurag Chandra',
    maintainer_email='nrgchandra@gmail.com',
    description='Launch configurations for Seva Sarathi MEC system',
    license='MIT',
    entry_points={
        'console_scripts': [],
    },
)
