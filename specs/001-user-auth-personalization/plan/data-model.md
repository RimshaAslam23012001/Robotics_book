# Data Model: User Authentication & Personalization Layer

**Feature**: User Authentication & Personalization Layer
**Created**: 2025-12-27

## Entity Definitions

### User Profile
**Description**: Extended user information including technical background for personalization

**Fields**:
- `id` (string, required): Unique identifier from Better Auth
- `email` (string, required): User's email address from Better Auth
- `name` (string, required): User's display name from Better Auth
- `createdAt` (timestamp, required): Account creation timestamp from Better Auth
- `updatedAt` (timestamp, required): Last update timestamp from Better Auth
- `softwareBackground` (enum, required): User's software experience level
  - Values: "beginner", "intermediate", "advanced"
- `programmingLanguages` (array<string>, optional): Programming languages known by user
  - Example: ["Python", "JavaScript", "C++"]
- `aiMlExperience` (enum, required): User's AI/ML experience level
  - Values: "yes", "no", "learning"
- `hardwareBackground` (enum, required): User's hardware experience
  - Values: "cpu", "gpu", "embedded", "none"
- `primaryLearningGoal` (string, required): User's main learning objective
- `profileComplete` (boolean, required): Whether user has completed background info
  - Default: false

**Validation Rules**:
- `email` must be a valid email format
- `softwareBackground` must be one of the defined enum values
- `aiMlExperience` must be one of the defined enum values
- `hardwareBackground` must be one of the defined enum values
- `primaryLearningGoal` must be 1-200 characters
- `programmingLanguages` can have 0-10 entries
- `profileComplete` is set to true when all required background fields are filled

**Relationships**:
- Extends Better Auth's base User entity
- Related to authentication sessions through Better Auth

### Authentication Token
**Description**: JWT tokens issued by Better Auth for session management

**Fields**:
- `token` (string, required): JWT token string
- `type` (string, required): Token type (e.g., "Bearer")
- `expiresAt` (timestamp, required): Token expiration time
- `userId` (string, required): Reference to the user ID

**Validation Rules**:
- Token must be properly formatted JWT
- Token must not be expired
- Token must be properly signed by Better Auth

### Personalization Context
**Description**: User-specific data used for content personalization

**Fields**:
- `userId` (string, required): Reference to the user ID
- `softwareBackground` (string, required): User's software experience level
- `programmingLanguages` (array<string>, optional): Programming languages known
- `aiMlExperience` (string, required): User's AI/ML experience level
- `hardwareBackground` (string, required): User's hardware experience
- `primaryLearningGoal` (string, required): User's main learning objective
- `difficultyLevel` (string, required): Derived difficulty level based on softwareBackground
  - Values: "basic", "intermediate", "advanced"

**Validation Rules**:
- All fields must match the corresponding user profile data
- `difficultyLevel` must be consistent with `softwareBackground`
- Context data must be fresh (not older than 1 hour for accuracy)

## State Transitions

### User Profile States
1. **Unregistered**: User has not signed up
2. **Registered (Incomplete)**: User has signed up but not filled background info
   - Transition: User completes background information
3. **Registered (Complete)**: User has completed all required background info
   - Transition: User updates profile information

### Authentication States
1. **Unauthenticated**: User is not logged in
2. **Authenticating**: User is in the process of signing in
3. **Authenticated**: User has valid session tokens
4. **Session Expired**: User's tokens have expired
5. **Logged Out**: User has explicitly signed out

## Data Flow

### User Registration Flow
1. User provides credentials and background information
2. Better Auth creates user record with extended schema
3. User profile is stored with `profileComplete: true`
4. Authentication tokens are issued

### Profile Update Flow
1. Authenticated user requests to update profile
2. Token is validated for the requesting user
3. Profile data is updated in Better Auth
4. `updatedAt` timestamp is updated

### Personalization Context Flow
1. Authenticated user makes request requiring personalization
2. Authentication token is validated
3. User profile is retrieved from Better Auth
4. Personalization context is created from profile data
5. Context is injected into RAG agent processing

## Constraints and Assumptions

### Constraints
- User profile data is stored within Better Auth's user schema
- Authentication must use Better Auth SDK only
- Personalization is read-only (no model fine-tuning)
- Auth must not affect existing vector storage

### Assumptions
- Better Auth provides reliable JWT token validation
- User profile data changes infrequently
- Personalization context can be reconstructed from user profile
- Network requests to Better Auth are reasonably fast