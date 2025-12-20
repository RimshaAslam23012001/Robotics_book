import React from 'react';
import styles from './HomepageFeatures.module.css';

const modules = [
  {
    id: '01',
    title: 'Communication Architecture',
    description:
      'ROS 2 communication model, DDS, publishers, subscribers, services, and real-time data flow between robotic components.',
    progress: 90,
  },
  {
    id: '02',
    title: 'Virtual Environment & Simulation',
    description:
      'Gazebo-based simulation pipelines, sensor modeling, physics accuracy, and digital twins for robotics systems.',
    progress: 75,
  },
  {
    id: '03',
    title: 'Perception & Navigation',
    description:
      'Sensor fusion, mapping, localization, path planning, and autonomous navigation stacks.',
    progress: 60,
  },
  {
    id: '04',
    title: 'Vision-Language-Action System',
    description:
      'Integrating vision, language understanding, and action execution for intelligent humanoid robots.',
    progress: 40,
  },
];

export default function HomepageFeatures() {
  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <h2 className={styles.heading}>SYSTEM CURRICULUM</h2>
        <p className={styles.subheading}>
          A structured, architecture-first learning path for Physical AI & Humanoid Robotics
        </p>

        <div className={styles.list}>
          {modules.map((m) => (
            <div key={m.id} className={styles.module}>
              <div className={styles.header}>
                <span className={styles.index}>{m.id}</span>
                <h3>{m.title}</h3>
              </div>

              <p className={styles.description}>{m.description}</p>

              <div className={styles.progress}>
                <div
                  className={styles.bar}
                  style={{ width: `${m.progress}%` }}
                />
                <span>{m.progress}% complete</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
