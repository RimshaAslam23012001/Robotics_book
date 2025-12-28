import React, { useState, useEffect } from 'react';
import PersonalizationAPI from '../../api/personalization';
import './PersonalizationButton.css';

const PersonalizationButton = ({ chapterId, authToken, onPersonalize, onRevert }) => {
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePersonalize = async () => {
    if (!authToken) {
      setError('User not authenticated');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const result = await PersonalizationAPI.personalizeChapter(chapterId, authToken);
      onPersonalize(result.personalizedContent, result);
      setIsPersonalized(true);
    } catch (err) {
      console.error('Error personalizing chapter:', err);
      setError('Failed to personalize chapter. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRevert = () => {
    onRevert();
    setIsPersonalized(false);
    setError(null);
  };

  // Check if user is authenticated
  if (!authToken) {
    return null; // Don't show button for unauthenticated users
  }

  return (
    <div className="personalization-container">
      <div className="personalization-controls">
        {!isPersonalized ? (
          <button
            className={`personalize-button ${isLoading ? 'loading' : ''}`}
            onClick={handlePersonalize}
            disabled={isLoading}
            title="Personalize this chapter based on your background"
          >
            {isLoading ? (
              <>
                <span className="spinner"></span>
                Personalizing...
              </>
            ) : (
              'Personalize This Chapter'
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
        <div className="personalization-error">
          {error}
        </div>
      )}

      {isPersonalized && (
        <div className="personalization-indicator">
          Content has been personalized for your background
        </div>
      )}
    </div>
  );
};

export default PersonalizationButton;