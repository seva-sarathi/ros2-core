import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SevaTalkerNode(Node):
    def __init__(self):
        super().__init__('seva_talker')
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0
        self.get_logger().info('Seva Talker active. Publishing to /chatter...')

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World from Laptop to MEC Server #{self.count}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: "{msg.data}"')
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = SevaTalkerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
