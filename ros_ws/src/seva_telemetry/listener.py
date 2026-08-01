import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SevaListenerNode(Node):
    def __init__(self):
        super().__init__('seva_listener')
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10
        )
        self.get_logger().info('Seva Listener active. Listening on /chatter...')

    def listener_callback(self, msg):
        self.get_logger().info(f'Received on MEC Server: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = SevaListenerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
