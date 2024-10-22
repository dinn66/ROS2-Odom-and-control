import rclpy
from rclpy.node import Node
from rclpy.parameter import ParameterType
from rcl_interfaces.msg import SetParametersResult

class SimpleParameter(Node):
    def __init__(self):
        super().__init__("simpleparameter")
        self.declare_parameter("simple_int_param", 28)
        self.declare_parameter("simple_string_param", "Din")
        self.add_on_set_parameters_callback(self.paramchangeCallback)
    
    def paramchangeCallback(self, params):
        result = SetParametersResult()
        for param in params:
            if param.name == "simple_int_param" and param.type_ == ParameterType.PARAMETER_INTEGER:
                self.get_logger().info ( "Parameter simple_int_param has been changed! New value is %d" % param.value)
                result.successful = True
            if param.name == "simple_string_param" and param.type == ParameterType.PARAMETER_STRING:
                self.get_logger().info("parameter simple_string_param has been changed1 new value is %d" % param.value)
                result.successful = True
        return result
def main(): 
    rclpy.init()
    simple_parameter = SimpleParameter()
    rclpy.spin(simple_parameter)
    simple_parameter.destroy_node()
    rclpy.shutdown()

if __name__== "__main__":
    main()