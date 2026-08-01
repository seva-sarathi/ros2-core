from setuptools import find_packages, setup

package_name = 'seva_telemetry'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Anurag Chandra',
    maintainer_email='nrgchandra@gmail.com',
    description='Telemetry listener and talker nodes for Seva Sarathi MEC system',
    license='MIT',
    entry_points={
        'console_scripts': [
            'listener = seva_telemetry.listener:main',
            'talker = seva_telemetry.talker:main',
        ],
    },
)
