import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../../components/Auth/AuthContext';
import styles from './auth.module.css';

export default function SignUp() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const { signup } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const profileData = {
        softwareBackground: 'beginner',
        programmingLanguages: [],
        aiMlExperience: 'learning',
        hardwareBackground: 'none',
        primaryLearningGoal: ''
      };
      const result = await signup(email, password, name, profileData);
      if (!result.success) {
        setError(result.error || 'Sign up failed');
      }
      // Redirect or show success message
    } catch (err) {
      setError(err.message || 'Sign up failed');
    }
  };

  return (
    <Layout title="Sign Up" description="Create a new account">
      <div className={styles.authContainer}>
        <div className={styles.authForm}>
          <h2>Sign Up</h2>
          {error && <div className={styles.error}>{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className={styles.formGroup}>
              <label htmlFor="name">Full Name:</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="password">Password:</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" className={styles.submitButton}>
              Sign Up
            </button>
          </form>
          <div className={styles.authFooter}>
            <p>Already have an account? <a href="/auth/signin">Sign In</a></p>
          </div>
        </div>
      </div>
    </Layout>
  );
}