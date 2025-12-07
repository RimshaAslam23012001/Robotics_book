### Title: Choice of MDX for Code + Diagrams

### Context:
The "Physical AI & Humanoid Robotics" book will contain extensive code examples, technical explanations, and various diagrams (flowcharts, architectural diagrams, data flow diagrams). The chosen content format must effectively integrate these elements while supporting Docusaurus capabilities.

### Decision:
The book content will primarily be authored in **MDX (Markdown with JSX)** files. MDX allows for seamless embedding of React components directly within Markdown, enabling dynamic content, interactive elements, and robust rendering of code blocks and diagrams.

### Alternatives Considered:
*   **Pure Markdown (.md)**: Standard Markdown format.
*   **HTML within Markdown**: Embedding raw HTML for more complex layouts or components.
*   **Separate files for code/diagrams**: Storing code in `.py`, `.cpp` files and diagrams as `.svg`, `.png` images, then embedding them.

### Pros & Cons:
*   **MDX (Markdown with JSX)**:
    *   **Pros**: Powerful combination of Markdown simplicity with React component flexibility. Enables creation of custom components for interactive diagrams, code snippets, or complex layouts directly within the content. Supports syntax highlighting for various languages. Integrates natively with Docusaurus.
    *   **Cons**: Has a learning curve for authors unfamiliar with JSX/React. Can become complex if overused for overly elaborate components. Requires a Node.js build environment.
*   **Pure Markdown (.md)**:
    *   **Pros**: Simplest format, universally readable. Good for static text and basic code blocks.
    *   **Cons**: Limited interactivity. Embedding complex diagrams or custom layouts is difficult or impossible. Requires external rendering for features like Mermaid diagrams or advanced syntax highlighting.
*   **HTML within Markdown**:
    *   **Pros**: Offers more flexibility than pure Markdown for custom layouts.
    *   **Cons**: Breaks Markdown readability. Can be difficult to maintain. Security risks if not properly sanitized.
*   **Separate files for code/diagrams**:
    *   **Pros**: Keeps content files clean. Promotes reusability of code/diagrams.
    *   **Cons**: Requires more boilerplate for embedding. Disconnects content from its visual/code representations during authoring. Manual updates for embedding can be error-prone.

### Impact:
*   All chapter files will use the `.mdx` extension.
*   Authors will be required to learn basic MDX syntax and potentially how to create/use simple React components for advanced content.
*   Claude Code automation will generate MDX-compliant content, including structured code blocks and placeholders for diagrams.
*   Docusaurus configuration will enable MDX processing and necessary plugins (e.g., for Mermaid).

### Risks:
*   **Learning Curve**: Authors unfamiliar with React/JSX might find MDX challenging initially. Mitigation involves providing clear examples and documentation for common MDX patterns.
*   **Over-engineering**: Tendency to create overly complex custom components when simpler Markdown might suffice. Mitigation involves establishing guidelines for when to use basic Markdown versus MDX components.
*   **Build Complexity**: MDX processing adds a layer to the build pipeline. Mitigation by relying on Docusaurus's native support and well-tested plugins.

### Rationale for Chosen Decision:
MDX is the optimal choice for the "Physical AI & Humanoid Robotics" book because it provides the flexibility to integrate rich technical content—including code examples, interactive simulations, and dynamic diagrams—directly within the narrative. This enhances the educational experience, allows for more engaging and illustrative explanations, and leverages Docusaurus's modern capabilities, thereby fulfilling the "Educational Value First" and "Reproducibility & Transparency" principles of the Constitution.

### Status: Accepted