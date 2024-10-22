import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class SimpleTurtlesimKinematics(Node):
    def __init__(self):
        super().__init__("simple_turtlesim_kinematics")
        
        self.turtle1pose_sub = self.create_subscription(Pose, "/turtle1/pose" , self.turtle1posecallback, 10)
        self.turtle2pose_sub = self.create_subscription(Pose, "/turtle2/pose" , self.turtle2posecallback, 10)
        self.last_turtle1_pose = Pose()
        self.last_turtle2_pose = Pose()
        
    def turtle1posecallback(self, msg):
        self.last_turtle1_pose = msg
    
    def turtle2posecallback(self, msg):
        self.last_turtle2_pose = msg
        Tx = self.last_turtle2_pose.x - self.last_turtle1_pose.x
        Ty = self.last_turtle2_pose.y - self.last_turtle1_pose.y
        theta = self.last_turtle2_pose.theta - self.last_turtle1_pose.theta
        
        self.get_logger().info ( "Transformation cordinates are Tx:%f , Ty: %f , theta: %f" %(Tx, Ty , theta)
                                )


def main():
    rclpy.init()
    simple_turtlesim_kinmatic = SimpleTurtlesimKinematics()
    rclpy.spin(simple_turtlesim_kinmatic)
    simple_turtlesim_kinmatic.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__" :
    main()