### Title: ROS 2 Distribution Choice (Humble vs Iron)

### Context:
The book project "Physical AI & Humanoid Robotics" requires selecting a stable and widely supported ROS 2 distribution for all examples, labs, and architectural discussions. This decision impacts the long-term maintainability of code examples, compatibility with other robotics software (Gazebo, Isaac Sim), and the target audience's ease of following along.

### Decision:
The project will standardize on **ROS 2 Humble Hawksbill** as the primary distribution.

### Alternatives Considered:
*   **ROS 2 Iron Irwini**: A newer distribution, offering recent features and improvements.

### Pros & Cons:
*   **ROS 2 Humble Hawksbill**:
    *   **Pros**: Long Term Support (LTS) release, highly stable, extensive community support, well-documented, widely used in industry and academia, good compatibility with existing tools and libraries.
    *   **Cons**: Slightly older features compared to Iron, potentially slower adoption of very new hardware or software.
*   **ROS 2 Iron Irwini**:
    *   **Pros**: Latest features, improved performance, newer drivers/tooling support.
    *   **Cons**: Shorter support window (non-LTS), less mature ecosystem, potentially more breaking changes or compatibility issues, less community support initially.

### Impact:
*   All ROS 2 code examples, configurations, and tutorials in the book will be based on Humble.
*   Readers will be advised to use Humble for consistency.
*   Ensures a stable foundation for the book's content, reducing the likelihood of examples breaking due to rapid changes in ROS 2.
*   Might require mentioning differences or upgrade paths for users on newer distributions.

### Risks:
*   **Outdated features**: Newer ROS 2 features introduced after Humble might not be covered directly. This can be mitigated by referencing newer features and providing migration notes.
*   **Future compatibility**: While LTS, eventual transition to a newer LTS release will be necessary for long-term project viability beyond the book's initial lifespan.

### Status: Accepted