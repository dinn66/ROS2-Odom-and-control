import rclpy
from rclpy.node import Node 
from bumperbot_msgs.srv import Addtwoints
import sys

class SimpleService(Node):
    def __init__(self, a , b):
        super().__init__("simpleservice_client")
        self.client_ = self.create_client(Addtwoints, "add_two_ints")
        
        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service client has not  been started, retrying again...")
        
        self.req_ = Addtwoints.Request()
        self.req_.a = a 
        self.req_.b = b 
        
        self.future_ = self.client_.call_async(self.req_)
        self.future_.add_done_callback(self.responseCallback)
        
    def responseCallback(self, future):
        self.get_logger().info( "service Response %d " % future.result().sum)
        

def main():
    rclpy.init()
    if len(sys.argv) !=3:
        print("Wrorng number of arguments ")
        return -1
    
    
    simple_service_client = SimpleService(int(sys.argv[1]), int(sys.argv[2]))
    rclpy.spin(simple_service_client)
    simple_service_client.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()



