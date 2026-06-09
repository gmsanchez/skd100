from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command

from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value = 'False',
        description = 'Use simulation (Gazebo) clock if true'
    )

    urdf_path = PathJoinSubstitution(
        [FindPackageShare("skd100_description"), 'urdf', 'skd100.urdf.xacro']
    )

    robot_description = ParameterValue(Command(['xacro ', urdf_path, ' is_sim:=', use_sim_time]), value_type=str)

    robot_state_publisher_node = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        output = 'screen',
        parameters = [{
            'robot_description': robot_description,
            'use_sim_time': use_sim_time,
        }]
    )

    ld = LaunchDescription([
        declare_use_sim_time,
    ])
    
    ld.add_action(robot_state_publisher_node)

    return ld