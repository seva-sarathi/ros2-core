import math

import rclpy
from geometry_msgs.msg import PoseStamped, Quaternion
from nav_msgs.msg import Path
from rclpy.node import Node

from seva_navigation.graph import NavigationGraph
from seva_navigation_interfaces.srv import PlanPath


def quaternion_from_yaw(yaw: float) -> Quaternion:
    quaternion = Quaternion()
    quaternion.z = math.sin(yaw / 2.0)
    quaternion.w = math.cos(yaw / 2.0)
    return quaternion


class PathPlanner(Node):
    def __init__(self):
        super().__init__("dijkstra_planner")

        self.declare_parameter("graph_file", "")
        self.declare_parameter("frame_id", "map")

        graph_file = self.get_parameter("graph_file").value
        self.frame_id = self.get_parameter("frame_id").value

        if not graph_file:
            raise RuntimeError("Parameter 'graph_file' is required")

        self.graph = NavigationGraph(graph_file)

        self.path_publisher = self.create_publisher(
            Path,
            "/planned_path",
            10,
        )

        self.plan_service = self.create_service(
            PlanPath,
            "/navigation/plan_path",
            self.plan_path,
        )

        self.get_logger().info(
            f"Loaded navigation graph with {len(self.graph.nodes)} nodes"
        )

    def plan_path(self, request, response):
        try:
            node_ids, total_cost = self.graph.shortest_path(
                request.start_node,
                request.goal_node,
            )
        except KeyError as error:
            response.success = False
            response.message = str(error)
            response.node_ids = []
            response.total_cost = 0.0
            response.path = Path()
            return response

        if not node_ids:
            response.success = False
            response.message = (
                f"No route from '{request.start_node}' "
                f"to '{request.goal_node}'"
            )
            response.node_ids = []
            response.total_cost = 0.0
            response.path = Path()
            return response

        path = Path()
        path.header.stamp = self.get_clock().now().to_msg()
        path.header.frame_id = self.frame_id

        for node_id in node_ids:
            node = self.graph.nodes[node_id]

            pose = PoseStamped()
            pose.header = path.header
            pose.pose.position.x = node.x
            pose.pose.position.y = node.y
            pose.pose.orientation = quaternion_from_yaw(node.yaw)

            path.poses.append(pose)

        self.path_publisher.publish(path)

        response.success = True
        response.message = "Path planned successfully"
        response.node_ids = node_ids
        response.total_cost = total_cost
        response.path = path

        self.get_logger().info(
            f"Planned {request.start_node} -> {request.goal_node}: "
            f"{' -> '.join(node_ids)} "
            f"(cost={total_cost:.3f} m)"
        )

        return response


def main(args=None):
    rclpy.init(args=args)
    node = PathPlanner()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()