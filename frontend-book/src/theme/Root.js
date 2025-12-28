import React from 'react';
import { AuthProvider } from '../components/Auth/AuthContext';
import { TranslationProvider } from '../contexts/TranslationContext';

export default function Root({ children }) {
  return (
    <TranslationProvider>
      <AuthProvider>{children}</AuthProvider>
    </TranslationProvider>
  );
}