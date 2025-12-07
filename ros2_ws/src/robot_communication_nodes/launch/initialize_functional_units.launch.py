from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Launch the publisher node
        Node(
            package='robot_communication_nodes',
            executable='publisher_node',
            name='publisher_node',
            output='screen'
        ),

        # Launch the subscriber node
        Node(
            package='robot_communication_nodes',
            executable='subscriber_node',
            name='subscriber_node',
            output='screen'
        ),

        # Launch the service server node
        Node(
            package='robot_communication_nodes',
            executable='service_server_node',
            name='service_server_node',
            output='screen'
        ),

        # Launch the service client node
        Node(
            package='robot_communication_nodes',
            executable='service_client_node',
            name='service_client_node',
            output='screen'
        ),

        # Launch the communication monitoring node
        Node(
            package='robot_communication_nodes',
            executable='monitor_node',
            name='monitor_node',
            output='screen'
        )
    ])