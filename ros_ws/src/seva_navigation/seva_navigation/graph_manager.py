from visualization_msgs.msg import Marker, MarkerArray
import rclpy
from rclpy.node import Node

from seva_navigation.graph import NavigationGraph


class GraphManager(Node):
    def __init__(self):
        super().__init__("navigation_graph")

        self.declare_parameter("graph_file", "")
        self.declare_parameter("frame_id", "map")
        self.declare_parameter("publish_rate", 1.0)

        graph_file = self.get_parameter("graph_file").value
        self.frame_id = self.get_parameter("frame_id").value
        publish_rate = float(self.get_parameter("publish_rate").value)

        if not graph_file:
            raise RuntimeError("Parameter 'graph_file' is required")

        self.graph = NavigationGraph(graph_file)

        self.marker_publisher = self.create_publisher(
            MarkerArray,
            "/navigation/graph",
            10,
        )

        self.timer = self.create_timer(
            1.0 / max(publish_rate, 0.1),
            self.publish_graph,
        )

        self.get_logger().info(
            f"Loaded navigation graph with {len(self.graph.nodes)} nodes"
        )

    def publish_graph(self):
        markers = MarkerArray()

        edge_marker = Marker()
        edge_marker.header.frame_id = self.frame_id
        edge_marker.header.stamp = self.get_clock().now().to_msg()
        edge_marker.ns = "navigation_edges"
        edge_marker.id = 0
        edge_marker.type = Marker.LINE_LIST
        edge_marker.action = Marker.ADD
        edge_marker.scale.x = 0.03

        marker_id = 1

        for source, neighbors in self.graph.edges.items():
            source_node = self.graph.nodes[source]

            for target, _ in neighbors:
                # Draw each undirected edge only once.
                if source > target:
                    continue

                target_node = self.graph.nodes[target]

                from geometry_msgs.msg import Point

                start = Point()
                start.x = source_node.x
                start.y = source_node.y

                end = Point()
                end.x = target_node.x
                end.y = target_node.y

                edge_marker.points.extend([start, end])

        markers.markers.append(edge_marker)

        for node_id, node in self.graph.nodes.items():
            marker = Marker()
            marker.header.frame_id = self.frame_id
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "navigation_nodes"
            marker.id = marker_id
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            marker.pose.position.x = node.x
            marker.pose.position.y = node.y
            marker.pose.position.z = 0.05
            marker.scale.x = 0.12
            marker.scale.y = 0.12
            marker.scale.z = 0.12
            markers.markers.append(marker)

            marker_id += 1

        self.marker_publisher.publish(markers)


def main(args=None):
    rclpy.init(args=args)
    node = GraphManager()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()