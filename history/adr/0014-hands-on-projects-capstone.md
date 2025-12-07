### Title: Hands-on Projects: Simulation → AI → VLA → Humanoid Capstone

### Context:
A key element of the "Physical AI & Humanoid Robotics" book's pedagogical approach is the inclusion of hands-on projects that progressively build reader skills. The culminating project, a humanoid capstone, requires a well-defined progression from basic simulation to advanced Vision-Language-Action (VLA) integration on a humanoid platform. This decision outlines the design philosophy and structure for these practical experiences.

### Decision:
The book will feature a series of progressively complex **hands-on projects**, culminating in a **humanoid capstone project**. These projects will follow a distinct progression: from foundational **simulation** exercises, to integrating **AI perception**, then building full **VLA pipelines**, and finally applying these concepts to a simulated **humanoid robot**. This ensures a coherent and challenging learning path.

### Alternatives Considered:
*   **Single large project**: One comprehensive project introduced early, with all concepts taught within its scope.
*   **Disjointed projects**: Independent projects scattered throughout the book, without a clear overarching theme or progression.
*   **Theory-only approach**: Eliminating hands-on projects in favor of purely theoretical discussions.

### Pros & Cons:
*   **Progressive Hands-on Projects (Sim → AI → VLA → Humanoid Capstone)**:
    *   **Pros**: Builds skills incrementally, allowing readers to master concepts step-by-step. Motivates learning by demonstrating practical application at each stage. The capstone provides a comprehensive integration challenge. Aligns with the structured learning and educational value principles.
    *   **Cons**: Requires careful design to ensure a smooth difficulty curve. Each project needs to be self-contained yet contribute to the overall capstone. Can be resource-intensive for readers (computation, time).
*   **Single large project**:
    *   **Pros**: Strong overarching theme. All concepts are directly relevant to one goal.
    *   **Cons**: Can be overwhelming for beginners. Difficulty in breaking down complex tasks. May limit the breadth of topics covered.
*   **Disjointed projects**:
    *   **Pros**: Flexibility in project topics. Readers can choose projects of interest.
    *   **Cons**: Lacks continuity and cumulative skill building. May not provide a holistic understanding of system integration.
*   **Theory-only approach**:
    *   **Pros**: Focuses purely on conceptual depth.
    *   **Cons**: Significantly reduces practical skill development and engagement. Less effective for complex engineering topics.

### Impact:
*   Specific sections and labs in each module will be dedicated to these progressive project components.
*   The capstone project will be detailed with clear objectives, required components (simulators, sensors, AI models), and success criteria.
*   Tools like Claude Code will be used to scaffold project files and provide guidance.
*   The project structure will directly feed into the book's task generation and quality validation phases.

### Risks:
*   **Project Scope Creep**: Ensuring projects remain manageable within the book's scope without becoming overly complex or time-consuming. Mitigation involves clear project definitions and strict adherence to objectives.
*   **Complexity Barrier**: Some readers might find the capstone project too challenging if foundational steps aren't thoroughly grasped. Mitigation includes providing robust intermediate projects and extensive support materials.
*   **Technology Volatility**: Projects reliant on specific software versions (ROS 2, Isaac Sim, LLM APIs) might become outdated. Mitigation involves designing projects with stable interfaces and providing update guides.

### Rationale for Chosen Decision:
This progressive project-based approach, culminating in a humanoid capstone, is fundamental to the book's promise of delivering practical skills in physical AI and humanoid robotics. It ensures that readers not only understand theoretical concepts but also gain hands-on experience in building, integrating, and testing complex robotic systems. This structured journey from simulation fundamentals to advanced VLA on a humanoid platform provides a highly effective and engaging learning experience, directly addressing the core goal of educational value and practical application.

### Status: Accepted