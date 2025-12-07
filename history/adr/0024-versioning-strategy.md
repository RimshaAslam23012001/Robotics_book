### Title: Versioning Strategy (Single Version vs Multi-Version Release)

### Context:
The "Physical AI & Humanoid Robotics" book, built with Docusaurus, addresses rapidly evolving technologies like ROS 2, NVIDIA Isaac Sim, and various AI models. A clear strategy for managing content versions is crucial to maintain accuracy, prevent outdated information, and cater to readers using different software releases.

### Decision:
The book will primarily focus on a **single, continuously updated version** aligned with the latest stable releases of key technologies (e.g., ROS 2 Humble LTS). However, the architecture will be designed to **support multi-versioning capabilities of Docusaurus for future expansion**, allowing for the potential addition of older or alternative technology versions if needed, without maintaining multiple active branches simultaneously.

### Alternatives Considered:
*   **Strict Single Version**: Only ever maintaining one version of the book, which is updated in place, without any historical versions.
*   **Immediate Multi-Versioning**: Actively maintaining separate branches/versions for each major technology release (e.g., ROS 2 Humble, Iron, etc.) from the outset.

### Pros & Cons:
*   **Single, Continuously Updated Version (with Multi-versioning Support)**:
    *   **Pros**: Simplifies initial authoring and maintenance by focusing on one primary content stream. Ensures readers always access the most current information. Docusaurus's built-in versioning features provide a clear path for future expansion if multiple versions become necessary, without immediate overhead. Aligns with the dynamic nature of robotics and AI development.
    *   **Cons**: Readers on older technology versions might need to adapt examples, though core concepts remain relevant. Requires careful management to avoid breaking changes during continuous updates.
*   **Strict Single Version**:
    *   **Pros**: Easiest to maintain. Always current.
    *   **Cons**: No historical context for readers on older setups. High risk of breaking changes if a technology update fundamentally alters code examples.
*   **Immediate Multi-Versioning**:
    *   **Pros**: Caters directly to users on various technology versions. Provides historical stability.
    *   **Cons**: Extremely high maintenance burden (multiple content bases to update and synchronize). Significantly increases authoring effort. Can lead to content divergence and increased complexity.

### Impact:
*   The book's content will target the selected ROS 2 LTS distribution (Humble) and recent versions of Isaac Sim and other tools.
*   `docusaurus.config.js` will be configured to allow for versioning, but initially, only one active version will be published.
*   Updates to chapters due to new technology releases will be integrated directly into the single active version, with clear notes on changes if significant.

### Risks:
*   **Outdated Examples**: Despite continuous updates, some examples might fall slightly behind the absolute bleeding edge of technology. Mitigation involves frequent review and updates.
*   **Maintenance Effort**: Even with a single version, keeping content current in rapidly evolving fields requires effort. Claude Code automation will assist in this process.
*   **Reader Compatibility**: Readers using significantly older software might face compatibility issues. Mitigation involves clear disclaimers and guidance on target software versions.

### Rationale for Chosen Decision:
This versioning strategy provides a practical balance between ensuring the book is up-to-date and managing authoring complexity. Focusing on a single, continuously updated version ensures readers always receive relevant information for current best practices, while the built-in Docusaurus multi-versioning support offers a strategic option for future-proofing without incurring immediate overhead. This approach best serves the dynamic nature of physical AI and humanoid robotics by providing a current, authoritative resource.

### Status: Accepted