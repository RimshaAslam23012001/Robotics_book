import React, { useState, useEffect } from 'react';
import PersonalizationButton from '../PersonalizationButton/PersonalizationButton';
import PersonalizedContentDisplay from '../PersonalizedContentDisplay/PersonalizedContentDisplay';

const ChapterPersonalization = ({
  chapterId,
  originalContent,
  authToken,
  className = ""
}) => {
  const [personalizedContent, setPersonalizedContent] = useState(null);
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [currentContent, setCurrentContent] = useState(originalContent);

  const handlePersonalize = (content, result) => {
    setPersonalizedContent(content);
    setIsPersonalized(true);
    setCurrentContent(content);
  };

  const handleRevert = () => {
    setCurrentContent(originalContent);
    setIsPersonalized(false);
  };

  return (
    <div className={`chapter-personalization ${className}`}>
      <PersonalizationButton
        chapterId={chapterId}
        authToken={authToken}
        onPersonalize={handlePersonalize}
        onRevert={handleRevert}
      />

      <PersonalizedContentDisplay
        originalContent={originalContent}
        personalizedContent={personalizedContent}
        isPersonalized={isPersonalized}
        onRevert={handleRevert}
      />
    </div>
  );
};

export default ChapterPersonalization;