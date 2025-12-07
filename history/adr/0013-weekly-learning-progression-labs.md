### Title: Inclusion of Weekly Learning Progression + Labs

### Context:
To maximize the educational value and engagement of the "Physical AI & Humanoid Robotics" book, a structured learning progression is essential. The plan specifies aligning each module with a weekly teaching plan and including hands-on labs. This decision impacts the book's pedagogical approach, practical utility, and its suitability for use in structured courses.

### Decision:
The book will explicitly incorporate a **weekly learning progression for each module**, complemented by **dedicated hands-on labs** for every chapter where applicable. This pedagogical approach reinforces theoretical concepts with practical application, allowing readers to build skills incrementally and apply learned material immediately.

### Alternatives Considered:
*   **Theory-only chapters**: Focusing solely on conceptual explanations without practical exercises.
*   **Separate lab manual**: Providing labs in a standalone document or section.
*   **Ad-hoc labs**: Including labs only when convenient, without a consistent schedule or integration.

### Pros & Cons:
*   **Weekly Learning Progression + Integrated Labs**:
    *   **Pros**: Enhances active learning and skill development. Provides a clear roadmap for self-learners and instructors. Increases engagement and retention of complex material. Directly supports the "Educational Value First" principle from the Constitution. Labs provide verifiable code examples and practical experience.
    *   **Cons**: Requires significant effort to design and maintain labs for each chapter. Labs must be consistently tested and updated to remain relevant. Can increase the overall length and complexity of the book.
*   **Theory-only chapters**:
    *   **Pros**: Focuses solely on conceptual depth, potentially covering more theoretical topics. Simpler to author and maintain.
    *   **Cons**: Lacks practical application, potentially leading to lower engagement and skill development. Less suitable for hands-on learners or course adoption.
*   **Separate lab manual**:
    *   **Pros**: Keeps theoretical content clean and separate. Labs can be updated independently.
    *   **Cons**: Disconnect between theory and practice. Requires readers to juggle multiple resources. May reduce the seamless flow of learning.
*   **Ad-hoc labs**:
    *   **Pros**: Flexibility in lab inclusion.
    *   **Cons**: Inconsistent learning experience. May leave gaps in practical skill development. Reduces the structured pedagogical value.

### Impact:
*   Every chapter will be evaluated for opportunities to include a hands-on lab or practical exercise.
*   The `/docs/labs/` directory will be a core part of the book's file structure.
*   The weekly progression will be implicitly or explicitly outlined, guiding readers through the modules at a manageable pace.
*   Assessment checkpoints will often be tied to the completion or understanding of lab exercises.

### Risks:
*   **Lab Maintenance**: Labs require constant testing and updates to ensure compatibility with evolving software (ROS 2, simulators) and hardware. Mitigation includes automation for testing and a clear maintenance strategy.
*   **Prerequisite Gaps**: Readers might struggle with labs if prerequisites are not clearly defined or if foundational knowledge is weak. Mitigation involves rigorous prerequisite sections for each chapter and lab.
*   **Computational Resources**: Some labs might require significant computational resources, potentially impacting accessibility. Mitigation includes providing simpler alternatives or cloud-based solutions where possible.

### Rationale for Chosen Decision:
This decision is critical for fulfilling the book's commitment to "Educational Value First" and "Structured Learning." By integrating a weekly learning progression with hands-on labs, the book moves beyond theoretical concepts to enable practical skill acquisition. This active learning approach is proven to enhance understanding and retention, making the book an invaluable resource for both self-study and formal education in physical AI and humanoid robotics.

### Status: Accepted