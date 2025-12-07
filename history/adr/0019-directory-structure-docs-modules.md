### Title: Directory Structure under /docs/module-1, module-2, etc.

### Context:
For the "Physical AI & Humanoid Robotics" book, a clear and consistent directory structure within the Docusaurus `docs/` folder is essential for content organization, navigation, and maintainability. This structure directly impacts how modules and chapters are accessed and managed.

### Decision:
The book's documentation content will be organized under the `/docs/` directory with a **module-based hierarchical structure**: `/docs/module-1/`, `/docs/module-2/`, `/docs/module-3/`, and `/docs/module-4/`. Each module directory will contain its respective chapters as Markdown/MDX files, alongside dedicated subdirectories for `images/`, `diagrams/`, and `labs/` at the root of the `/docs/` folder for shared assets.

### Alternatives Considered:
*   **Flat Structure**: All chapters directly under `/docs/` without module subdirectories.
*   **Chapter-specific asset folders**: Placing `images/`, `diagrams/`, `labs/` within each chapter's directory.
*   **Separate `content/` folder**: Using a different top-level folder for content, outside of `docs/`.

### Pros & Cons:
*   **Module-based Hierarchical Structure with Centralized Assets**:
    *   **Pros**: Clearly separates content by module, enhancing logical organization. Simplifies Docusaurus sidebar configuration. Centralized asset folders (`images/`, `diagrams/`, `labs/`) reduce redundancy and simplify asset management across chapters. Supports the book's 4-module pedagogical structure. Easy for readers to navigate.
    *   **Cons**: Requires careful planning to ensure assets are correctly linked from various chapters. The shared asset folders mean a slightly less granular organization for assets compared to chapter-specific folders.
*   **Flat Structure**:
    *   **Pros**: Very simple for a small number of files.
    *   **Cons**: Becomes unwieldy and difficult to navigate with a large number of chapters (10-15+ chapters). Does not reflect the modular structure of the book.
*   **Chapter-specific Asset Folders**:
    *   **Pros**: Assets are tightly coupled with their respective chapters, easy to find specific chapter assets.
    *   **Cons**: High redundancy of asset folders across many chapters. Can lead to scattered assets and make global asset management difficult. Increases total file count.
*   **Separate `content/` folder**:
    *   **Pros**: Cleaner separation from Docusaurus boilerplate if desired.
    *   **Cons**: Might require more custom configuration in Docusaurus, deviates from common Docusaurus practices.

### Impact:
*   All new content files (chapters, labs) will be created strictly according to this directory structure.
*   The `sidebars.js` configuration will be directly based on this hierarchy to generate the book's navigation.
*   Claude Code automation scripts for file generation will adhere to this pathing convention.

### Risks:
*   **Broken Asset Links**: Incorrect paths when referencing centralized assets from nested chapter directories. Mitigation requires careful relative pathing and robust internal linking conventions.
*   **Scalability for Labs/Diagrams**: If the number of labs or diagrams becomes extremely large, the centralized folders might become less organized. Mitigation involves further sub-categorization within `labs/` or `diagrams/` if needed.

### Rationale for Chosen Decision:
This modular and hierarchical directory structure is chosen to mirror the book's 4-module pedagogical design, providing a logical and intuitive organization for both authors and readers. Centralizing shared assets like images, diagrams, and labs streamlines management and reduces redundancy, while the Docusaurus framework inherently supports and benefits from such a well-defined content hierarchy, ensuring easy navigation and future scalability.

### Status: Accepted