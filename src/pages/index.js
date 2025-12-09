import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [selectedModule, setSelectedModule] = useState(null);

  const handleReadModeClick = (e) => {
    // Add a visual effect to simulate book opening
    const readModeButton = document.querySelector(`.${styles.button}`);
    if (readModeButton) {
      readModeButton.classList.add(styles.bookOpening);
      setTimeout(() => {
        readModeButton.classList.remove(styles.bookOpening);
      }, 600);
    }

    // Add a subtle page transition effect
    document.body.style.overflow = 'hidden';
    setTimeout(() => {
      document.body.style.overflow = '';
    }, 300);
  };

  const handleExploreModulesClick = (e) => {
    e.preventDefault();
    setDropdownOpen(!dropdownOpen);

    // Add visual feedback to the button
    const exploreButton = document.querySelector(`.${styles.secondaryButton}`);
    if (exploreButton) {
      exploreButton.classList.toggle(styles['dropdown-active']);
    }
  };

  const handleModuleClick = (moduleName, modulePath) => {
    setSelectedModule(moduleName);
    setDropdownOpen(false);

    // Remove active class from button when dropdown closes
    const exploreButton = document.querySelector(`.${styles.secondaryButton}`);
    if (exploreButton) {
      exploreButton.classList.remove(styles['dropdown-active']);
    }

    // Navigate to the module page
    window.location.href = modulePath;
  };

  // Close dropdown when clicking outside
  React.useEffect(() => {
    const handleClickOutside = (event) => {
      const dropdown = document.querySelector(`.${styles.dropdown}`);
      if (dropdown && !dropdown.contains(event.target)) {
        setDropdownOpen(false);
        const exploreButton = document.querySelector(`.${styles.secondaryButton}`);
        if (exploreButton) {
          exploreButton.classList.remove(styles['dropdown-active']);
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Define the 4 modules
  const modules = [
    { name: 'Module 1: Communication Architecture', path: '/docs/module-1/communication-architecture' },
    { name: 'Module 2: Virtual Environment', path: '/docs/module-2/virtual-environment' },
    { name: 'Module 3: Perception Navigation', path: '/docs/module-3/perception-navigation' },
    { name: 'Module 4: VLA System', path: '/docs/module-4/vla-system' }
  ];

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className={styles.techElement}>⚙️</div>
      <div className="container">
        <div className={styles.contentContainer}>
          <div className={styles.textSection}>
            <div className={styles.logoContainer}>
              <img
                src="/img/logo.svg"
                alt="Book Logo"
                className={styles.bookLogo}
              />
            </div>
            <h1 className="hero__title">{siteConfig.title}</h1>
            <p className="hero__subtitle">{siteConfig.tagline}</p>
            <div className={styles.buttons}>
              <Link
                className={clsx('button button--outline button--lg', styles.button)}
                to="/docs/quickstart"
                onClick={handleReadModeClick}>
                Read Mode
              </Link>
              <div className={styles.dropdown}>
                <button
                  className={clsx('button button--outline button--lg', styles.secondaryButton)}
                  onClick={handleExploreModulesClick}
                  type="button">
                  Explore Modules
                </button>
                {dropdownOpen && (
                  <div className={clsx(styles['dropdown-content'], styles.show)}>
                    {modules.map((module, index) => (
                      <div
                        key={index}
                        className={styles['dropdown-item']}
                        onClick={() => handleModuleClick(module.name, module.path)}
                      >
                        {module.name}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
          <div className={styles.robotSection}>
            <div className={styles.robotVisualization}>
              <div className={styles.robotBase}>
                <div className={styles.robotBody}>
                  <div className={styles.robotHead}>
                    <div className={clsx(styles.robotEye, styles.left)}></div>
                    <div className={clsx(styles.robotEye, styles.right)}></div>
                    <div className={styles.robotAntenna}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="A comprehensive guide to robotics, simulation, and AI integration">
      <HomepageHeader />
      <main>
        {/* You can add more content here if needed */}
      </main>
    </Layout>
  );
}