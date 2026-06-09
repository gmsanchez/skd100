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
    
    joy_vel = LaunchConfiguration('joy_vel')
    declare_joy_vel = DeclareLaunchArgument(
        'joy_vel',
        default_value = 'cmd_vel_joy',
        description = 'Joy velocity topic'
    )
    
    joy_config = LaunchConfiguration('joy_config')
    declare_joy_config = DeclareLaunchArgument(
        'joy_config',
        default_value = 'FS-i6X.config.yaml',
        description = 'Joy param file (into "config" folder)'
    )
    
    joy_dev = LaunchConfiguration('joy_dev')
    declare_joy_dev = DeclareLaunchArgument(
        'joy_dev',
        default_value = '/dev/input/js0',
        description = 'Joy device'
    )
    
    ARGUMENTS = [
        declare_use_sim_time,
        declare_joy_vel,
        declare_joy_config,
        declare_joy_dev,
    ]

    spawn_joy_node = Node(
        package = 'joy',
        executable = 'joy_node',
        name = 'joy_node',
        parameters = [{
            'use_sim_time': use_sim_time,
            'dev': joy_dev,
            'deadzone': 0.05,
            'autorepeat_rate': 20.0,
            # This option is added because of
            # https://github.com/ros2/teleop_twist_joy/issues/37
            # https://github.com/ros-drivers/joystick_drivers/issues/263
            # https://github.com/ros-drivers/joystick_drivers/pull/266
            'init': True,

        }],
    )
    
    teleop_twist_joy_params_file = PathJoinSubstitution(
        [FindPackageShare('skd100_teleop'), 'config', joy_config]
    )
    
    teleop_twist_joy_node = Node(
        package = 'teleop_twist_joy',
        executable = 'teleop_node',
        name = 'teleop_twist_joy_node',
        parameters = [
            {
                'use_sim_time': use_sim_time,
                'publish_stamped_twist': True,
            },
            teleop_twist_joy_params_file,
        ],
        remappings = {
            ('/cmd_vel', joy_vel),
        },
    )
    
    ld = LaunchDescription(ARGUMENTS)
    
    ld.add_action(spawn_joy_node)
    ld.add_action(teleop_twist_joy_node)

    return ld
