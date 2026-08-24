#!/bin/bash
set -e

source /opt/ros/humble/setup.bash
source /app/ros_ws/install/setup.bash

if [ -f "/app/ros_ws/install/setup.bash" ]; then
    source /app/ros_ws/install/setup.bash
fi

exec "$@"
