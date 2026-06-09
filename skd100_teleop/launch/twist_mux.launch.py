from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value = 'False',
        description = 'Use simulation (Gazebo) clock if true'
    )

    twist_mux_params_file = PathJoinSubstitution(
        [FindPackageShare('skd100_teleop'), 'config', 'twist_mux.yaml']
    )

    twist_mux_node = Node(
        package = "twist_mux",
        executable = "twist_mux",
        parameters = [
            {
                'use_sim_time': use_sim_time,
                'use_stamped': True,
            },
            twist_mux_params_file,
        ],
        # Default publisher for twist_mux is /cmd_vel_out
        # Rename so it matches skd_base_controller topic
        remappings=[
            ('/cmd_vel_out','/skd_base_controller/cmd_vel'),
        ],
    )
    
    ld = LaunchDescription([
        declare_use_sim_time,
    ])
    
    ld.add_action(twist_mux_node)
    
    return ld