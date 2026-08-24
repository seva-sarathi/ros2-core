# ============================================================
# SevaSarathi ROS 2 Core
# ROS 2 Humble / Ubuntu 22.04
# ============================================================

# ============================================================
# Stage 1: Build
# ============================================================
FROM ros:humble-ros-base-jammy AS builder

SHELL ["/bin/bash", "-c"]

WORKDIR /app/ros_ws

# ------------------------------------------------------------
# Build dependencies
# ------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-pip \
    python3-yaml \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Copy ROS workspace
# ------------------------------------------------------------
COPY ros_ws/src ./src

# ------------------------------------------------------------
# Install ROS dependencies
# ------------------------------------------------------------
RUN source /opt/ros/humble/setup.bash && \
    apt-get update && \
    rosdep update && \
    rosdep install \
        --from-paths src \
        --ignore-src \
        --rosdistro humble \
        -r \
        -y && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Build workspace
# ------------------------------------------------------------
RUN source /opt/ros/humble/setup.bash && \
    colcon build \
        --cmake-args \
        -DCMAKE_BUILD_TYPE=Release


# ============================================================
# Stage 2: Runtime
# ============================================================
FROM ros:humble-ros-core-jammy AS runtime

SHELL ["/bin/bash", "-c"]

WORKDIR /app

# ------------------------------------------------------------
# Runtime dependencies
# ------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-rmw-cyclonedds-cpp \
    ros-humble-nav2-map-server \
    ros-humble-nav2-lifecycle-manager \
    python3-yaml \
    python3-pip \
    && pip3 install --no-cache-dir \
        paho-mqtt \
        redis \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Copy compiled ROS workspace
# ------------------------------------------------------------
COPY --from=builder /app/ros_ws/install /app/ros_ws/install

# Keep source available for debugging
COPY --from=builder /app/ros_ws/src /app/ros_ws/src

# ------------------------------------------------------------
# Copy navigation maps
# ------------------------------------------------------------
COPY maps /app/maps

# ------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------
COPY scripts/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# ------------------------------------------------------------
# ROS environment
# ------------------------------------------------------------
ENV ROS_DISTRO=humble
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/entrypoint.sh"]

CMD ["ros2", "launch", "seva_bringup", "core.launch.py"]