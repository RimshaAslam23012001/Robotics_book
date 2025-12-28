import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import styles from './index.module.css';

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  const [open, setOpen] = useState(false);

  const modules = [
    { name: '01 — Communication Architecture', path: '/module-1/communication-architecture' },
    { name: '02 — Virtual Environment & Simulation', path: '/module-2/virtual-environment' },
    { name: '03 — Perception & Navigation', path: '/module-3/perception-navigation' },
    { name: '04 — Vision-Language-Action System', path: '/module-4/vla-system' },
  ];

  return (
    <Layout title={siteConfig.title}>
      <main>
        <div className={styles.hero}>
          <div className={styles.overlay} />

          <section className={styles.container}>
            <div className={styles.centered}>
              <span className={styles.badge}>
                PHYSICAL AI · HUMANOID ROBOTICS
              </span>

              <h1 className={styles.title}>{siteConfig.title}</h1>

              <p className={styles.subtitle}>
                Design, Simulation, Perception, and Intelligent Control Systems
              </p>

              <div className={styles.actions}>
                <Link to="/intro" className={styles.primary}>
                  START READING
                </Link>

                <button
                  className={styles.secondary}
                  onClick={() => setOpen(!open)}
                  aria-expanded={open}
                >
                  SYSTEM MODULES
                </button>
              </div>

              {open && (
                <div className={styles.panel}>
                  {modules.map((m) => (
                    <Link key={m.path} to={m.path} className={styles.item}>
                      {m.name}
                    </Link>
                  ))}
                </div>
              )}
            </div>
          </section>
        </div>

        <HomepageFeatures />
      </main>
    </Layout>
  );
}
