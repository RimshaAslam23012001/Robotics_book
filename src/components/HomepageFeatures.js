import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Robot Communication',
    imageUrl: 'img/robot-communication.jpg',
    description: (
      <>
        Learn about ROS 2 communication architecture, publisher-subscriber patterns,
        and how different robot components exchange information.
      </>
    ),
  },
  {
    title: 'Virtual Environment',
    imageUrl: 'img/virtual-environment.jpg',
    description: (
      <>
        Set up realistic Gazebo simulations with accurate sensor models
        and physics-based robot representations.
      </>
    ),
  },
  {
    title: 'Vision-Language-Action',
    imageUrl: 'img/vla-system.jpg',
    description: (
      <>
        Implement advanced VLA systems that understand natural language commands
        and execute complex robotic actions.
      </>
    ),
  },
];

function Feature({title, imageUrl, description}) {
  const imgUrl = imageUrl ? require('@site/' + imageUrl).default : null;
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        {imgUrl ? (
          <img src={imgUrl} alt={title} className={styles.featureImage} />
        ) : (
          <div className={styles.featurePlaceholder}>
            <div className={styles.featureIcon}>{title.charAt(0)}</div>
          </div>
        )}
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}