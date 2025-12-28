import React, { useState, useEffect } from 'react';
import { useAuth } from '../Auth/AuthContext';
import ChapterActionBar from '../ChapterActionBar/ChapterActionBar';
import './ChapterPersonalizationTranslation.css';

const ChapterPersonalizationTranslation = ({
  children,
  chapterId,
  className = ""
}) => {
  const { user, loading } = useAuth();
  const [currentContent, setCurrentContent] = useState(children);
  const [isUrduContent, setIsUrduContent] = useState(false);

  // Update content when children prop changes
  useEffect(() => {
    setCurrentContent(children);
    setIsUrduContent(false); // Reset to non-Urdu when chapter changes
  }, [children]);

  const handleContentChange = (newContent, isUrdu) => {
    setCurrentContent(newContent);
    setIsUrduContent(isUrdu);
  };

  // Show loading state while checking authentication
  if (loading) {
    return (
      <div className={`chapter-features ${className}`}>
        <div className="chapter-features-loading">Loading...</div>
        {children}
      </div>
    );
  }

  return (
    <div className={`chapter-features ${className}`}>
      {/* Action bar for logged-in users */}
      {user && (
        <ChapterActionBar
          chapterId={chapterId}
          originalContent={children}
          onContentChange={handleContentChange}
        />
      )}

      {/* Chapter content */}
      <div className={`chapter-content ${isUrduContent ? 'urdu-content' : ''}`} dir={isUrduContent ? 'rtl' : 'ltr'}>
        {currentContent}
      </div>
    </div>
  );
};

export default ChapterPersonalizationTranslation;