import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped


class Utilmessage(Node):
    def __init__(self):
        super().__init__("simple_util")
        self.odom_sub_ = self.create_subscription(Odometry, "bumperbot_controller/odom", self.odomcallback, 10)
        self.path_pub_ = self.create_publisher(Path, "bumperbot_controller/trajectory", 10)
        self.trajectory_ = Path()
    
    
    def odomcallback(self, msg:Odometry):
        self.trajectory_.header.frame_id = msg.header.frame_id
        current_pose = PoseStamped()
        current_pose.header.frame_id = msg.header.frame_id
        current_pose.header.stamp = msg.header.stamp
        current_pose.pose = msg.pose.pose
        self.trajectory_.poses.append(current_pose)
        self.path_pub_.publish(self.trajectory_)
        
        

def main():
    rclpy.init()
    simple_util = Utilmessage()
    rclpy.spin(simple_util)
    simple_util.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
    