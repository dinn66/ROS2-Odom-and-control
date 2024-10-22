import rclpy
from rclpy.node import Node
import rclpy.time
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster, TransformException
from tf_transformations import quaternion_from_euler, quaternion_multiply, quaternion_inverse
from bumperbot_msgs.srv import GetTransform
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener



class SimpleStaticTransform(Node):
    def __init__(self):
        super().__init__("simple_tf_broadcaster")
        self.static_transform_boradcaster_ = StaticTransformBroadcaster(self)
        self.dynamic_transform_broadcaster_ = TransformBroadcaster(self)
        self.static_transform_stamped_ = TransformStamped()
        self.dynamic_transform_stamped_ = TransformStamped()
        
        self.x_increament = 0.05
        self.last_x_pos = 0.0
        self.last_quaternion_pos = quaternion_from_euler(0, 0 ,0)
        self.quaternion_increament = quaternion_from_euler(0, 0, 0.05)
        self.rotation_counter = 0 
        
        self.buffer_ = Buffer()
        self.tf_listener_ = TransformListener(self.buffer_, self)
    
        
        self.static_transform_stamped_.header.stamp = self.get_clock().now().to_msg()
        self.static_transform_stamped_.header.frame_id = "bumperbot_base"
        self.static_transform_stamped_.child_frame_id = "bumperbot_top"
        self.static_transform_stamped_.transform.translation.x = 0.0
        self.static_transform_stamped_.transform.translation.y = 0.0
        self.static_transform_stamped_.transform.translation.z = 0.3
        self.static_transform_stamped_.transform.rotation.x = 0.0
        self.static_transform_stamped_.transform.rotation.y = 0.0
        self.static_transform_stamped_.transform.rotation.z = 0.0
        self.static_transform_stamped_.transform.rotation.w = 1.0
        
        self.static_transform_boradcaster_.sendTransform(self.static_transform_stamped_)
        self.get_logger().info("Broadcasting static trannsform message betwwen %s and %s" 
                               %(self.static_transform_stamped_.header.frame_id, self.static_transform_stamped_.child_frame_id))
        
        
        self.timer_ = self.create_timer(0.1, self.timer_callback)
        
        self.get_transform_srv = self.create_service(GetTransform, "get_transform", self.transformcallback)
    def timer_callback(self):
        
        self.dynamic_transform_stamped_.header.stamp = self.get_clock().now().to_msg()
        self.dynamic_transform_stamped_.header.frame_id = "odom"
        self.dynamic_transform_stamped_.child_frame_id = "bumperbot_base"
        
        self.dynamic_transform_stamped_.transform.translation.x = self.x_increament + self.last_x_pos
        self.dynamic_transform_stamped_.transform.translation.y = 0.0
        self.dynamic_transform_stamped_.transform.translation.z = 0.0
        q = quaternion_multiply(self.last_quaternion_pos, self.quaternion_increament)
        self.dynamic_transform_stamped_.transform.rotation.x = q[0]
        self.dynamic_transform_stamped_.transform.rotation.y = q[1]
        self.dynamic_transform_stamped_.transform.rotation.z = q[2]
        self.dynamic_transform_stamped_.transform.rotation.w = q[3]
        self.dynamic_transform_broadcaster_.sendTransform(self.dynamic_transform_stamped_)
        self.last_x_pos = self.dynamic_transform_stamped_.transform.translation.x
        self.last_quaternion_pos = q
        self.rotation_counter +=1
        if self.rotation_counter >=100:
            self.quaternion_increament = quaternion_inverse(self.quaternion_increament)
            self.rotation_counter = 0 
        self.get_logger().info("Broadcasting dynamic trannsform message betwwen %s and %s" 
                               %(self.dynamic_transform_stamped_.header.frame_id, self.dynamic_transform_stamped_.child_frame_id))
    
    def transformcallback(self, req, res):
        self.get_logger().info("Requested service between %s and %s has been started" %(req.frame_id, req.child_frame_id))
        requested_transform = TransformStamped()
        try:
            requested_transform = self.buffer_.lookup_transform(req.frame_id, req.child_frame_id, rclpy.time.Time())
        except TransformException as e:
            self.get_logger().error("Requested transform between %s and %s is not available "%(req.frame_id, req.child_frame_id) )
            res.success = False
            return res
        res.transform = requested_transform
        res.success = True
        return res
    
        
    
def main():
    rclpy.init()
    simple_tf_broadcaster = SimpleStaticTransform()
    rclpy.spin(simple_tf_broadcaster)
    simple_tf_broadcaster.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
        
