import React, { useState } from 'react';
import TranslationButton from '../TranslationButton/TranslationButton';
import TranslatedContentDisplay from '../TranslatedContentDisplay/TranslatedContentDisplay';

const ChapterTranslation = ({
  chapterId,
  originalContent,
  authToken,
  className = ""
}) => {
  const [translatedContent, setTranslatedContent] = useState(null);
  const [isTranslated, setIsTranslated] = useState(false);
  const [currentContent, setCurrentContent] = useState(originalContent);

  const handleTranslate = (content, result) => {
    setTranslatedContent(content);
    setIsTranslated(true);
    setCurrentContent(content);
  };

  const handleRevert = () => {
    setCurrentContent(originalContent);
    setIsTranslated(false);
  };

  return (
    <div className={`chapter-translation ${className}`}>
      <TranslationButton
        chapterId={chapterId}
        authToken={authToken}
        onTranslate={handleTranslate}
        onRevert={handleRevert}
      />

      <TranslatedContentDisplay
        originalContent={originalContent}
        translatedContent={translatedContent}
        isTranslated={isTranslated}
        onRevert={handleRevert}
      />
    </div>
  );
};

export default ChapterTranslation;