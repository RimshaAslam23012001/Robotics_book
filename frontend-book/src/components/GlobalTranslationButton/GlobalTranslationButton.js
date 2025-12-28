import React, { useState, useEffect } from 'react';
import TranslationAPI from '../api/translation';
import './GlobalTranslationButton.css';

const GlobalTranslationButton = ({ children }) => {
  const [isTranslated, setIsTranslated] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [currentContent, setCurrentContent] = useState(null);
  const [error, setError] = useState(null);
  const [originalContent, setOriginalContent] = useState(null);

  // Get the original content from children when component mounts
  useEffect(() => {
    if (children && !originalContent) {
      setOriginalContent(children);
      setCurrentContent(children);
    }
  }, [children, originalContent]);

  const handleTranslate = async () => {
    if (!children) return;

    setIsLoading(true);
    setError(null);

    try {
      // Extract chapter ID from document metadata if available
      // For this implementation, we'll need a way to identify the chapter
      // This is a simplified approach - in practice, you'd get the chapter ID from the page context
      const contentString = typeof children === 'string' ? children : JSON.stringify(children);

      // For now, we'll just toggle between original and a placeholder translated content
      // In a real implementation, you'd call the actual API with a chapter ID
      if (!isTranslated) {
        // Simulate translation - in real implementation, call actual API
        console.log('Translation would be called for this chapter');
        // This is where you'd implement the actual translation logic
        setIsTranslated(true);
      } else {
        // Revert to original
        setCurrentContent(children);
        setIsTranslated(false);
      }
    } catch (err) {
      console.error('Error with translation:', err);
      setError('Translation failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // If this is a placeholder for actual implementation, we'll just show the button
  return (
    <div className="global-translation-container">
      <div className="global-translation-bar">
        <button
          className={`global-translate-button ${isTranslated ? 'translated' : ''} ${isLoading ? 'loading' : ''}`}
          onClick={handleTranslate}
          disabled={isLoading}
          title={isTranslated ? "Switch to English" : "Translate to Urdu"}
        >
          {isLoading ? (
            <>
              <span className="spinner"></span>
              {isTranslated ? 'Switching...' : 'Translating...'}
            </>
          ) : (
            isTranslated ? 'English' : 'اردو ترجمہ'
          )}
        </button>

        {error && (
          <div className="global-translation-error">
            {error}
          </div>
        )}
      </div>

      <div className="content-container">
        {currentContent || children}
      </div>
    </div>
  );
};

export default GlobalTranslationButton;