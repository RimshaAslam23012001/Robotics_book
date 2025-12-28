import React, { useState, useEffect } from 'react';
import { useAuth } from '../Auth/AuthContext';
import PersonalizationAPI from '../../api/personalization';
import TranslationAPI from '../../api/translation';
import './ChapterActionBar.css';

const ChapterActionBar = ({ chapterId, originalContent, onContentChange }) => {
  const { user, loading } = useAuth();
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [isTranslated, setIsTranslated] = useState(false);
  const [isLoading, setIsLoading] = useState({ personalization: false, translation: false });
  const [error, setError] = useState(null);
  const [currentContent, setCurrentContent] = useState(originalContent);

  // Reset when chapter changes
  useEffect(() => {
    setIsPersonalized(false);
    setIsTranslated(false);
    setCurrentContent(originalContent);
    setError(null);
  }, [chapterId, originalContent]);

  const handlePersonalize = async () => {
    if (!user) return;

    setIsLoading(prev => ({ ...prev, personalization: true }));
    setError(null);

    try {
      const token = user.token || localStorage.getItem('auth_token');
      const result = await PersonalizationAPI.personalizeChapter(chapterId, token);

      if (result.personalizedContent) {
        setCurrentContent(result.personalizedContent);
        setIsPersonalized(true);
        if (onContentChange) onContentChange(result.personalizedContent, false); // not Urdu
      }
    } catch (err) {
      console.error('Error personalizing chapter:', err);
      setError('Failed to personalize chapter. Please try again.');
    } finally {
      setIsLoading(prev => ({ ...prev, personalization: false }));
    }
  };

  const handleTranslate = async () => {
    if (!user) return;

    setIsLoading(prev => ({ ...prev, translation: true }));
    setError(null);

    try {
      const token = user.token || localStorage.getItem('auth_token');
      const result = await TranslationAPI.translateChapterToUrdu(chapterId, token);

      if (result.translatedContent) {
        setCurrentContent(result.translatedContent);
        setIsTranslated(true);
        if (onContentChange) onContentChange(result.translatedContent, true); // is Urdu
      }
    } catch (err) {
      console.error('Error translating chapter:', err);
      setError('Failed to translate chapter. Please try again.');
    } finally {
      setIsLoading(prev => ({ ...prev, translation: false }));
    }
  };

  const handleRevert = () => {
    setCurrentContent(originalContent);
    setIsPersonalized(false);
    setIsTranslated(false);
    setError(null);
    if (onContentChange) onContentChange(originalContent, false); // not Urdu
  };

  const handleToggleTranslation = async () => {
    if (isTranslated) {
      // If currently translated, revert to original
      setCurrentContent(originalContent);
      setIsTranslated(false);
      if (isPersonalized) {
        // If it was personalized, try to get personalized content again
        try {
          const token = user.token || localStorage.getItem('auth_token');
          if (!token) {
            throw new Error('No authentication token available');
          }
          const result = await PersonalizationAPI.personalizeChapter(chapterId, token);
          if (result && result.personalizedContent) {
            setCurrentContent(result.personalizedContent);
            if (onContentChange) onContentChange(result.personalizedContent, false); // not Urdu
          } else {
            if (onContentChange) onContentChange(originalContent, false); // not Urdu
          }
        } catch (err) {
          console.error('Error reverting translation:', err);
          if (onContentChange) onContentChange(originalContent, false); // not Urdu
        }
      } else {
        if (onContentChange) onContentChange(originalContent, false); // not Urdu
      }
    } else {
      // If not translated, translate to Urdu
      handleTranslate();
    }
  };

  const handleTogglePersonalization = async () => {
    if (isPersonalized) {
      // If currently personalized, revert to original
      setCurrentContent(originalContent);
      setIsPersonalized(false);
      if (isTranslated) {
        // If it was translated, try to get translated content again
        try {
          const token = user.token || localStorage.getItem('auth_token');
          if (!token) {
            throw new Error('No authentication token available');
          }
          const result = await TranslationAPI.translateChapterToUrdu(chapterId, token);
          if (result && result.translatedContent) {
            setCurrentContent(result.translatedContent);
            if (onContentChange) onContentChange(result.translatedContent, true); // is Urdu
          } else {
            if (onContentChange) onContentChange(originalContent, false); // not Urdu
          }
        } catch (err) {
          console.error('Error reverting personalization:', err);
          if (onContentChange) onContentChange(originalContent, false); // not Urdu
        }
      } else {
        if (onContentChange) onContentChange(originalContent, false); // not Urdu
      }
    } else {
      // If not personalized, personalize content
      handlePersonalize();
    }
  };

  if (loading) {
    return <div className="chapter-action-bar-loading">Loading...</div>;
  }

  if (!user) {
    return null; // Don't show action bar for unauthenticated users
  }

  useEffect(() => {
    const handleGlobalLanguageChange = (e) => {
      const isUrdu = e.detail.isUrdu;
      if (isUrdu && !isTranslated) {
        // If global state is Urdu but this chapter isn't translated, translate it
        handleTranslate();
      } else if (!isUrdu && isTranslated) {
        // If global state is English but this chapter is translated, revert it
        handleRevert();
      }
    };

    window.addEventListener('languageChange', handleGlobalLanguageChange);

    // Cleanup event listener on unmount
    return () => {
      window.removeEventListener('languageChange', handleGlobalLanguageChange);
    };
  }, [isTranslated, isPersonalized, handleTranslate, handleRevert]); // Add dependencies

  return (
    <div className="chapter-action-bar">
      <div className="chapter-action-buttons">
        <button
          className={`action-button personalize-button ${isPersonalized ? 'active' : ''} ${isLoading.personalization ? 'loading' : ''}`}
          onClick={handleTogglePersonalization}
          disabled={isLoading.personalization || isLoading.translation}
          title="Personalize this chapter based on your background"
        >
          {isLoading.personalization ? (
            <>
              <span className="spinner"></span>
              Personalizing...
            </>
          ) : (
            isPersonalized ? 'Original Content' : 'Personalize This Chapter'
          )}
        </button>

        <button
          className={`action-button translate-button ${isTranslated ? 'active urdu-mode' : ''} ${isLoading.translation ? 'loading' : ''}`}
          onClick={handleToggleTranslation}
          disabled={isLoading.translation || isLoading.personalization}
          title="Toggle Urdu translation"
        >
          {isLoading.translation ? (
            <>
              <span className="spinner"></span>
              Translating...
            </>
          ) : (
            isTranslated ? 'English' : 'اردو ترجمہ'
          )}
        </button>

        {(isPersonalized || isTranslated) && (
          <button
            className="action-button revert-button"
            onClick={handleRevert}
            title="Revert to original content"
          >
            Revert to Original
          </button>
        )}
      </div>

      {error && (
        <div className="action-bar-error">
          {error}
        </div>
      )}
    </div>
  );
};

export default ChapterActionBar;