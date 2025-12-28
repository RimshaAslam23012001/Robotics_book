# Quickstart Guide: User Authentication & Personalization Layer

**Feature**: User Authentication & Personalization Layer
**Created**: 2025-12-27

## Overview

This guide provides a quick overview of how to implement and integrate the user authentication and personalization layer into your existing system.

## Prerequisites

- Node.js 18+ (for Better Auth)
- Python 3.9+ (for FastAPI backend)
- Better Auth SDK installed
- Existing FastAPI backend setup
- Docusaurus documentation site

## Installation Steps

### 1. Install Better Auth

```bash
npm install better-auth
```

### 2. Configure Better Auth Server

Create `auth.config.ts`:

```typescript
import { betterAuth } from "better-auth";
import { postgresAdapter } from "better-auth/adapters/postgres";

export const auth = betterAuth({
  database: postgresAdapter({
    url: process.env.DATABASE_URL!,
  }),
  // Extend user schema with custom fields
  user: {
    schema: {
      softwareBackground: {
        type: "string",
        required: true,
      },
      programmingLanguages: {
        type: "string[]",
        required: false,
      },
      aiMlExperience: {
        type: "string",
        required: true,
      },
      hardwareBackground: {
        type: "string",
        required: true,
      },
      primaryLearningGoal: {
        type: "string",
        required: true,
      },
      profileComplete: {
        type: "boolean",
        default: false,
      },
    },
  },
});
```

### 3. Set Up FastAPI Middleware

```python
from fastapi import FastAPI, HTTPException, Depends
from better_auth.client import get_user_from_token

app = FastAPI()

async def get_current_user(token: str = Depends(get_token_from_header)):
    user = await get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
```

### 4. Create API Endpoints

```python
@app.post("/api/user/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    return current_user

@app.put("/api/user/profile")
async def update_user_profile(
    profile_data: dict,
    current_user: dict = Depends(get_current_user)
):
    # Update user profile with provided data
    updated_user = await update_user(current_user["id"], profile_data)
    return {"success": True, "user": updated_user}
```

## Frontend Integration

### 1. Install Client Library

```bash
npm install better-auth
```

### 2. Initialize Auth Client

```javascript
import { createAuthClient } from "better-auth/client";

const authClient = createAuthClient({
  baseURL: "http://localhost:8000/api/auth",
  fetch: globalThis.fetch,
});
```

### 3. Implement Authentication UI

```jsx
import { useAuth } from "better-auth/react";

function SignupForm() {
  const { signUp } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    await signUp({
      email: formData.get("email"),
      password: formData.get("password"),
      name: formData.get("name"),
      profileData: {
        softwareBackground: formData.get("softwareBackground"),
        programmingLanguages: formData.getAll("programmingLanguages"),
        aiMlExperience: formData.get("aiMlExperience"),
        hardwareBackground: formData.get("hardwareBackground"),
        primaryLearningGoal: formData.get("primaryLearningGoal"),
      },
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields for signup */}
    </form>
  );
}
```

## Personalization Implementation

### 1. Retrieve User Context

```javascript
async function getUserPersonalizationContext(token) {
  const response = await fetch("/api/personalization/context", {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });
  return await response.json();
}
```

### 2. Inject Context into RAG Agent

```javascript
function createPersonalizedPrompt(userContext, originalQuery) {
  const { softwareBackground, aiMlExperience, primaryLearningGoal } = userContext;

  const systemPrompt = `
    You are helping a user with ${softwareBackground} software background
    and ${aiMlExperience} AI/ML experience. They are interested in ${primaryLearningGoal}.
    Adjust your responses to match their experience level.
  `;

  return {
    system: systemPrompt,
    user: originalQuery
  };
}
```

## Testing

### 1. Unit Tests

```bash
# Test authentication flows
npm run test auth

# Test API endpoints
pytest tests/test_auth_api.py

# Test personalization logic
npm run test personalization
```

### 2. Integration Tests

```bash
# Test complete user flow
npm run test e2e
```

## Deployment

### 1. Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Auth secrets
AUTH_SECRET=your-secret-key

# API configuration
API_BASE_URL=https://yourdomain.com
```

### 2. Build and Deploy

```bash
# Build frontend with auth components
npm run build

# Deploy backend with auth middleware
docker build -t auth-backend .
docker run -p 8000:8000 auth-backend
```

## Troubleshooting

### Common Issues

1. **Token validation fails**
   - Check that `AUTH_SECRET` is consistent across services
   - Verify JWT configuration

2. **Custom fields not saving**
   - Ensure database schema includes custom fields
   - Check Better Auth configuration

3. **Personalization not working**
   - Verify user context is being retrieved correctly
   - Check that RAG agent is receiving context

## Next Steps

1. Complete full implementation following the detailed plan
2. Perform security review of authentication implementation
3. Test personalization effectiveness with users
4. Monitor performance impact of personalization features