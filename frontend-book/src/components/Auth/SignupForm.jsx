import React, { useState } from 'react';
import { useAuth } from './AuthContext';
import styles from './AuthForm.module.css';

const SignupForm = ({ onSwitchToSignin, onClose }) => {
  const { signup } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    profileData: {
      softwareBackground: 'beginner',
      programmingLanguages: [],
      aiMlExperience: 'learning',
      hardwareBackground: 'none',
      primaryLearningGoal: ''
    }
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name.startsWith('profile.')) {
      const profileField = name.split('.')[1];
      setFormData(prev => ({
        ...prev,
        profileData: {
          ...prev.profileData,
          [profileField]: value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleLanguageChange = (e) => {
    const value = e.target.value;
    setFormData(prev => ({
      ...prev,
      profileData: {
        ...prev.profileData,
        programmingLanguages: value ? value.split(',').map(lang => lang.trim()) : []
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});

    try {
      const result = await signup(
        formData.email,
        formData.password,
        formData.name,
        formData.profileData
      );

      if (result.success) {
        alert('Signup successful!');
        if (onClose) onClose();
      } else {
        if (result.error && typeof result.error === 'object') {
          setErrors(result.error);
        } else {
          alert(result.error || 'Signup failed');
        }
      }
    } catch (error) {
      console.error('Signup error:', error);
      alert('An error occurred during signup');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.authForm}>
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <div className={styles.formGroup}>
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="softwareBackground">Software Background</label>
          <select
            id="softwareBackground"
            name="profile.softwareBackground"
            value={formData.profileData.softwareBackground}
            onChange={handleChange}
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="programmingLanguages">Programming Languages (comma-separated)</label>
          <input
            type="text"
            id="programmingLanguages"
            name="profile.programmingLanguages"
            value={formData.profileData.programmingLanguages.join(', ')}
            onChange={handleLanguageChange}
            placeholder="e.g., Python, JavaScript, C++"
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="aiMlExperience">AI/ML Experience</label>
          <select
            id="aiMlExperience"
            name="profile.aiMlExperience"
            value={formData.profileData.aiMlExperience}
            onChange={handleChange}
          >
            <option value="no">No Experience</option>
            <option value="learning">Learning</option>
            <option value="yes">Experienced</option>
          </select>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="hardwareBackground">Hardware Background</label>
          <select
            id="hardwareBackground"
            name="profile.hardwareBackground"
            value={formData.profileData.hardwareBackground}
            onChange={handleChange}
          >
            <option value="none">None</option>
            <option value="cpu">CPU</option>
            <option value="gpu">GPU</option>
            <option value="embedded">Embedded Systems</option>
          </select>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="primaryLearningGoal">Primary Learning Goal</label>
          <input
            type="text"
            id="primaryLearningGoal"
            name="profile.primaryLearningGoal"
            value={formData.profileData.primaryLearningGoal}
            onChange={handleChange}
            placeholder="What do you want to learn?"
          />
        </div>

        <button type="submit" disabled={loading} className={styles.submitButton}>
          {loading ? 'Signing up...' : 'Sign Up'}
        </button>

        <div className={styles.switchForm}>
          Already have an account? <button type="button" onClick={onSwitchToSignin} className={styles.linkButton}>Sign In</button>
        </div>
      </form>
    </div>
  );
};

export default SignupForm;