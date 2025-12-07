### Title: Theme Selection: Docusaurus Classic

### Context:
The "Physical AI & Humanoid Robotics" book, built with Docusaurus, requires a theme that provides an optimal reading experience for technical documentation. The theme must support the book's pedagogical structure, offer customization capabilities for technical content, and align with the project's goals of accessibility and maintainability. Docusaurus Classic is the default theme that comes with Docusaurus and offers comprehensive features out-of-the-box.

### Decision:
The book will use the **Docusaurus Classic theme** as the base theme. This decision leverages the well-maintained, feature-rich default theme that provides excellent support for documentation sites, including sidebar navigation, search functionality, code blocks, and responsive design. The Classic theme's modular architecture allows for customization where needed while maintaining a solid foundation.

### Alternatives Considered:
*   **Docusaurus Swizzle-based Custom Theme**: Creating a completely custom theme by swizzling components from the Classic theme.
*   **Third-party Docusaurus Themes**: Using themes from the Docusaurus ecosystem like Infima-based custom themes or community themes.
*   **Tailwind CSS-based Themes**: Building a theme using Tailwind CSS for more granular control over styling.
*   **No Theme (Custom from Scratch)**: Starting with minimal Docusaurus configuration and building all UI components from scratch.

### Pros & Cons:
*   **Docusaurus Classic Theme**:
    *   **Pros**: Well-documented and widely supported. Includes all essential features out-of-the-box (search, navigation, code blocks, responsive design). Extensive customization options through CSS variables and component swizzling. Large community and extensive documentation. Maintained by the Docusaurus team. Provides a familiar, professional look for documentation. Supports the book's modular structure effectively. Integrates seamlessly with Docusaurus features like versioning and i18n.
    *   **Cons**: May appear generic compared to highly customized themes. Requires some learning curve to customize effectively. Less unique visual identity compared to custom themes.
*   **Swizzle-based Custom Theme**:
    *   **Pros**: Complete control over every aspect of the UI. Unique visual identity for the book. Ability to optimize specifically for robotics content.
    *   **Cons**: Significantly more development time and maintenance effort. Requires deep understanding of Docusaurus internals. Risk of breaking changes during Docusaurus updates. More complex for contributors to understand.
*   **Third-party Themes**:
    *   **Pros**: Potentially more unique appearance than Classic. May offer additional features.
    *   **Cons**: Less control over the theme's behavior. Potential compatibility issues with future Docusaurus updates. Less documentation and support. May not align perfectly with the book's specific needs.
*   **Tailwind CSS-based Themes**:
    *   **Pros**: Highly flexible styling. Modern CSS framework. Great for custom UI components.
    *   **Cons**: Requires additional setup and configuration. Adds complexity to the build process. May not be necessary for the book's requirements.
*   **Custom from Scratch**:
    *   **Pros**: Complete control over every aspect.
    *   **Cons**: Extremely high development and maintenance overhead. Risk of missing important accessibility or responsive features. Not cost-effective for the project's goals.

### Impact:
*   The `docusaurus.config.js` file will specify the Classic theme and configure its options.
*   Customization will be achieved through CSS variables and selective component swizzling rather than complete theme replacement.
*   The theme will support the book's content structure with proper sidebar navigation, code block styling, and responsive design.
*   Claude Code automation will include mechanisms to customize the Classic theme components as needed.
*   The theme choice will ensure compatibility with Docusaurus's built-in features like search, versioning, and internationalization.

### Risks:
*   **Generic Appearance**: The Classic theme might look similar to other Docusaurus sites. Mitigation involves targeted customizations to add unique visual elements while keeping the core structure.
*   **Limited Differentiation**: May not stand out visually from other documentation sites. Mitigation includes custom CSS additions and unique content organization that enhances the learning experience.
*   **Over-customization**: Temptation to heavily modify the Classic theme might lead to maintenance issues. Mitigation involves establishing clear guidelines for acceptable customizations that preserve the theme's core functionality.

### Rationale for Chosen Decision:
The Docusaurus Classic theme is the optimal choice for the "Physical AI & Humanoid Robotics" book because it provides a robust, well-supported foundation that meets all functional requirements without unnecessary complexity. The theme's proven track record in technical documentation, extensive customization options, and seamless integration with Docusaurus features align perfectly with the project's goals of accessibility, maintainability, and educational effectiveness. While it may require some visual customization to distinguish the book, the Classic theme offers the best balance between functionality and development effort, supporting the "Educational Value First" and "Reproducibility & Transparency" principles of the Constitution.

### Status: Accepted