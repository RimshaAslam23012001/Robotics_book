# ADR-0037: Robotics AI System Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-07
- **Feature:** 2-robotics-ai-modules
- **Context:** The "Physical AI & Humanoid Robotics" book project requires a comprehensive system architecture that integrates ROS 2 communication middleware, simulation environments, AI perception systems, and Vision-Language-Action (VLA) capabilities into a cohesive framework. This architecture decision impacts how all components interact, how data flows through the system, and how readers will understand the integration of robotics and AI technologies.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

The project will implement a modular, layered system architecture that separates concerns while enabling tight integration between components:

- **Communication Layer**: ROS 2 as the primary middleware for all inter-component communication using topics, services, and actions
- **Simulation Layer**: Gazebo and Isaac Sim providing physics-based simulation with realistic sensor models
- **Perception Layer**: GPU-accelerated computer vision and sensor processing with SLAM capabilities
- **Cognitive Layer**: LLM-based planning and decision-making with safety constraint validation
- **Action Layer**: Low-level robot control and actuator interfaces
- **Integration Layer**: VLA (Vision-Language-Action) pipeline connecting voice commands to physical actions

The architecture follows a service-oriented approach where each functional unit operates as a semi-autonomous component that communicates through standardized ROS 2 interfaces, enabling both simulation-first development and eventual deployment to physical robots.

## Consequences

### Positive

- Clear separation of concerns enabling independent development and testing of components
- Simulation-first approach allowing development without physical hardware
- Scalable architecture supporting both simple and complex robotic behaviors
- Industry-standard ROS 2 interfaces ensuring compatibility with broader robotics ecosystem
- Modular design enabling substitution of components (e.g., different LLMs, simulation engines)
- Reusable components across different robotic platforms and applications
- Clear pathways for sim-to-real transfer of learned behaviors

### Negative

- Complex system with multiple integration points requiring careful coordination
- Potential performance bottlenecks at component boundaries
- Increased debugging complexity due to distributed architecture
- Dependency on multiple technology ecosystems (ROS 2, NVIDIA, etc.)
- Higher cognitive load for readers learning multiple interconnected systems
- Potential for component version compatibility issues
- More complex error handling and system monitoring requirements

## Alternatives Considered

Alternative Architecture A: Monolithic approach with tightly integrated components
- Pros: Simpler initial development, fewer integration concerns, potentially better performance
- Cons: Poor modularity, difficult to test components independently, harder to maintain and extend, not following ROS 2 best practices

Alternative Architecture B: Pure cloud-based architecture with remote simulation and control
- Pros: Reduced local hardware requirements, centralized management, easier updates
- Cons: Network latency issues for real-time control, requires reliable internet connection, limited to online use cases, higher operational costs

Alternative Architecture C: Hardware-first architecture designed specifically for one robot platform
- Pros: Optimized for specific hardware, potentially better performance, simpler integration
- Cons: Not generalizable to other platforms, limits educational value, vendor lock-in, less flexible for simulation-first learning approach

## References

- Feature Spec: specs/2-robotics-ai-modules/spec.md
- Implementation Plan: specs/2-robotics-ai-modules/plan.md
- Related ADRs: ADR-0001 through ADR-0011 (technology stack), ADR-0033 (end-to-end pipeline design)
- Evaluator Evidence: history/prompts/2-robotics-ai-modules/001-implement-robotics-ai-modules.implementation.prompt.md