
# Seva Sarathi — ROS 2 Core (`ros2-core`)

The central ROS 2 node architecture for the **Seva Sarathi** MEC (Multi-access Edge Computing) infrastructure. This repository manages hardware communications, telemetry streaming, and node orchestration over CycloneDDS.

---

## 📁 Repository Structure

```text
ros2-core/
├── ros_ws/
│   └── src/
│       ├── seva_bringup/          # Launch scripts & core configurations
│       └── seva_telemetry/        # Telemetry nodes (Listener & Talker)
├── scripts/
│   └── entrypoint.sh              # Docker environment sourcing script
├── docker-compose.yml             # Local testing environment
├── Dockerfile                     # Multi-stage production container build
└── README.md

```
## ⚙️ Prerequisites
 * **MEC Server:**
   * Docker & Docker Compose **or** MicroK8s installed.
   * Same LAN / Wi-Fi network as your laptop.
 * **Laptop:**
   * ROS 2 Humble installed (or Docker running ROS 2 Humble).
   * ROS_DOMAIN_ID=0 set on both machines.
## 🚀 Step-by-Step Usage Guide
### 1. Build and Run the Server (MEC Node)
#### Option A: Using Docker Compose
On your MEC server, navigate to the repository root and start the container:
```bash
# Build and launch in detached mode
docker compose up -d --build

# View real-time logs from the listener
docker compose logs -f ros2-core

```
#### Option B: Native Workspace Build (Without Docker)
If ROS 2 Humble is installed directly on your MEC server:
```bash
cd ros_ws

# Source ROS 2 base
source /opt/ros/humble/setup.bash

# Build workspace packages
colcon build --symlink-install

# Source workspace
source install/setup.bash

# Run listener node
ros2 run seva_telemetry listener

```
### 2. Send "Hello World" from Your Laptop
On your laptop, open a terminal connected to the same local network:
```bash
# 1. Source ROS 2 base environment
source /opt/ros/humble/setup.bash   # On Linux / macOS
# call C:\dev\ros2_humble\local_setup.ps1  (On Windows PowerShell)

# 2. Match the ROS_DOMAIN_ID and DDS Implementation
export ROS_DOMAIN_ID=0
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# 3. Source your compiled workspace or run directly if built locally:
# (If workspace is built locally on laptop)
source ros_ws/install/setup.bash
ros2 run seva_telemetry talker

# OR publish directly via ROS 2 CLI:
ros2 topic pub /chatter std_msgs/msg/String "data: 'Hello World from Laptop to MEC Server!'"

```
## 📊 Live Message Transfer Logs
When the connection succeeds over DDS multicast, you will observe the following logs on both ends:
### 📤 Laptop Terminal (talker.py)
```text
[INFO] [seva_talker]: Seva Talker active. Publishing to /chatter...
[INFO] [seva_talker]: Published: "Hello World from Laptop to MEC Server #0"
[INFO] [seva_talker]: Published: "Hello World from Laptop to MEC Server #1"
[INFO] [seva_talker]: Published: "Hello World from Laptop to MEC Server #2"
[INFO] [seva_talker]: Published: "Hello World from Laptop to MEC Server #3"

```
### 📥 MEC Server Terminal (listener.py)
```text
[INFO] [seva_listener]: Seva Listener active. Listening on /chatter...
[INFO] [seva_listener]: Received on MEC Server: "Hello World from Laptop to MEC Server #0"
[INFO] [seva_listener]: Received on MEC Server: "Hello World from Laptop to MEC Server #1"
[INFO] [seva_listener]: Received on MEC Server: "Hello World from Laptop to MEC Server #2"
[INFO] [seva_listener]: Received on MEC Server: "Hello World from Laptop to MEC Server #3"

```
## 🛠️ Troubleshooting & Networking
 * **No Messages Received?**
   Ensure your firewall allows ROS 2 DDS multicast traffic on ports 7400:7500/udp:
   ```bash
   sudo ufw allow 7400:7500/udp
   
   ```
 * **Host Network Mode:**
   When running inside Docker or Kubernetes, ensure network_mode: "host" (or hostNetwork: true in Kubernetes manifests) is set so DDS discovery packet broadcats cross container boundaries.
```

---

<ElicitationsGroup message="What would you like to set up next?">
  <Elicitation label="Setup GitHub Actions CI/CD pipeline" query="Show me the GitHub Actions workflow file to build and push this ros2-core Docker image."/>
  <Elicitation label="Configure MQTT Broker & Bridge Node" query="Let's set up the mqtt-broker repository structure and bridge node to relay ROS2 messages to MQTT."/>
</ElicitationsGroup>


