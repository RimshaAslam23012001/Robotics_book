import React, { useState } from 'react';
import OriginalDocItem from '@theme-original/DocItem';
import { useAuth } from '../components/Auth/AuthContext';
import ChapterActionBar from '../components/ChapterActionBar/ChapterActionBar';
import ErrorBoundary from '../components/ErrorBoundary/ErrorBoundary';

export default function DocItem(props) {
  const { content: DocContent } = props;
  const { metadata } = DocContent;
  const { user } = useAuth();
  const [content, setContent] = useState(null);

  const handleContentChange = (newContent, isUrdu) => {
    setContent({ content: newContent, isUrdu });
  };

  return (
    <>
      {user && (
        <ErrorBoundary>
          <ChapterActionBar
            chapterId={metadata?.unversionedId || metadata?.id}
            originalContent={props.children}
            onContentChange={handleContentChange}
          />
        </ErrorBoundary>
      )}
      <OriginalDocItem {...props} />
    </>
  );
}