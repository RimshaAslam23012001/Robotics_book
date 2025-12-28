import React, { useState, useEffect } from 'react';
import TranslationAPI from '../../api/translation';
import './TranslationButton.css';

const TranslationButton = ({ chapterId, authToken, onTranslate, onRevert }) => {
  const [isTranslated, setIsTranslated] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleTranslate = async () => {
    if (!authToken) {
      setError('User not authenticated');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const result = await TranslationAPI.translateChapterToUrdu(chapterId, authToken);
      onTranslate(result.translatedContent, result);
      setIsTranslated(true);
    } catch (err) {
      console.error('Error translating chapter to Urdu:', err);
      setError('Failed to translate chapter to Urdu. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRevert = () => {
    onRevert();
    setIsTranslated(false);
    setError(null);
  };

  // Check if user is authenticated
  if (!authToken) {
    return null; // Don't show button for unauthenticated users
  }

  return (
    <div className="translation-container">
      <div className="translation-controls">
        {!isTranslated ? (
          <button
            className={`translate-button ${isLoading ? 'loading' : ''}`}
            onClick={handleTranslate}
            disabled={isLoading}
            title="Translate this chapter to Urdu"
          >
            {isLoading ? (
              <>
                <span className="spinner"></span>
                Translating...
              </>
            ) : (
              '.Translate to Urdu'
            )}
          </button>
        ) : (
          <button
            className="revert-button"
            onClick={handleRevert}
            title="Revert to original content"
          >
            Revert to Original
          </button>
        )}
      </div>

      {error && (
        <div className="translation-error">
          {error}
        </div>
      )}

      {isTranslated && (
        <div className="translation-indicator">
          Content has been translated to Urdu
        </div>
      )}
    </div>
  );
};

export default TranslationButton;