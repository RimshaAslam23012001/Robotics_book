// Translation and auth functionality for navbar buttons
function initializeNavbarFeatures() {
  // Wait for the DOM to be fully loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFeatures);
  } else {
    initFeatures();
  }

  function initFeatures() {
    // Initialize translation button
    initializeTranslationButton();

    // Initialize auth buttons
    initializeAuthButtons();
  }

  function initializeTranslationButton() {
    const toggleButton = document.getElementById('translation-toggle-btn');
    if (!toggleButton) return;

    // Check for saved preference in localStorage
    const savedPreference = localStorage.getItem('book-language-preference');
    let isUrdu = savedPreference === 'urdu';

    // Apply saved preference on page load
    if (isUrdu) {
      document.documentElement.dir = 'rtl';
      document.body.classList.add('urdu-mode');
      toggleButton.textContent = 'English';
      toggleButton.classList.add('translated');
    } else {
      document.documentElement.dir = 'ltr';
      document.body.classList.remove('urdu-mode');
      toggleButton.textContent = 'اردو ترجمہ';
      toggleButton.classList.remove('translated');
    }

    // Add click event listener to the toggle button
    toggleButton.addEventListener('click', function() {
      isUrdu = !isUrdu;

      if (isUrdu) {
        // Switch to Urdu mode
        document.documentElement.dir = 'rtl';
        document.body.classList.add('urdu-mode');
        toggleButton.textContent = 'English';
        toggleButton.classList.add('translated');
        localStorage.setItem('book-language-preference', 'urdu');
      } else {
        // Switch to English mode
        document.documentElement.dir = 'ltr';
        document.body.classList.remove('urdu-mode');
        toggleButton.textContent = 'اردو ترجمہ';
        toggleButton.classList.remove('translated');
        localStorage.setItem('book-language-preference', 'english');
      }

      // Trigger a custom event to notify other components of the language change
      window.dispatchEvent(new CustomEvent('languageChange', { detail: { isUrdu } }));
    });
  }

  function initializeAuthButtons() {
    const authPlaceholder = document.getElementById('auth-buttons-placeholder');
    if (!authPlaceholder) return;

    // Check if user is authenticated
    const token = localStorage.getItem('auth_token');
    const user = token ? JSON.parse(localStorage.getItem('user') || 'null') : null;

    if (user) {
      // User is logged in - show sign out button
      authPlaceholder.innerHTML = `
        <a href="#" id="signout-btn" class="navbar__link auth-button signin-btn">Sign Out</a>
      `;

      const signOutBtn = document.getElementById('signout-btn');
      if (signOutBtn) {
        signOutBtn.addEventListener('click', function(e) {
          e.preventDefault();
          localStorage.removeItem('auth_token');
          localStorage.removeItem('user');
          window.location.reload(); // Refresh to update navbar
        });
      }
    } else {
      // User is not logged in - show sign in and sign up buttons
      authPlaceholder.innerHTML = `
        <a href="/auth/signin" class="navbar__link auth-button signin-btn">Sign In</a>
        <a href="/auth/signup" class="navbar__link auth-button signup-btn">Sign Up</a>
      `;
    }
  }

  // Listen for auth state changes (if triggered by other parts of the app)
  window.addEventListener('authChange', function() {
    initializeAuthButtons();
  });
}

// Initialize the navbar features when the script loads
initializeNavbarFeatures();