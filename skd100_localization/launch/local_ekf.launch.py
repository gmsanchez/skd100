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
    
    local_ekf_params = PathJoinSubstitution(
        [FindPackageShare("skd100_localization"), "config", "local_ekf.yaml"],
    )

    local_ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='local_ekf_filter_node',
        parameters = [
            {'use_sim_time': use_sim_time},
            local_ekf_params,
        ],
        remappings=[
            # Input sensors
            ("odom", "/skd_base_controller/odom"),
            ("imu/data", "mti_630_8A1G6/imu/data"),
            # Filter output
            ("odometry/filtered", "odometry/local"),
        ],
        output='screen',
    )
    
    ld = LaunchDescription([
        declare_use_sim_time,
    ])
    
    ld.add_action(local_ekf_node)

    return ld
