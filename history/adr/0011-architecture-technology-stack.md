# ADR-0011: Architecture Technology Stack

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-07
- **Feature:** 2-robotics-ai-modules
- **Context:** The "Physical AI & Humanoid Robotics" book project requires an integrated technology stack that encompasses both the educational content delivery (via Docusaurus-based book) and the robotics development environment (ROS 2, simulation tools, AI components). This decision impacts how readers will interact with the content, set up their development environment, and implement the examples throughout the book.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

The project will utilize an integrated technology stack consisting of:

- **Book Platform**: Docusaurus for content delivery, GitHub Pages for deployment
- **Robotics Middleware**: ROS 2 Humble Hawksbill as the primary communication framework
- **Simulation Environment**: NVIDIA Isaac Sim for advanced simulation, Gazebo for foundational examples
- **AI Components**: Whisper STT + LLM Planner + ROS 2 Actions for Vision-Language-Action (VLA) system
- **Development Environment**: Python 3.x, Markdown/MDX, JavaScript/TypeScript
- **Target Hardware**: NVIDIA Jetson for edge deployment, Linux for development

## Consequences

### Positive

- Comprehensive coverage of modern robotics development stack from foundational to advanced concepts
- Integration between educational content and practical implementation
- Access to cutting-edge simulation and AI tools (Isaac Sim, NVIDIA ecosystem)
- Strong ROS 2 integration for industry-standard robotics development
- Scalable from simulation to real hardware deployment
- Well-documented and supported technologies

### Negative

- Complex multi-toolchain setup required for readers
- Hardware dependencies (NVIDIA hardware for Isaac Sim, Jetson for edge)
- Multiple learning curves (ROS 2, Isaac Sim, Docusaurus, AI tools)
- Potential licensing considerations for proprietary tools (Unity, Isaac Sim)
- Higher system requirements for advanced simulation

## Alternatives Considered

Alternative Stack A: Simplified approach using only Gazebo + basic ROS 2 + static HTML book
- Pros: Simpler setup, open source tools only, lower hardware requirements
- Cons: Missing advanced AI/simulation capabilities, less realistic industry preparation

Alternative Stack B: Cloud-first approach with web-based IDEs and cloud simulation
- Pros: Reduced local setup complexity, standardized environment
- Cons: Requires internet connection, potential costs, less control over development environment

Alternative Stack C: Pure simulation approach without physical robot considerations
- Pros: Focus on simulation and AI, no hardware requirements
- Cons: Missing physical AI and real-world deployment aspects that are core to the book's mission

## References

- Feature Spec: specs/2-robotics-ai-modules/spec.md
- Implementation Plan: specs/2-robotics-ai-modules/plan.md
- Related ADRs: ADR-0001 through ADR-0010
- Evaluator Evidence: history/prompts/2-robotics-ai-modules/0001-generate-planning-specification-for-robotics-book.plan.prompt.md