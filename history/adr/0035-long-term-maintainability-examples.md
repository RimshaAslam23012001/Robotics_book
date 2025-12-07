### Title: Long-term Maintainability of Examples (ROS Updates, Isaac Releases)

### Context:
The "Physical AI & Humanoid Robotics" book contains numerous code examples, tutorials, and practical exercises that rely on specific versions of ROS 2, NVIDIA Isaac Sim, and other rapidly evolving technologies. These technologies undergo regular updates, version changes, and sometimes breaking changes that can render existing examples non-functional. The book must remain useful and accurate over time despite ongoing development in the underlying technologies, requiring a strategy for maintaining example code and exercises as the ecosystem evolves.

### Decision:
The project will implement a **long-term maintainability strategy** for all examples, focusing on creating robust, version-aware code that can adapt to updates in ROS 2, Isaac Sim, and related technologies. This includes writing examples with clear version requirements, implementing abstraction layers where appropriate, and establishing processes for tracking and updating examples when underlying technologies change.

### Alternatives Considered:
*   **Version Locking**: Locking all examples to specific, unchanging versions of dependencies.
*   **Frequent Complete Overhauls**: Periodically rewriting all examples to match the latest technology versions.
*   **Minimal Maintenance**: Creating examples without specific maintenance strategies, accepting that they may break over time.
*   **Community Maintenance**: Relying primarily on community contributions to update examples.
*   **Documentation-Only Approach**: Focusing on concepts rather than detailed, runnable examples.

### Pros & Cons:
*   **Long-term Maintainability Strategy**:
    *   **Pros**: Ensures examples remain functional over time. Reduces frustration for readers encountering broken code. Maintains the book's educational value across technology updates. Provides clear guidance on version compatibility. Enables systematic updates when technologies change. Builds in adaptability to breaking changes. Supports the living document workflow.
    *   **Cons**: Requires additional development time to create maintainable examples. May add complexity to simple examples for the sake of maintainability. Requires ongoing maintenance processes and resources. May slow down initial content creation.
*   **Version Locking**:
    *   **Pros**: Examples remain stable and predictable. No risk of breaking due to external updates. Easiest to implement initially.
    *   **Cons**: Examples become outdated as technologies advance. Readers may learn obsolete practices. Creates security risks if locked versions have vulnerabilities. Doesn't reflect current best practices.
*   **Frequent Complete Overhauls**:
    *   **Pros**: Ensures all examples use current best practices. Maintains relevance with latest features.
    *   **Cons**: Resource-intensive process. Creates periods where content may be inconsistent. Disruptive to readers who started with earlier versions.
*   **Minimal Maintenance**:
    *   **Pros**: Fastest path to initial publication. No additional maintenance overhead.
    *   **Cons**: Examples likely to break over time. Reduces book's educational value. Frustrates readers with non-functional code.
*   **Community Maintenance**:
    *   **Pros**: Distributes maintenance burden. Leverages community expertise.
    *   **Cons**: Inconsistent maintenance quality and timing. May not address core examples. Reliability depends on community engagement.

### Impact:
*   All examples will include clear version requirements and compatibility notes.
*   Code examples will be designed with abstraction layers where appropriate to minimize impact of API changes.
*   A systematic process will be established for monitoring technology updates and their impact on examples.
*   Examples will be tested against new versions of key technologies when updates are released.
*   Documentation will include guidance on adapting examples to different technology versions.
*   Version control practices will track changes to examples over time.
*   Claude Code automation will assist in identifying examples that need updates when technologies change.

### Risks:
*   **Maintenance Overhead**: The maintainability strategy may require significant ongoing resources. Mitigation involves automating where possible and focusing on the most critical examples.
*   **Complexity in Examples**: Maintainability requirements might make simple examples unnecessarily complex. Mitigation includes balancing maintainability with educational clarity.
*   **Technology Changes**: Some updates might require significant example rewrites despite maintainability efforts. Mitigation involves modular design that isolates components likely to change.

### Rationale for Chosen Decision:
The long-term maintainability strategy is essential for the "Physical AI & Humanoid Robotics" book because it operates in technology domains where updates and changes are frequent and significant. Unlike books on stable technologies, this book must remain functional and educational despite ongoing evolution in ROS 2, Isaac Sim, and related frameworks. The maintainability strategy ensures that readers can successfully execute examples and learn from them regardless of when they access the book, supporting the "Educational Value First" principle by maintaining the book's practical utility over time. This approach also aligns with the continuous iteration and living document workflow adopted for the project.

### Status: Accepted