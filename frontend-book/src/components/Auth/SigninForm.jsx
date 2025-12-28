import React, { useState } from 'react';
import { useAuth } from './AuthContext';
import styles from './AuthForm.module.css';

const SigninForm = ({ onSwitchToSignup, onClose }) => {
  const { signin } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await signin(formData.email, formData.password);

      if (result.success) {
        alert('Signin successful!');
        if (onClose) onClose();
      } else {
        alert(result.error || 'Signin failed');
      }
    } catch (error) {
      console.error('Signin error:', error);
      alert('An error occurred during signin');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.authForm}>
      <h2>Sign In</h2>
      <form onSubmit={handleSubmit}>
        <div className={styles.formGroup}>
          <label htmlFor="signin-email">Email</label>
          <input
            type="email"
            id="signin-email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="signin-password">Password</label>
          <input
            type="password"
            id="signin-password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" disabled={loading} className={styles.submitButton}>
          {loading ? 'Signing in...' : 'Sign In'}
        </button>

        <div className={styles.switchForm}>
          Don't have an account? <button type="button" onClick={onSwitchToSignup} className={styles.linkButton}>Sign Up</button>
        </div>
      </form>
    </div>
  );
};

export default SigninForm;