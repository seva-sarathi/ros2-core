# Seva Sarathi ROS 2 Server Core

This implementation establishes the first server-side navigation core.

## Responsibilities

- Publish the occupancy map on `/map`.
- Load a topological navigation graph.
- Visualize the graph on `/navigation/graph`.
- Run Dijkstra shortest-path planning.
- Expose `/navigation/plan_path`.
- Publish the resulting `nav_msgs/Path` on `/planned_path`.

The Jetson will later consume `/planned_path` and remain responsible for localization,
path following, `/cmd_vel`, motor control, and local safety stop.

## ROS graph

```text
map_server
    |
    +---- /map
    |
navigation_graph ---- /navigation/graph
    |
dijkstra_planner
    |
    +---- /navigation/plan_path (service)
    |
    +---- /planned_path (nav_msgs/Path)
```

## Build locally

```bash
cd ros_ws
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y --rosdistro humble
colcon build --symlink-install
source install/setup.bash
ros2 launch seva_bringup core.launch.py   map_file:=../../maps/my_track_map.yaml
```

From the repository root, the installed graph is used automatically.

## Test the planner

```bash
ros2 service call /navigation/plan_path   seva_navigation_interfaces/srv/PlanPath   "{start_node: track_01, goal_node: track_08}"
```

Check:

```bash
ros2 topic echo /planned_path
ros2 topic echo /map --once
ros2 topic echo /navigation/graph
```

## RViz

Set:

```text
Fixed Frame: map
```

Add:

- Map -> `/map`
- Path -> `/planned_path`
- MarkerArray -> `/navigation/graph`

## Important

`config/graph.yaml` contains bootstrap node coordinates estimated from the supplied
map. They must be validated and adjusted in RViz before physical AGV motion.
Do not use the current graph for live motor control until those coordinates are verified.
