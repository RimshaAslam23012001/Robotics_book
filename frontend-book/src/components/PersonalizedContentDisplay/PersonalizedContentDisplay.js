import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import './PersonalizedContentDisplay.css';

const PersonalizedContentDisplay = ({
  originalContent,
  personalizedContent,
  isPersonalized,
  onRevert
}) => {
  const [displayContent, setDisplayContent] = useState(originalContent);
  const [showOriginal, setShowOriginal] = useState(false);

  useEffect(() => {
    if (isPersonalized && personalizedContent) {
      setDisplayContent(personalizedContent);
    } else {
      setDisplayContent(originalContent);
    }
  }, [isPersonalized, personalizedContent, originalContent]);

  const handleToggleView = () => {
    if (isPersonalized) {
      if (showOriginal) {
        setDisplayContent(personalizedContent);
        setShowOriginal(false);
      } else {
        setDisplayContent(originalContent);
        setShowOriginal(true);
      }
    }
  };

  const getDisplayTitle = () => {
    if (!isPersonalized) {
      return "Original Content";
    }
    return showOriginal ? "Original Content" : "Personalized Content";
  };

  return (
    <div className="personalized-content-container">
      <div className="content-header">
        <h3>{getDisplayTitle()}</h3>
        {isPersonalized && (
          <button
            className="toggle-view-button"
            onClick={handleToggleView}
          >
            {showOriginal ? "Show Personalized" : "Show Original"}
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

      {isPersonalized && (
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

export default PersonalizedContentDisplay;