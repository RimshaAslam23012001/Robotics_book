### Title: Use of Mermaid for Flow Diagrams

### Context:
The "Physical AI & Humanoid Robotics" book requires clear and concise visual representations for complex processes, data flows, and system architectures (e.g., AI pipelines, ROS 2 communication graphs). Integrating diagrams directly into the Markdown content enhances readability and understanding.

### Decision:
The book will utilize **Mermaid.js** for generating all flowcharts, sequence diagrams, state diagrams, and other textual diagrams directly within Markdown/MDX files. This decision leverages Mermaid's text-based syntax for version control friendliness and Docusaurus's native support for rendering such diagrams.

### Alternatives Considered:
*   **Image-based Diagrams (e.g., SVG, PNG)**: Creating diagrams in external tools (e.g., draw.io, Lucidchart) and embedding them as image files.
*   **ASCII Art Diagrams**: Using text characters to create diagrams directly in Markdown.
*   **PlantUML**: Another text-based diagramming tool.

### Pros & Cons:
*   **Mermaid.js**:
    *   **Pros**: Text-based syntax, making diagrams version-control-friendly (diffable) and easily editable. Integrates seamlessly with Markdown/MDX and Docusaurus. Supports a variety of diagram types (flowcharts, sequence, state, class, etc.). Highly readable source code for diagrams. Allows for dynamic diagrams if used with React components.
    *   **Cons**: Has a learning curve for new syntax. Can become complex for very large or intricate diagrams. Rendering might vary slightly across platforms if not configured consistently.
*   **Image-based Diagrams**:
    *   **Pros**: High visual fidelity, full control over styling and layout. Universally supported.
    *   **Cons**: Not version-control-friendly (binary files make diffs meaningless). Requires external tools and separate file management. Difficult to update and synchronize with textual content. No interactivity.
*   **ASCII Art Diagrams**:
    *   **Pros**: Pure text, extremely portable. No special tooling required.
    *   **Cons**: Very limited in complexity and visual appeal. Difficult to maintain for anything beyond simple structures.
*   **PlantUML**:
    *   **Pros**: Powerful, supports many diagram types, text-based. Good for complex enterprise-level diagrams.
    *   **Cons**: Requires a Java runtime to render, which adds a dependency. Integration into Docusaurus might be less straightforward than Mermaid.

### Impact:
*   All new diagrams (especially flowcharts, sequence diagrams, and architectural overviews) will be created using Mermaid syntax within MDX files.
*   Authors will be trained on Mermaid syntax. Claude Code automation will assist in scaffolding Mermaid diagram code blocks.
*   Docusaurus build will include the necessary plugin to render Mermaid diagrams.

### Risks:
*   **Syntax Complexity**: For very complex diagrams, Mermaid syntax can become dense. Mitigation involves modularizing diagrams and providing clear examples.
*   **Rendering Issues**: Ensuring consistent rendering across different Docusaurus versions or themes. Mitigation through testing and adherence to documented Mermaid/Docusaurus best practices.

### Rationale for Chosen Decision:
Mermaid.js is chosen as the primary diagramming tool because its text-based nature aligns perfectly with the Spec-Kit Plus workflow and version control best practices. It allows for diagrams to be managed and diffed like code, ensuring consistency and ease of updates. Coupled with Docusaurus's native integration, Mermaid enhances the book's "Educational Value First" and "Reproducibility & Transparency" principles by providing clear, maintainable, and visually engaging explanations of complex robotics and AI concepts.

### Status: Accepted