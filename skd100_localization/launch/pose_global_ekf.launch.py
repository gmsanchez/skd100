from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node


def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default = False)
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value = use_sim_time,
        description = 'Use simulation (Gazebo) clock if true'
    )
    
    pose_global_ekf_params = PathJoinSubstitution(
        [FindPackageShare("skd100_localization"), "config", "pose_global_ekf.yaml"],
    )

    global_ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='global_ekf_filter_node',
        parameters = [
            {'use_sim_time': use_sim_time},
            pose_global_ekf_params,
        ],
        remappings=[
            # Input sensors
            ("odom", "/odometry/local"),
            ("pose", "/pose"),
            # Filter output
            ("odometry/filtered", "odometry/global"),
        ],
        output='screen',
    )
    
    ld = LaunchDescription([
        declare_use_sim_time,
    ])
    
    ld.add_action(global_ekf_node)

    return ld
