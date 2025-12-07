### Title: Simulation Engine Criteria (Gazebo vs Unity vs NVIDIA Isaac Sim)

### Context:
The "Physical AI & Humanoid Robotics" book project requires a robust simulation environment to develop and test robotic concepts. The choice of simulation engine directly impacts realism, integration capabilities, supported features (physics, sensors, rendering), and the learning curve for readers. The book will cover simulated environments extensively.

### Decision:
The project will primarily utilize **NVIDIA Isaac Sim** for advanced robotics simulation, with **Gazebo** used for foundational ROS 2 examples due to its tight integration with ROS. **Unity** may be referenced for specific use cases requiring high-fidelity rendering or specific game development tools, but will not be the primary focus.

### Alternatives Considered:
*   **Gazebo**: A widely used, open-source robotics simulator tightly integrated with ROS, offering realistic physics and sensor models.
*   **Unity**: A powerful game development engine capable of high-fidelity graphics and physics, with some robotics extensions and ROS integrations (e.g., Unity Robotics Hub).
*   **NVIDIA Isaac Sim**: A robotics simulation platform built on NVIDIA Omniverse, offering highly accurate physics (PhysX 5), photorealistic rendering (RTX), and seamless integration with NVIDIA's AI and robotics ecosystem (Isaac ROS, Omniverse).

### Pros & Cons:
*   **Gazebo**:
    *   **Pros**: Deep ROS integration, mature ecosystem, open-source, good for basic robotics and traditional control.
    *   **Cons**: Graphical fidelity can be limited, steeper learning curve for advanced rendering, less focus on AI integration compared to Isaac Sim.
*   **Unity**:
    *   **Pros**: Excellent graphics and visualization, strong community for game development, flexible for custom environments.
    *   **Cons**: ROS integration requires external packages, potentially less focus on robotics-specific physics accuracy out-of-the-box, proprietary.
*   **NVIDIA Isaac Sim**:
    *   **Pros**: Superior physics and rendering, native integration with NVIDIA AI (Isaac ROS), excellent for sim-to-real transfer, strong API for programmatic control, scalable via Omniverse.
    *   **Cons**: Proprietary, requires NVIDIA hardware, higher resource demands, potentially steeper initial learning curve for those unfamiliar with Omniverse.

### Impact:
*   Core simulation examples and labs will be developed in Isaac Sim, showcasing its advanced capabilities.
*   Introductory ROS 2 simulation content will use Gazebo to leverage its strong ROS integration and widespread adoption.
*   The book will highlight the strengths of each simulator and guide readers on when to choose which for specific tasks.
*   Requires readers to have access to NVIDIA hardware for optimal Isaac Sim experience.

### Risks:
*   **Hardware dependency**: Reliance on NVIDIA Isaac Sim might exclude readers without compatible hardware. This will be mitigated by providing alternatives (Gazebo) and clearly stating hardware requirements.
*   **Complexity**: Integrating multiple simulators (Gazebo and Isaac Sim) could increase complexity for both authors and readers. Mitigation involves clear module separation and focused examples for each simulator.
*   **Licensing/Cost**: Isaac Sim is proprietary; this should be transparently communicated.

### Status: Accepted