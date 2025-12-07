### Title: Edge Compute Platform (Jetson Orin Nano vs Orin NX)

### Context:
The "Physical AI & Humanoid Robotics" book will discuss and provide examples for deploying AI models and robotic control systems on edge devices, particularly for physical humanoid robots. The choice of edge compute platform significantly impacts the performance, power consumption, cost, and complexity of deployment for the target applications.

### Decision:
The book will primarily focus on the **NVIDIA Jetson Orin Nano** for its excellent balance of AI performance, power efficiency, and cost-effectiveness, making it accessible for a broader audience. The **Jetson Orin NX** will be discussed as a higher-performance alternative for more demanding applications.

### Alternatives Considered:
*   **NVIDIA Jetson Orin NX**: Offers higher AI performance and more memory bandwidth compared to the Orin Nano.
*   **Other SBCs (e.g., Raspberry Pi, Coral Dev Board)**: Less specialized for NVIDIA's AI ecosystem (CUDA, TensorRT, Isaac ROS) which is central to the book's advanced topics.

### Pros & Cons:
*   **NVIDIA Jetson Orin Nano**:
    *   **Pros**: Highly cost-effective, excellent performance for its price point (up to 40 TOPS), low power consumption, fully compatible with NVIDIA's AI software stack (CUDA, cuDNN, TensorRT), ideal for introductory to intermediate edge AI robotics.
    *   **Cons**: Lower raw performance and memory capacity compared to Orin NX, may be a bottleneck for very large or complex AI models.
*   **NVIDIA Jetson Orin NX**:
    *   **Pros**: Significantly higher AI performance (up to 100 TOPS), more memory and bandwidth, suitable for complex multi-sensor AI pipelines and higher-fidelity models.
    *   **Cons**: Higher cost, higher power consumption, potentially overkill for simpler examples.

### Impact:
*   Labs and examples related to edge deployment will be designed and tested primarily on the Jetson Orin Nano, ensuring broad accessibility.
*   The book will provide guidance on scaling up to the Orin NX for more demanding tasks, discussing the performance benefits and considerations.
*   Focuses on the NVIDIA ecosystem, aligning with the use of NVIDIA Isaac Sim for simulation.

### Risks:
*   **Performance limitations**: Readers attempting highly complex AI tasks on the Orin Nano might hit performance ceilings. Mitigation involves clear performance expectations and recommendations for when to upgrade to Orin NX.
*   **Hardware availability/cost**: While Orin Nano is cost-effective within its class, it still represents an investment for readers. Alternatives like cloud-based inference will be mentioned where appropriate.

### Status: Accepted