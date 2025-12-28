import React, { useEffect } from 'react';
import { useTranslation } from '../contexts/TranslationContext';
import './TranslationNavbarButton.css';

const TranslationNavbarButton = () => {
  const { isUrdu, toggleLanguage } = useTranslation();

  useEffect(() => {
    // Update button text when language changes
    const updateButtonText = () => {
      const button = document.getElementById('translation-toggle');
      if (button) {
        button.textContent = isUrdu ? 'English' : 'اردو ترجمہ';
        button.classList.toggle('translated', isUrdu);
      }
    };

    updateButtonText();
  }, [isUrdu]);

  const handleClick = (e) => {
    e.preventDefault();
    toggleLanguage();
  };

  // We return null because the button is added via HTML in docusaurus.config.js
  // This component just handles the logic
  return null;
};

export default TranslationNavbarButton;