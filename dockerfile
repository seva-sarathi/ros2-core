# ==========================================
# Stage 1: Build Stage
# ==========================================
FROM ros:humble-ros-base-jammy AS builder

# Set working directory
WORKDIR /app/ros_ws

# Install build dependencies and tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy workspace source code
COPY ros_ws/src ./src

# Install ROS dependencies via rosdep
RUN . /opt/ros/humble/setup.sh && \
    apt-get update && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -y --rosdistro humble && \
    rm -rf /var/lib/apt/lists/*

# Build the ROS2 workspace
RUN . /opt/ros/humble/setup.sh && \
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

# ==========================================
# Stage 2: Runtime Stage
# ==========================================
FROM ros:humble-ros-core-jammy AS runner

WORKDIR /app

# Install runtime dependencies (Python libraries for MQTT/Redis bridging)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    ros-humble-rmw-cyclonedds-cpp \
    && pip3 install --no-cache-dir paho-mqtt redis \
    && rm -rf /var/lib/apt/lists/*

# Copy compiled installation artifacts from builder stage
COPY --from=builder /app/ros_ws/install /app/ros_ws/install
COPY scripts/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# Environment variables for ROS2 DDS discovery
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/entrypoint.sh"]

# Default launch command (points to your main bringup package)
CMD ["ros2", "launch", "seva_bringup", "core.launch.py"]
