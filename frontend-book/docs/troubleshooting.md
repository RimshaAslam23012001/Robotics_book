---
sidebar_position: 6
title: "Troubleshooting Guide: Physical AI & Humanoid Robotics"
---

# Troubleshooting Guide: Physical AI & Humanoid Robotics

## Overview
This guide provides solutions for common issues encountered when working with the Physical AI & Humanoid Robotics book project, including ROS 2 communication problems, simulation issues, perception challenges, and VLA system problems.

## Common Installation Issues

### ROS 2 Installation Problems
**Problem**: Unable to install ROS 2 packages
**Solution**:
```bash
# Update package lists
sudo apt update

# Install missing dependencies
sudo apt install python3-rosdep2
sudo rosdep init
rosdep update

# Source ROS 2 environment
source /opt/ros/humble/setup.bash
```

**Problem**: Workspace build fails
**Solution**:
```bash
# Clean the workspace
cd ~/robotics_ws
rm -rf build install log

# Rebuild with symlinks
colcon build --symlink-install
source install/setup.bash
```

## Simulation Issues

### Gazebo Problems
**Problem**: Gazebo fails to launch or runs very slowly
**Solution**:
1. Check GPU drivers are properly installed
2. Reduce physics update rate in world files:
   ```xml
   <physics name="1ms" type="ode">
     <max_step_size>0.01</max_step_size>  <!-- Increased from 0.001 -->
     <real_time_factor>0.5</real_time_factor>  <!-- Reduced for stability -->
   </physics>
   ```

**Problem**: Robot model not loading in Gazebo
**Solution**:
1. Verify URDF files are properly formatted
2. Check that all mesh files exist and are accessible
3. Ensure Gazebo plugins are properly referenced in URDF

### Sensor Simulation Issues
**Problem**: Sensor data not publishing
**Solution**:
1. Check that sensor plugins are loaded in Gazebo
2. Verify topic names match between simulation and nodes
3. Confirm sensor frames are properly defined in TF tree

## Communication Problems

### ROS 2 Network Issues
**Problem**: Nodes cannot communicate across machines
**Solution**:
1. Ensure ROS_DOMAIN_ID is the same on all machines
2. Check firewall settings allow ROS 2 traffic (UDP port 11811+)
3. Verify network configuration:
   ```bash
   # Check ROS 2 settings
   echo $ROS_DOMAIN_ID
   echo $ROS_LOCALHOST_ONLY
   ```

**Problem**: Topic connections are unstable
**Solution**:
1. Check QoS settings match between publishers and subscribers
2. Verify sufficient network bandwidth
3. Consider using reliable QoS for critical topics

### TF Tree Issues
**Problem**: TF tree is disconnected or missing transforms
**Solution**:
```bash
# Visualize the TF tree
ros2 run tf2_tools view_frames

# Check specific transforms
ros2 run tf2_ros tf2_echo <frame1> <frame2>
```

## Perception System Troubleshooting

### SLAM Problems
**Problem**: Map quality is poor or inconsistent
**Solution**:
1. Ensure robot has sufficient movement diversity for mapping
2. Check sensor data quality and frequency
3. Verify initial localization is stable before mapping

**Problem**: Loop closure not working
**Solution**:
1. Increase visual overlap between locations
2. Check that visual features are distinctive enough
3. Verify SLAM parameters for loop closure detection

### Object Detection Issues
**Problem**: Objects not detected reliably
**Solution**:
1. Check camera calibration parameters
2. Verify lighting conditions are adequate
3. Adjust detection thresholds and confidence levels

## Navigation Troubleshooting

### Path Planning Problems
**Problem**: Robot cannot find a path to goal
**Solution**:
1. Check that goal is in a free space in the map
2. Verify costmap parameters are appropriate
3. Ensure robot footprint is correctly defined

**Problem**: Robot gets stuck during navigation
**Solution**:
1. Check local planner parameters
2. Verify obstacle inflation settings
3. Increase oscillation and recovery timeouts

## VLA System Issues

### Speech-to-Text Problems
**Problem**: Voice commands not recognized
**Solution**:
1. Check audio input device is properly configured
2. Verify audio level is sufficient
3. Test with simple, clear commands first

**Problem**: High error rate in transcription
**Solution**:
1. Reduce background noise
2. Speak clearly and at moderate pace
3. Check audio input quality and format

### LLM Integration Issues
**Problem**: Commands not properly interpreted
**Solution**:
1. Use clear, unambiguous language
2. Provide sufficient context for complex tasks
3. Check that safety constraints are not overly restrictive

## Performance Optimization

### CPU Usage High
**Problem**: System performance is degraded
**Solutions**:
1. Reduce sensor data rates for non-critical sensors
2. Optimize perception pipeline for real-time performance
3. Use appropriate QoS settings to reduce overhead

### Memory Issues
**Problem**: System runs out of memory
**Solutions**:
1. Limit the size of data buffers
2. Use efficient data structures for point clouds
3. Monitor memory usage with `htop` or similar tools

## Debugging Tools

### ROS 2 Debugging
```bash
# Check all active nodes
ros2 node list

# Check all topics and their types
ros2 topic list -t

# Monitor topic data
ros2 topic echo /topic_name

# Check service availability
ros2 service list
```

### Visualization Tools
```bash
# Launch RViz for visualization
ros2 run rviz2 rviz2

# Monitor TF tree
ros2 run tf2_tools view_frames

# Check system performance
ros2 run rqt_plot rqt_plot
```

## Hardware-Specific Issues

### Jetson Platform Problems
**Problem**: Perception pipeline too slow on Jetson
**Solutions**:
1. Use TensorRT optimization for neural networks
2. Reduce sensor data resolution where possible
3. Optimize ROS 2 communication for edge deployment

**Problem**: Power consumption too high
**Solutions**:
1. Use appropriate CPU/GPU frequency scaling
2. Implement power-aware scheduling
3. Optimize algorithms for efficiency

## Simulation vs. Reality Gaps

### Sim-to-Real Transfer
**Problem**: Behavior differs between simulation and reality
**Solutions**:
1. Add noise models to simulation sensors
2. Include latency in simulation communication
3. Validate all parameters with physical robot when possible

## Getting Help

### Useful Commands
```bash
# Check ROS 2 environment
printenv | grep ROS

# Get detailed system information
ros2 doctor

# Check for common issues
ros2 run quality_of_service_demo_py check_qos_compatibility
```

### Community Resources
- ROS Discourse: https://discourse.ros.org/
- ROS Answers: https://answers.ros.org/
- Gazebo Community: https://community.gazebosim.org/
- NVIDIA Robotics: https://developer.nvidia.com/isaac

### Log Files
- ROS 2 logs: `~/.ros/log/`
- Gazebo logs: `~/.gazebo/log/`
- System logs: `/var/log/`

## When to Seek Further Help

Contact the development team or community if you encounter:
- Issues not covered in this guide
- Potential bugs in the provided code
- Feature requests for future improvements
- Performance issues that cannot be resolved with optimization