import React from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function About() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout title={`About - ${siteConfig.title}`} description="Learn more about the Physical AI & Humanoid Robotics book">
      <main className="container margin-vert--lg">
        <div className="row">
          <div className="col col--8 col--offset-2">
            <h1>About This Book</h1>
            <p className="hero__subtitle">
              <strong>Physical AI & Humanoid Robotics</strong> is a comprehensive guide designed for robotics engineers, AI researchers, university students, and professionals seeking to understand the intersection of artificial intelligence and physical systems.
            </p>

            <div className="margin-vert--lg">
              <h2>Book Overview</h2>
              <p>
                This technical handbook covers the essential components of modern robotics systems, from communication architectures to intelligent control systems. The book follows an architecture-first approach, emphasizing system design principles that underpin successful robotic implementations.
              </p>

              <h3>Core Modules</h3>
              <ul>
                <li><strong>Communication Architecture:</strong> Distributed systems and real-time communication protocols</li>
                <li><strong>Virtual Environment & Simulation:</strong> Physics engines and simulation frameworks</li>
                <li><strong>Perception & Navigation:</strong> Sensor fusion and autonomous navigation systems</li>
                <li><strong>Vision-Language-Action System:</strong> Integrated AI for robotic manipulation</li>
              </ul>
            </div>

            <div className="margin-vert--lg">
              <h2>Target Audience</h2>
              <p>
                This book is designed for professionals and academics who need practical, implementation-focused guidance on building complex robotic systems. It assumes familiarity with basic programming concepts and mathematical foundations relevant to robotics.
              </p>
            </div>

            <div className="margin-vert--lg">
              <h2>Philosophy</h2>
              <p>
                We believe in an architecture-first approach to robotics, where system design principles guide implementation decisions. The book emphasizes minimal, precise, and calm design principles that reflect the serious engineering nature of robotics systems.
              </p>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}