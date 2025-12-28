# Authentication Setup with Better Auth Integration

This project now includes a complete authentication system with sign in and sign up functionality. The system is built on top of a mock Better Auth implementation for development purposes.

## Features

- User registration (sign up) with profile information
- User authentication (sign in)
- JWT-based token authentication
- Profile management
- Session management

## API Endpoints

### Authentication Endpoints

- `POST /api/auth/signup` - Create a new user account
- `POST /api/auth/signin` - Authenticate an existing user
- `POST /api/auth/signout` - End the current session
- `GET /api/auth/me` - Get current user's profile (requires auth token)
- `PUT /api/auth/me` - Update current user's profile (requires auth token)

### Request/Response Examples

**Sign Up:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "name": "John Doe",
  "profileData": {
    "softwareBackground": "beginner",
    "programmingLanguages": ["Python", "JavaScript"],
    "aiMlExperience": "learning",
    "hardwareBackground": "none",
    "primaryLearningGoal": "Learn AI concepts"
  }
}
```

**Sign In:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

**Response:**
```json
{
  "user": {
    "id": "user_xxx",
    "email": "user@example.com",
    "name": "John Doe",
    "software_background": "beginner",
    "programming_languages": ["Python", "JavaScript"],
    "ai_ml_experience": "learning",
    "hardware_background": "none",
    "primary_learning_goal": "Learn AI concepts",
    "profile_complete": true,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
  },
  "session": {
    "token": "jwt_token_here",
    "type": "Bearer"
  }
}
```

## Frontend Integration

The frontend includes:
- Sign in and sign up buttons in the navbar
- Complete authentication flow pages at `/auth/signin` and `/auth/signup`
- Authentication context for managing user state
- Protected routes that require authentication

## Environment Variables

The authentication system uses the following environment variables:

- `BETTER_AUTH_SECRET` - Secret key for JWT signing (default: `your-super-secret-key-change-in-production`)
- `AUTH_SECRET_KEY` - Fallback secret key (from existing config)
- `DATABASE_URL` - Database URL for user storage (default: `sqlite:///./better_auth.db`)

## Password Requirements

- Minimum 8 characters
- Must include at least one number
- Must include at least one uppercase letter
- Maximum 72 characters (due to bcrypt limitations)

## Development Notes

The authentication system uses a mock Better Auth implementation that:
- Stores users in memory (not persistent across restarts)
- Uses SHA256 hashing with salt for password security
- Generates JWT tokens for session management
- Supports custom user profile fields

For production deployment, this should be replaced with a real Better Auth or other authentication service.

## Testing

The authentication system has been tested and confirmed to work with:
- User registration and login
- Token-based authentication
- Profile retrieval and updates
- Session management