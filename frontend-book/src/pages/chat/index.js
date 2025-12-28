import React from 'react';
import Layout from '@theme/Layout';
import Chatbot from '@site/src/components/Chatbot/Chatbot';
import ErrorBoundary from '@site/src/components/ErrorBoundary/ErrorBoundary';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './chat.module.css';

export default function ChatPage() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout title={`Chat - ${siteConfig.title}`} description="Chat with the RAG-powered assistant">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--12">
            <div className={styles.chatPage}>
              <div className={styles.chatContainer}>
                <ErrorBoundary>
                  <Chatbot />
                </ErrorBoundary>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}