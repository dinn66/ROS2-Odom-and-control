import rclpy
from rclpy.node import Node
from std_msgs.msg import String 

class SimplePublisher(Node):
    def __init__(self):
        super().__init__("Simplepublisher")
        self.pub_ = self.create_publisher(String, "chatter", 10)
        self.counter = 0
        self.frequency = 10 
        self.get_logger().info("Publishing at %d Hz" % self.frequency)
        self.timer_ = self.create_timer( self.frequency, self.msgcallback)
        
    def msgcallback(self):
        msg= String()
        msg.data = "Hello Ros2 counter : %d" %self.counter
        self.pub_.publish(msg)
        self.counter +=1
        
    def main():
        rclpy.init()
        simple_publisher = SimplePublisher()
        rclpy.spin(simple_publisher)
        simple_publisher.destroy_node()
        rclpy.shutdown()
    if __name__ == "__main__":
        main()
        