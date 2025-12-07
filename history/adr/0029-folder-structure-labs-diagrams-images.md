### Title: Folder Structure for Labs, Diagrams, Images

### Context:
The "Physical AI & Humanoid Robotics" book includes various types of supplementary content beyond the main text, including hands-on labs, technical diagrams, and images. These assets need to be organized in a way that maintains consistency across modules, supports the Docusaurus documentation structure, and enables efficient content management. The book's pedagogical approach includes weekly learning progression with integrated labs, requiring a systematic approach to organizing these assets.

### Decision:
The project will implement a **centralized assets folder structure** where labs, diagrams, and images are organized by type in dedicated directories at the root level, while also maintaining module-specific assets when necessary. The structure will follow the pattern: `/docs/assets/labs/`, `/docs/assets/diagrams/`, and `/docs/assets/images/` for shared resources, with module-specific subdirectories as needed (e.g., `/docs/assets/labs/module-1/`, `/docs/assets/diagrams/module-1/`).

### Alternatives Considered:
*   **Flat Structure**: Placing all assets in a single directory without categorization.
*   **Module-Specific Assets**: Keeping all assets within each module directory (e.g., `/docs/module-1/labs/`, `/docs/module-1/diagrams/`).
*   **Type-Specific Structure with Module Subdirectories**: Organizing by asset type first, then by module (e.g., `/docs/labs/module-1/`, `/docs/diagrams/module-1/`).
*   **File Extension-Based Structure**: Organizing assets based on file extensions (e.g., `/docs/images/png/`, `/docs/images/svg/`).
*   **Centralized with Symbolic Links**: Using a central repository with symbolic links from module directories.

### Pros & Cons:
*   **Centralized Assets with Type-Based Organization**:
    *   **Pros**: Clear categorization by asset type makes it easy to locate specific resources. Enables efficient reuse of common assets across modules. Simplifies asset management and maintenance. Supports both shared and module-specific assets. Consistent with common documentation practices. Easy to implement search and indexing for assets. Facilitates bulk operations on similar asset types.
    *   **Cons**: May require longer paths for module-specific assets. Could become crowded if not properly organized with subdirectories. Requires discipline to maintain proper categorization.
*   **Flat Structure**:
    *   **Pros**: Simple to implement. Minimal directory navigation.
    *   **Cons**: Difficult to organize and locate specific assets. No clear categorization. Becomes unwieldy as the number of assets grows. No logical grouping of related assets.
*   **Module-Specific Assets**:
    *   **Pros**: Assets are co-located with related content. Clear separation between modules. Easy to identify module dependencies.
    *   **Cons**: Difficult to share assets across modules. May lead to duplication of common assets. Harder to maintain consistent styling across modules. More complex to update shared assets.
*   **Type-Specific with Module Subdirectories**:
    *   **Pros**: Maintains clear asset type categorization. Organizes assets by module for easy location.
    *   **Cons**: May make it harder to identify common assets that could be shared across modules. Could result in fragmented common resources.
*   **File Extension-Based Structure**:
    *   **Pros**: Organized by technical format. Efficient for format-specific operations.
    *   **Cons**: Doesn't reflect the pedagogical or functional organization needed for a book. May mix unrelated assets of the same format.

### Impact:
*   The `/docs/assets/` directory will be created with subdirectories for `labs`, `diagrams`, and `images`.
*   Each module may have subdirectories within these asset types when module-specific content is needed.
*   Docusaurus configuration will be updated to properly serve these assets.
*   Content creators will need to follow the established asset organization conventions.
*   Claude Code automation will include mechanisms to scaffold the appropriate asset directories when creating new modules or chapters.
*   The build process will need to ensure all assets are properly copied and referenced.

### Risks:
*   **Asset Duplication**: Without careful management, similar assets might be duplicated across modules. Mitigation involves establishing clear guidelines for when to use shared vs. module-specific assets.
*   **Path Complexity**: Long asset paths might complicate referencing in content. Mitigation includes establishing clear conventions and potentially using Docusaurus aliases for common paths.
*   **Maintenance Overhead**: Centralized assets require coordination when updating shared resources. Mitigation involves clear documentation of asset dependencies and impact analysis for changes.

### Rationale for Chosen Decision:
The centralized assets structure with type-based organization is chosen because it provides the best balance between asset discoverability, reusability, and maintainability for the "Physical AI & Humanoid Robotics" book. This structure supports both the sharing of common assets (like standard diagrams or lab templates) across modules and the organization of module-specific content. The clear categorization by asset type aligns with the different roles these assets play in the educational experience, making it easier for content creators to locate and manage resources. This approach supports the "Educational Value First" and "Reproducibility & Transparency" principles by ensuring consistent organization and easy access to all educational materials.

### Status: Accepted