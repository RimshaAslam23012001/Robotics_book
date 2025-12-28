import React from 'react';
import { useAuth } from '../Auth/AuthContext';

const NavbarAuth = () => {
  const { user, loading, signout } = useAuth();

  if (loading) {
    return null; // Don't show auth buttons while loading
  }

  if (user) {
    // User is logged in - show sign out button
    return (
      <a
        href="#"
        className="navbar__link auth-button signin-btn"
        onClick={(e) => {
          e.preventDefault();
          signout();
        }}
      >
        Sign Out
      </a>
    );
  } else {
    // User is not logged in - show sign in and sign up buttons
    return (
      <>
        <a href="/auth/signin" className="navbar__link auth-button signin-btn">Sign In</a>
        <a href="/auth/signup" className="navbar__link auth-button signup-btn">Sign Up</a>
      </>
    );
  }
};

export default NavbarAuth;