### Title: Sensor Suite Selection (LiDAR, Depth Cameras, IMUs)

### Context:
For the "Physical AI & Humanoid Robotics" book, a foundational understanding of robotic perception is crucial. This requires selecting a representative set of sensors to be covered in simulation and conceptual discussions. The choice of sensors impacts the types of perception tasks the robot can perform, the complexity of data processing, and the relevance to real-world humanoid robotics applications.

### Decision:
The book will primarily focus on a sensor suite comprising **depth cameras (e.g., Intel RealSense, NVIDIA Isaac Realsense simulation), LiDAR (2D and 3D), and Inertial Measurement Units (IMUs)**. These sensors provide a comprehensive foundation for various perception tasks in humanoid robotics.

### Alternatives Considered:
*   **Monocular Cameras**: Simpler, but lack direct depth information.
*   **Stereo Cameras (without depth processing)**: Provide two images for depth estimation, but often require more complex processing than active depth cameras.
*   **Force/Torque Sensors**: Important for manipulation and interaction, but will be covered as a secondary topic rather than a primary perception input for foundational modules.
*   **Radar**: Less common in current humanoid robotics for general perception compared to optical/LiDAR.

### Pros & Cons:
*   **Depth Cameras**:
    *   **Pros**: Provide dense 3D point cloud data and RGB images, excellent for object detection, manipulation, and local navigation. Widely used and accessible.
    *   **Cons**: Range limitations (especially outdoors), can be affected by ambient light, data can be noisy.
*   **LiDAR (2D and 3D)**:
    *   **Pros**: Highly accurate distance measurements, robust in various lighting conditions, essential for mapping (SLAM) and long-range obstacle avoidance. 3D LiDAR provides full volumetric data.
    *   **Cons**: Generally more expensive, 2D LiDAR provides limited vertical information, data sparsity can be an issue.
*   **IMUs (Inertial Measurement Units)**:
    *   **Pros**: Essential for odometry, attitude estimation, balance, and control. Provides critical data on orientation, acceleration, and angular velocity.
    *   **Cons**: Suffers from drift over time, requires fusion with other sensors for accurate global pose estimation.

### Impact:
*   Labs and examples will demonstrate how to acquire, process, and utilize data from depth cameras, LiDAR, and IMUs within ROS 2 and simulation environments.
*   Discussions on perception algorithms (e.g., object recognition, SLAM, state estimation) will be framed around the data types provided by these sensors.
*   The capstone project will integrate these sensor modalities for comprehensive robotic perception.

### Risks:
*   **Sensor Noise/Error**: Real-world sensors are noisy; simulations need to accurately model this. The book must emphasize filtering and data fusion techniques.
*   **Data Volume**: Processing 3D data from depth cameras and 3D LiDAR can be computationally intensive, requiring discussions on optimization and efficient algorithms.

### Status: Accepted