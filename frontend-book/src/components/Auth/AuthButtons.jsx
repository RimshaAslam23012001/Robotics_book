import React, { useState } from 'react';
import { useAuth } from './AuthContext';
import { Modal } from 'react-responsive-modal';
import 'react-responsive-modal/styles.css';
import SignupForm from './SignupForm';
import SigninForm from './SigninForm';
import styles from './AuthButtons.module.css';

const AuthButtons = () => {
  const { user, signout, loading } = useAuth();
  const [openModal, setOpenModal] = useState(false);
  const [modalType, setModalType] = useState('signin'); // 'signin' or 'signup'

  const onOpenModal = (type = 'signin') => {
    setModalType(type);
    setOpenModal(true);
  };

  const onCloseModal = () => {
    setOpenModal(false);
  };

  const handleSignout = async () => {
    await signout();
  };

  if (loading) {
    return <div className={styles.authButton}>Loading...</div>;
  }

  return (
    <div className={styles.authContainer}>
      {user ? (
        <div className={styles.userMenu}>
          <span className={styles.userName}>{user.name || user.email}</span>
          <button onClick={handleSignout} className={styles.signoutButton}>
            Sign Out
          </button>
        </div>
      ) : (
        <div className={styles.authButtons}>
          <button
            onClick={() => onOpenModal('signin')}
            className={`${styles.authButton} ${styles.signinButton}`}
          >
            Sign In
          </button>
          <button
            onClick={() => onOpenModal('signup')}
            className={`${styles.authButton} ${styles.signupButton}`}
          >
            Sign Up
          </button>
        </div>
      )}

      <Modal
        open={openModal}
        onClose={onCloseModal}
        center
        styles={{
          modal: {
            padding: '0',
            borderRadius: '8px',
            overflow: 'hidden'
          }
        }}
      >
        <div className={styles.modalContent}>
          <button className={styles.closeButton} onClick={onCloseModal}>
            ×
          </button>
          {modalType === 'signin' ? (
            <SigninForm
              onSwitchToSignup={() => setModalType('signup')}
              onClose={onCloseModal}
            />
          ) : (
            <SignupForm
              onSwitchToSignin={() => setModalType('signin')}
              onClose={onCloseModal}
            />
          )}
        </div>
      </Modal>
    </div>
  );
};

export default AuthButtons;