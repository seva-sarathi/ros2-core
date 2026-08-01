from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='seva_telemetry',
            executable='listener',
            name='seva_listener',
            output='screen',
            emulate_tty=True
        )
    ])
