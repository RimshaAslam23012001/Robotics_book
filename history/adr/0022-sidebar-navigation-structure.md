### Title: Sidebar Structure for Navigation

### Context:
The "Physical AI & Humanoid Robotics" book, built with Docusaurus, requires an intuitive and consistent sidebar navigation to guide readers through its modular structure (4 modules, 3-4 chapters each). The sidebar is critical for user experience, content discoverability, and reinforcing the book's pedagogical flow.

### Decision:
The Docusaurus sidebar will be structured hierarchically, mirroring the **4-module and chapter breakdown**. Each module will be a top-level category in the sidebar, with its respective chapters nested as individual links. This design ensures that navigation is predictable, aligns with the book's content architecture, and facilitates easy access to all sections.

### Alternatives Considered:
*   **Flat Sidebar**: Listing all chapters directly in the sidebar without module categories.
*   **Tag-based Sidebar**: Grouping content by keywords or tags instead of a rigid hierarchical structure.
*   **Dynamic Sidebar**: Generating sidebar links based on detected headings within MDX files, rather than explicit configuration.

### Pros & Cons:
*   **Module-based Hierarchical Sidebar**:
    *   **Pros**: Directly reflects the book's logical structure, making it easy for readers to understand content organization. Provides a clear progression through the modules and chapters. Enhances content discoverability. Easy to configure and maintain in Docusaurus's `sidebars.js` file. Supports the "Structured Learning" principle.
    *   **Cons**: Less flexible for non-linear reading paths, though search can mitigate this. Requires all content to fit neatly into the module/chapter structure.
*   **Flat Sidebar**:
    *   **Pros**: Simplest to implement for a small number of pages.
    *   **Cons**: Becomes unwieldy and overwhelming for a book with 10-15+ chapters. Lacks logical grouping, making navigation difficult and confusing for readers.
*   **Tag-based Sidebar**:
    *   **Pros**: Highly flexible for cross-referencing topics. Supports multiple ways of organizing content.
    *   **Cons**: Can be inconsistent and less intuitive for a structured educational book. Relies heavily on accurate tagging. Harder to ensure a linear learning path.
*   **Dynamic Sidebar**:
    *   **Pros**: Automatically adapts to content changes. Less manual configuration.
    *   **Cons**: Less explicit control over the navigation hierarchy. Might not always produce the desired pedagogical flow. Can lead to unpredictable sidebar items.

### Impact:
*   The `sidebars.js` file will be meticulously configured to define the module and chapter hierarchy.
*   Any new chapters or modules added to the book will require updates to `sidebars.js`.
*   Claude Code automation will include mechanisms to update `sidebars.js` when new content files are generated.
*   The visual layout of the Docusaurus theme will be optimized to display this hierarchical structure clearly.

### Risks:
*   **Configuration Errors**: Manual errors in `sidebars.js` can lead to broken navigation. Mitigation involves validation scripts and careful review.
*   **Maintenance Burden**: As the book grows, `sidebars.js` could become large. Mitigation includes modularizing the `sidebars.js` file itself or using Docusaurus features for automatic grouping where appropriate.
*   **Stale Navigation**: If content is moved or renamed without updating `sidebars.js`, navigation can break. Mitigation through automated checks and consistent naming conventions.

### Rationale for Chosen Decision:
The module-based hierarchical sidebar structure is the most effective approach for the "Physical AI & Humanoid Robotics" book because it directly supports its pedagogical goals and structured content architecture. It provides a clear, predictable, and intuitive navigation experience, which is paramount for a technical educational resource. This decision ensures that readers can easily follow the intended learning progression and access specific information efficiently, aligning with the "Structured Learning" and "Book Format" principles of the Constitution.

### Status: Accepted