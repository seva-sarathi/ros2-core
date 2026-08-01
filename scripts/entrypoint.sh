#!/bin/bash
set -e

# Source base ROS2 environment
source "/opt/ros/humble/setup.bash"

# Source compiled workspace if built
if [ -f "/app/ros_ws/install/setup.bash" ]; then
    source "/app/ros_ws/install/setup.bash"
fi

exec "$@"
