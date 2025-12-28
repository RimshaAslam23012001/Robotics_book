# Data Model: Chapter-Level Content Personalization

## User Profile Entity

### Schema
```json
{
  "userId": {
    "type": "string",
    "description": "Unique identifier for the user",
    "required": true,
    "primaryKey": true
  },
  "technicalDepth": {
    "type": "string",
    "enum": ["beginner", "intermediate", "advanced"],
    "description": "User's preferred technical depth level",
    "required": true,
    "default": "intermediate"
  },
  "terminologyComplexity": {
    "type": "string",
    "enum": ["simple", "moderate", "complex"],
    "description": "User's preferred terminology complexity level",
    "required": true,
    "default": "moderate"
  },
  "exampleFocus": {
    "type": "string",
    "enum": ["hardware", "software", "mixed"],
    "description": "User's preferred example focus area",
    "required": true,
    "default": "mixed"
  },
  "aiConceptLevel": {
    "type": "string",
    "enum": ["basic", "intermediate", "advanced"],
    "description": "User's preferred AI concept explanation level",
    "required": true,
    "default": "intermediate"
  },
  "createdAt": {
    "type": "timestamp",
    "description": "Timestamp of profile creation",
    "required": true
  },
  "updatedAt": {
    "type": "timestamp",
    "description": "Timestamp of last profile update",
    "required": true
  }
}
```

### Validation Rules
- `userId` must be a valid user identifier from the authentication system
- All preference fields must be one of the specified enum values
- `createdAt` must be before or equal to `updatedAt`
- Profile must exist before personalization request can be processed

### Relationships
- One-to-one relationship with user authentication system
- Referenced by Personalization Request entity

## Chapter Content Entity

### Schema
```json
{
  "chapterId": {
    "type": "string",
    "description": "Unique identifier for the chapter",
    "required": true,
    "primaryKey": true
  },
  "title": {
    "type": "string",
    "description": "Chapter title",
    "required": true
  },
  "slug": {
    "type": "string",
    "description": "URL-friendly chapter identifier",
    "required": true,
    "unique": true
  },
  "originalContent": {
    "type": "string",
    "description": "Original markdown content of the chapter",
    "required": true
  },
  "metadata": {
    "type": "object",
    "description": "Additional chapter metadata (tags, categories, etc.)",
    "required": false
  },
  "createdAt": {
    "type": "timestamp",
    "description": "Timestamp of content creation",
    "required": true
  }
}
```

### Validation Rules
- `chapterId` must be unique across all chapters
- `slug` must be URL-friendly and unique
- `originalContent` must be valid markdown format
- `title` must not be empty

### Relationships
- Referenced by Personalization Request entity
- Stored in Qdrant vector database for retrieval

## Personalization Request Entity

### Schema
```json
{
  "requestId": {
    "type": "string",
    "description": "Unique identifier for the personalization request",
    "required": true,
    "primaryKey": true
  },
  "userId": {
    "type": "string",
    "description": "Reference to the user making the request",
    "required": true,
    "foreignKey": "User Profile.userId"
  },
  "chapterId": {
    "type": "string",
    "description": "Reference to the chapter being personalized",
    "required": true,
    "foreignKey": "Chapter Content.chapterId"
  },
  "status": {
    "type": "string",
    "enum": ["pending", "processing", "completed", "failed"],
    "description": "Current status of the personalization request",
    "required": true,
    "default": "pending"
  },
  "personalizedContent": {
    "type": "string",
    "description": "Personalized markdown content (temporary storage)",
    "required": false
  },
  "userBackgroundApplied": {
    "type": "object",
    "description": "Snapshot of user background used for personalization",
    "required": false
  },
  "processingTime": {
    "type": "number",
    "description": "Time taken to process the personalization (in milliseconds)",
    "required": false
  },
  "createdAt": {
    "type": "timestamp",
    "description": "Timestamp of request creation",
    "required": true
  },
  "completedAt": {
    "type": "timestamp",
    "description": "Timestamp of request completion",
    "required": false
  }
}
```

### Validation Rules
- `userId` must reference an existing user profile
- `chapterId` must reference an existing chapter
- `status` must be one of the specified enum values
- `personalizedContent` should only exist when status is "completed"
- `processingTime` should only exist when status is "completed" or "failed"

### Relationships
- Many-to-one relationship with User Profile (via `userId`)
- Many-to-one relationship with Chapter Content (via `chapterId`)

## State Transitions

### Personalization Request States
```
PENDING → PROCESSING → COMPLETED
              ↓
             FAILED
```

- **PENDING**: Request created, waiting to be processed
- **PROCESSING**: Currently being processed by the personalization service
- **COMPLETED**: Successfully personalized, content available
- **FAILED**: Personalization failed due to error

### Transition Rules
- PENDING → PROCESSING: When personalization service starts processing
- PROCESSING → COMPLETED: When personalization completes successfully
- PROCESSING → FAILED: When personalization encounters an error
- State cannot transition backwards

## Indexes and Performance Considerations

### Required Indexes
1. **User Profile**: Index on `userId` (primary)
2. **Chapter Content**: Index on `chapterId` (primary), `slug` (unique)
3. **Personalization Request**: Index on `userId`, `chapterId`, `status`, `createdAt`

### Performance Optimizations
- Cache frequently accessed chapter content
- Index user preferences for fast lookup
- Time-based cleanup of completed requests (after 24 hours)
- Asynchronous processing for long-running requests