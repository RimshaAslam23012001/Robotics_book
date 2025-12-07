### Title: Humanoid Robot Model Choice (Unitree Go2/H1 vs Custom)

### Context:
To provide practical examples and hands-on labs for the "Physical AI & Humanoid Robotics" book, a specific humanoid robot model needs to be chosen for simulation and conceptual physical implementation. This decision influences the complexity of examples, accessibility for readers (cost of real hardware), and the level of detail required for kinematics and dynamics.

### Decision:
The book will primarily use **conceptual examples based on a generic humanoid robot model**, but will frequently reference and draw inspiration from the **Unitree Go2 and H1** robots for practical insights and discussion of real-world capabilities. This approach balances accessibility with practical relevance.

### Alternatives Considered:
*   **Unitree Go2**: A commercially available quadruped robot with advanced locomotion, often used for research and education. While not a true humanoid, it represents a step towards advanced physical AI.
*   **Unitree H1**: A commercially available humanoid robot with bipedal locomotion, offering advanced capabilities but at a higher cost and complexity.
*   **Custom Humanoid Models**: Designing and simulating entirely custom humanoid robots.

### Pros & Cons:
*   **Conceptual Generic Humanoid (with Unitree references)**:
    *   **Pros**: Maximizes accessibility for readers (no specific hardware required), simplifies early examples, allows focus on general robotics principles, Unitree references provide concrete real-world context.
    *   **Cons**: May lack the specific detailed mechanics of a real robot for advanced users, requires careful balancing to avoid being too abstract.
*   **Unitree Go2/H1 as Primary Focus**:
    *   **Pros**: Highly realistic and directly applicable examples, showcases cutting-edge commercial robotics, high educational value for those with access to or interest in these specific platforms.
    *   **Cons**: Significantly higher barrier to entry for readers (cost of hardware), increased complexity in simulation and control, potentially rapid model obsolescence.
*   **Custom Humanoid Models**:
    *   **Pros**: Full control over design and features, tailored to specific pedagogical goals.
    *   **Cons**: Extremely high development effort for creating and validating models, less direct relevance to existing commercial robots.

### Impact:
*   Simulation environments will include generic humanoid models with configurable parameters, alongside discussions of how these apply to robots like the Unitree Go2/H1.
*   Code examples will use standardized ROS 2 interfaces, making them adaptable to different URDFs, including those of Unitree robots.
*   The capstone project will be designed to be implementable on a generic humanoid simulation, with considerations for adapting it to specific commercial platforms.

### Risks:
*   **Abstraction Gap**: Over-reliance on generic models might make it difficult for readers to bridge to real-world robots. Mitigation involves strong connections between generic concepts and Unitree examples.
*   **Realism vs. Accessibility**: Balancing detailed realism with ease of use for a broad audience. This will be managed by providing layered complexity in labs and examples.

### Status: Accepted