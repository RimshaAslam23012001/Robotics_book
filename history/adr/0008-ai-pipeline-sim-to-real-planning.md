### Title: AI Pipeline Approach - Sim-to-Real Transfer (RL vs Modular Planning)

### Context:
A critical challenge in humanoid robotics is transferring policies learned in simulation to physical robots (sim-to-real transfer). The "Physical AI & Humanoid Robotics" book needs to address different methodologies for this, as the chosen approach impacts the robustness, generalization, and training data requirements for robotic control systems.

### Decision:
The book will advocate for and demonstrate a **hybrid approach to sim-to-real transfer**, emphasizing **modular planning and control architectures** (e.g., hierarchical task planning, state machines, inverse kinematics/dynamics solvers) for robustness and interpretability, complemented by **Reinforcement Learning (RL)** for optimizing specific low-level skills (e.g., locomotion gaits, fine manipulation) within a safe and constrained learning environment. Domain randomization and adaptation techniques will be covered for bridging the reality gap.

### Alternatives Considered:
*   **Pure Reinforcement Learning (RL)**: Learning end-to-end policies directly in simulation and transferring them.
*   **Exclusively Modular/Classical Planning**: Relying solely on symbolic planning, inverse kinematics, and predefined controllers.

### Pros & Cons:
*   **Hybrid Approach (Modular Planning + Selective RL)**:
    *   **Pros**: Combines the strengths of both: modularity provides interpretability, safety, and robustness for high-level tasks, while RL can optimize challenging low-level behaviors. Easier to debug and verify. More practical for current complex robotics tasks.
    *   **Cons**: Requires careful decomposition of tasks and integration of different paradigms, potentially more complex to set up initially than a pure end-to-end RL system.
*   **Pure Reinforcement Learning (RL)**:
    *   **Pros**: Potentially capable of discovering highly optimized or novel behaviors, simpler end-to-end learning framework.
    *   **Cons**: Can be data-intensive, challenging to achieve zero-shot sim-to-real transfer, policies can be opaque and difficult to debug, often requires significant domain randomization or real-world fine-tuning to overcome the reality gap.
*   **Exclusively Modular/Classical Planning**:
    *   **Pros**: Highly interpretable, predictable, provably safe (in many cases), well-established methodologies.
    *   **Cons**: Can be brittle to environmental variations, difficult to hand-engineer solutions for highly dynamic or complex tasks (e.g., highly agile locomotion), less adaptable to unforeseen situations.

### Impact:
*   The book will present a VLA pipeline where high-level LLM plans are broken down into sub-tasks managed by a modular control architecture.
*   Specific sections will be dedicated to RL for learning skills, demonstrating how these skills can be integrated into the broader modular framework.
*   Techniques like domain randomization in Isaac Sim will be used to enhance sim-to-real transfer capabilities for RL-learned policies.

### Risks:
*   **Integration Complexity**: Combining RL with modular planning requires careful design and interfaces. Mitigation involves clear architectural patterns and examples.
*   **Reality Gap**: Despite domain randomization, residual differences between simulation and reality can lead to performance degradation. The book must discuss strategies for detection and mitigation.
*   **Training Data**: RL still requires significant interaction data, which needs to be generated efficiently in simulation. This will tie into the discussion of Isaac Sim's capabilities.

### Status: Accepted