import React, { useState } from 'react';
import Link from '@docusaurus/Link';
import styles from './FloatingChatButton.module.css';

const FloatingChatButton = () => {
  const [isVisible, setIsVisible] = useState(true);

  // Function to hide the button when user scrolls down and show when scrolls up
  React.useEffect(() => {
    let lastScrollY = window.scrollY;

    const handleScroll = () => {
      if (window.scrollY > lastScrollY && window.scrollY > 100) {
        // Scrolling down
        setIsVisible(false);
      } else {
        // Scrolling up
        setIsVisible(true);
      }
      lastScrollY = window.scrollY;
    };

    window.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <div className={`${styles.floatingChatButton} ${isVisible ? styles.visible : styles.hidden}`}>
      <Link
        to="/chat"
        className={styles.chatButton}
        aria-label="Open chat"
      >
        <svg
          className={styles.chatIcon}
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.36 15.01 3.02 16.32L2 22L7.68 20.98C8.99 21.64 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C8.69 20 6 17.31 6 14C6 13.11 6.21 12.26 6.57 11.5C7.26 10.17 8.5 9.21 9.91 8.97C10.16 8.39 10.7 8 11.32 8H12C13.1 8 14 8.9 14 10C14 11.1 13.1 12 12 12H11C10.45 12 10 12.45 10 13C10 13.55 10.45 14 11 14H12C13.66 14 15 12.66 15 11C15 9.34 13.66 8 12 8H11.32C9.92 8 8.72 8.84 8.16 10.03C7.33 10.27 6.64 11.05 6.35 12C6.12 12.66 6 13.33 6 14C6 17.31 8.69 20 12 20Z"
            fill="currentColor"
          />
        </svg>
      </Link>
    </div>
  );
};

export default FloatingChatButton;