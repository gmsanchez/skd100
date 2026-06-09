from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value = 'False',
        description = 'Use simulation (Gazebo) clock if true'
    )
    
    skd100_description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare("skd100_description"),
                "launch",
                "description.launch.py"
            ])
        ]),
        launch_arguments = {
            'use_sim_time': use_sim_time
        }.items(),
    )
        
    skd100_controller_params = PathJoinSubstitution(
        [FindPackageShare("skd100_control"), "config", "controllers.yaml"],
    )

    # From https://github.com/husarion/rosbot_hardware_interfaces
    controller_manager_node = Node(
        package = "controller_manager",
        executable = "ros2_control_node",
        parameters = [
            {'use_sim_time': use_sim_time},
            skd100_controller_params,
        ],
        arguments = ['--ros-args', '--log-level', 'WARN'],
    )

    spawn_joint_state_broadcaster_node = Node(
        package = "controller_manager",
        executable = "spawner",
        arguments = [
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    spawn_skd_base_controller_node = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "skd_base_controller",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    # Delay start of robot_controller after joint_state_broadcaster
    delay_robot_controller_spawner_after_joint_state_broadcaster_spawner = (
        RegisterEventHandler(
            event_handler = OnProcessExit(
                target_action = spawn_joint_state_broadcaster_node,
                on_exit = [spawn_skd_base_controller_node],
            )
        )
    )

    ld = LaunchDescription([
        declare_use_sim_time,
    ])
    
    ld.add_action(skd100_description)
    ld.add_action(controller_manager_node)
    ld.add_action(spawn_joint_state_broadcaster_node)
    ld.add_action(delay_robot_controller_spawner_after_joint_state_broadcaster_spawner)
    
    return ld
