import React, { useState, useEffect } from 'react';
import './GlobalTranslationToggle.css';

const GlobalTranslationToggle = () => {
  const [isUrdu, setIsUrdu] = useState(false);

  // Check for saved preference in localStorage
  useEffect(() => {
    const savedPreference = localStorage.getItem('book-language-preference');
    if (savedPreference) {
      setIsUrdu(savedPreference === 'urdu');
    }

    // Apply directionality based on saved preference
    document.documentElement.dir = savedPreference === 'urdu' ? 'rtl' : 'ltr';
    if (savedPreference === 'urdu') {
      document.body.classList.add('urdu-mode');
    } else {
      document.body.classList.remove('urdu-mode');
    }
  }, []);

  const toggleLanguage = () => {
    const newLanguage = !isUrdu;
    setIsUrdu(newLanguage);
    localStorage.setItem('book-language-preference', newLanguage ? 'urdu' : 'english');

    // Apply directionality to the entire document
    document.documentElement.dir = newLanguage ? 'rtl' : 'ltr';

    // Add/remove CSS class for Urdu styling
    if (newLanguage) {
      document.body.classList.add('urdu-mode');
    } else {
      document.body.classList.remove('urdu-mode');
    }
  };

  return (
    <div className="global-translation-toggle">
      <button
        className={`translation-toggle-btn ${isUrdu ? 'urdu-mode' : 'english-mode'}`}
        onClick={toggleLanguage}
        title={isUrdu ? "Switch to English" : "اردو میں تبدیل کریں"}
        aria-label={isUrdu ? "Switch to English" : "Switch to Urdu"}
      >
        {isUrdu ? 'English' : 'اردو ترجمہ'}
      </button>
    </div>
  );
};

export default GlobalTranslationToggle;