from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    return LaunchDescription([
        # Launch the robot state publisher node
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'use_sim_time': True
            }],
            output='screen'
        ),

        # Launch the joint state publisher node
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{
                'use_sim_time': True
            }],
            output='screen'
        ),

        # Launch a simple controller for the robot
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            name='ros2_control_node',
            parameters=[{
                'use_sim_time': True
            }],
            output='screen'
        )
    ])