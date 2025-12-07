### Title: GitHub Pages for Deployment (vs Netlify/Vercel)

### Context:
The "Physical AI & Humanoid Robotics" book, built with Docusaurus, requires a reliable and cost-effective hosting solution for its static site. The deployment strategy impacts ease of setup, integration with GitHub-based workflows, and overall hosting costs. The plan specifies GitHub Pages.

### Decision:
The book will be deployed using **GitHub Pages**. This decision leverages the tight integration with the project's GitHub repository, offering a straightforward, free, and efficient way to publish the static Docusaurus site directly from the source code.

### Alternatives Considered:
*   **Netlify**: A popular platform for hosting static sites, offering continuous deployment, serverless functions, and global CDN.
*   **Vercel**: Another leading platform for frontend frameworks, known for its performance and developer experience, especially with Next.js.
*   **AWS S3 + CloudFront**: A cloud-based solution for hosting static sites with a content delivery network, offering high scalability and performance.
*   **Self-hosting (e.g., Nginx)**: Deploying the static site on a custom server.

### Pros & Cons:
*   **GitHub Pages**:
    *   **Pros**: Free hosting, seamless integration with GitHub repositories (automatic deployment from specified branch), straightforward setup for Docusaurus projects. Version control is inherently tied to deployment. Widely used for open-source documentation.
    *   **Cons**: Less advanced features compared to dedicated platforms (e.g., no built-in serverless functions, simpler CDN). Can be slower for global audiences compared to platforms with extensive edge networks. Custom domain setup requires DNS configuration.
*   **Netlify/Vercel**:
    *   **Pros**: Excellent developer experience, continuous deployment from Git, global CDN, built-in serverless functions, analytics, and other advanced features. Highly performant.
    *   **Cons**: Free tier has limitations; paid plans can incur costs as usage scales. Adds an external dependency to the deployment pipeline.
*   **AWS S3 + CloudFront**:
    *   **Pros**: Highly scalable, performant global CDN, full control over infrastructure, very reliable.
    *   **Cons**: More complex to set up and manage. Can incur significant costs depending on traffic.
*   **Self-hosting**:
    *   **Pros**: Full control over environment.
    *   **Cons**: High operational overhead for maintenance, security, and scalability. Not recommended for a typical documentation site.

### Impact:
*   The `package.json` and `docusaurus.config.js` files will be configured for GitHub Pages deployment, including base URL and deployment scripts.
*   Deployment will be triggered by pushing changes to a designated branch (e.g., `gh-pages` or `main`/`master` branch).
*   Claude Code automation will include scripts or guidance for initiating and verifying GitHub Pages deployments.

### Risks:
*   **Performance for Global Audience**: For very high global traffic, GitHub Pages' CDN might not be as optimized as commercial alternatives. Mitigation by optimizing Docusaurus build for performance.
*   **Custom Domain Setup**: Requires manual DNS configuration, which can be a point of error. Mitigation includes providing clear instructions in the book.
*   **Feature Limitations**: If advanced hosting features (e.g., A/B testing, complex redirects, serverless logic) are needed later, a migration might be required. Mitigation by addressing this as an ADR in future iterations if the need arises.

### Rationale for Chosen Decision:
GitHub Pages is the ideal deployment solution for the "Physical AI & Humanoid Robotics" book due to its seamless integration with GitHub, zero hosting costs, and straightforward setup for Docusaurus. This aligns with the open-source nature of many robotics projects and ensures that the book remains accessible and maintainable without incurring external hosting expenses, directly supporting the "Book Format" principle of the Constitution.

### Status: Accepted