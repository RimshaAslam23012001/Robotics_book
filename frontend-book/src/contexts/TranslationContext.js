import React, { createContext, useContext, useState, useEffect } from 'react';

const TranslationContext = createContext();

export const TranslationProvider = ({ children }) => {
  const [isUrdu, setIsUrdu] = useState(false);

  useEffect(() => {
    const savedPreference = localStorage.getItem('book-language-preference');
    if (savedPreference) {
      setIsUrdu(savedPreference === 'urdu');
    }
  }, []);

  const toggleLanguage = () => {
    setIsUrdu(!isUrdu);
  };

  const value = {
    isUrdu,
    toggleLanguage,
    setIsUrdu
  };

  return (
    <TranslationContext.Provider value={value}>
      {children}
    </TranslationContext.Provider>
  );
};

export const useTranslation = () => {
  const context = useContext(TranslationContext);
  if (!context) {
    throw new Error('useTranslation must be used within a TranslationProvider');
  }
  return context;
};