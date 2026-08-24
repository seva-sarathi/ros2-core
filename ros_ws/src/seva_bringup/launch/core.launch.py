from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    navigation_share = get_package_share_directory("seva_navigation")

    default_graph = os.path.join(
        navigation_share,
        "config",
        "graph.yaml",
    )

    default_map = "/app/maps/my_track_map.yaml"

    map_file = LaunchConfiguration("map_file")
    graph_file = LaunchConfiguration("graph_file")

    map_server = Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[
            {
                "yaml_filename": map_file,
                "use_sim_time": False,
            }
        ],
    )

    map_lifecycle = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="map_lifecycle_manager",
        output="screen",
        parameters=[
            {
                "autostart": True,
                "node_names": ["map_server"],
                "use_sim_time": False,
            }
        ],
    )

    graph_manager = Node(
        package="seva_navigation",
        executable="graph_manager",
        name="navigation_graph",
        output="screen",
        parameters=[
            {
                "graph_file": graph_file,
                "frame_id": "map",
                "publish_rate": 1.0,
            }
        ],
    )

    path_planner = Node(
        package="seva_navigation",
        executable="path_planner",
        name="dijkstra_planner",
        output="screen",
        parameters=[
            {
                "graph_file": graph_file,
                "frame_id": "map",
            }
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "map_file",
                default_value=default_map,
                description="Absolute path to the ROS occupancy map YAML.",
            ),
            DeclareLaunchArgument(
                "graph_file",
                default_value=default_graph,
                description="Absolute path to the navigation graph YAML.",
            ),
            map_server,
            map_lifecycle,
            graph_manager,
            path_planner,
        ]
    )
