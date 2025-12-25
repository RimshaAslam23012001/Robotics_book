import React, { useState, useRef, useEffect } from 'react';
import styles from './Chatbot.module.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Hugging Face backend URL
  const BACKEND_URL = 'https://rimsha23-rag-chatboat.hf.space';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Optional: fetch with timeout
  const fetchWithTimeout = (url, options = {}, timeout = 15000) => {
    return Promise.race([
      fetch(url, options),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Request timed out')), timeout)
      ),
    ]);
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      console.log('Sending request to:', `${BACKEND_URL}/api/v1/query`);
      console.log('Request payload:', { query: inputValue, top_k: 5 });

      const response = await fetchWithTimeout(`${BACKEND_URL}/api/v1/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: inputValue, top_k: 5 }),
      });

      console.log('Response status:', response.status);

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log('Response data:', data);

      let botResponseText = '';
      const results = Array.isArray(data.results) ? data.results : [];

      if (results.length > 0) {
        botResponseText = results.map(r => r.text || r.content || '').join('\n\n');
      } else {
        botResponseText =
          "I couldn't find any relevant information. Please try rephrasing your question.";
      }

      const botMessage = {
        id: Date.now() + 1,
        text: botResponseText,
        sender: 'bot',
        sources: results,
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to get response from the backend. Please try again.');

      const errorMessage = {
        id: Date.now() + 1,
        text: err.message || 'Sorry, I encountered an error while processing your request.',
        sender: 'bot',
        error: true,
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <div className={styles.chatbotContainer}>
      <div className={styles.chatHeader}>
        <h3>Book Assistant</h3>
        <button onClick={clearChat} className={styles.clearButton}>
          Clear Chat
        </button>
      </div>

      <div className={styles.chatMessages}>
        {messages.length === 0 && (
          <div className={styles.welcomeMessage}>
            <p>Hello! I'm your Physical AI & Humanoid Robotics assistant.</p>
            <p>Ask me anything about the book content, and I'll help you find relevant information.</p>
          </div>
        )}

        {messages.map((message) => (
          <div key={message.id} className={`${styles.message} ${styles[message.sender]}`}>
            <div className={styles.messageContent}>
              {message.error ? (
                <span className={styles.errorText}>{message.text}</span>
              ) : (
                <div>
                  <p>{message.text}</p>
                  {message.sources && message.sources.length > 0 && (
                    <div className={styles.sources}>
                      <small>Sources:</small>
                      <ul>
                        {message.sources.slice(0, 3).map((source, index) => (
                          <li key={index}>
                            <a
                              href={source.metadata?.url || source.url || '#'}
                              target="_blank"
                              rel="noopener noreferrer"
                              onClick={(e) => e.stopPropagation()}
                            >
                              {source.metadata?.title || source.title || 'Source'}
                            </a>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className={`${styles.message} ${styles.bot}`}>
            <div className={styles.messageContent}>
              <div className={styles.typingIndicator}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className={styles.errorContainer}>
          <p className={styles.errorText}>{error}</p>
        </div>
      )}

      <div className={styles.chatInput}>
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about Physical AI & Humanoid Robotics..."
          disabled={isLoading}
          rows="1"
          className={styles.textInput}
        />
        <button
          onClick={sendMessage}
          disabled={isLoading || !inputValue.trim()}
          className={styles.sendButton}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
