import rclpy
from rclpy.node import Node 
from bumperbot_msgs.srv import Addtwoints

class SimpleService(Node):
    def __init__(self):
        super().__init__("simpleservice_server")
        self.add_ints = self.create_service(Addtwoints, "add_two_ints", self.service_callback)
        self.get_logger().info("Service Server has been started")
        
    def service_callback(self, req, res):
        
        res.sum = req.a + req.b
        self.get_logger().info( "addition of two ints %s, %s, sum would be %s" %(req.a , req.b, res.sum) )
        return res

def main():
    rclpy.init()
    simple_Service = SimpleService()
    rclpy.spin(simple_Service) 
    simple_Service.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
    
