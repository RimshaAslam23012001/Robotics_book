import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import './TranslatedContentDisplay.css';

const TranslatedContentDisplay = ({
  originalContent,
  translatedContent,
  isTranslated,
  onRevert
}) => {
  const [displayContent, setDisplayContent] = useState(originalContent);
  const [showOriginal, setShowOriginal] = useState(false);

  useEffect(() => {
    if (isTranslated && translatedContent) {
      setDisplayContent(translatedContent);
    } else {
      setDisplayContent(originalContent);
    }
  }, [isTranslated, translatedContent, originalContent]);

  const handleToggleView = () => {
    if (isTranslated) {
      if (showOriginal) {
        setDisplayContent(translatedContent);
        setShowOriginal(false);
      } else {
        setDisplayContent(originalContent);
        setShowOriginal(true);
      }
    }
  };

  const getDisplayTitle = () => {
    if (!isTranslated) {
      return "Original Content";
    }
    return showOriginal ? "Original Content" : "Urdu Translation";
  };

  return (
    <div className="translated-content-container">
      <div className="content-header">
        <h3>{getDisplayTitle()}</h3>
        {isTranslated && (
          <button
            className="toggle-view-button"
            onClick={handleToggleView}
          >
            {showOriginal ? "Show Urdu" : "Show Original"}
          </button>
        )}
      </div>

      <div className="content-body">
        <ReactMarkdown
          className="markdown-content"
          rehypePlugins={[rehypeRaw]}
        >
          {displayContent}
        </ReactMarkdown>
      </div>

      {isTranslated && (
        <div className="content-footer">
          <button
            className="revert-button"
            onClick={onRevert}
          >
            Revert to Original View
          </button>
        </div>
      )}
    </div>
  );
};

export default TranslatedContentDisplay;