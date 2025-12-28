# Data Model: Chapter-Level Urdu Translation

## User Session Entity

### Schema
```json
{
  "userId": {
    "type": "string",
    "description": "Unique identifier for the user",
    "required": true,
    "primaryKey": true
  },
  "authToken": {
    "type": "string",
    "description": "Authentication token for validation",
    "required": true
  },
  "translationPreferences": {
    "type": "object",
    "description": "User preferences for translation settings",
    "required": false
  },
  "createdAt": {
    "type": "timestamp",
    "description": "Timestamp of session creation",
    "required": true
  }
}
```

### Validation Rules
- `userId` must be a valid user identifier from the authentication system
- `authToken` must be a valid authentication token
- `createdAt` must be before or equal to current time
- Session must exist before translation request can be processed

### Relationships
- One-to-one relationship with user authentication system
- Referenced by Translation Request entity

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
- Referenced by Translation Request entity
- Stored in Qdrant vector database for retrieval

## Translation Request Entity

### Schema
```json
{
  "requestId": {
    "type": "string",
    "description": "Unique identifier for the translation request",
    "required": true,
    "primaryKey": true
  },
  "userId": {
    "type": "string",
    "description": "Reference to the user making the request",
    "required": true,
    "foreignKey": "User Session.userId"
  },
  "chapterId": {
    "type": "string",
    "description": "Reference to the chapter being translated",
    "required": true,
    "foreignKey": "Chapter Content.chapterId"
  },
  "status": {
    "type": "string",
    "enum": ["pending", "processing", "completed", "failed"],
    "description": "Current status of the translation request",
    "required": true,
    "default": "pending"
  },
  "translatedContent": {
    "type": "string",
    "description": "Translated Urdu markdown content (temporary storage)",
    "required": false
  },
  "processingTime": {
    "type": "number",
    "description": "Time taken to process the translation (in milliseconds)",
    "required": false
  },
  "translationQuality": {
    "type": "string",
    "enum": ["high", "medium", "low"],
    "description": "Quality assessment of the translation",
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
- `userId` must reference an existing user session
- `chapterId` must reference an existing chapter
- `status` must be one of the specified enum values
- `translatedContent` should only exist when status is "completed"
- `processingTime` should only exist when status is "completed" or "failed"

### Relationships
- Many-to-one relationship with User Session (via `userId`)
- Many-to-one relationship with Chapter Content (via `chapterId`)

## State Transitions

### Translation Request States
```
PENDING → PROCESSING → COMPLETED
              ↓
             FAILED
```

- **PENDING**: Request created, waiting to be processed
- **PROCESSING**: Currently being processed by the translation service
- **COMPLETED**: Successfully translated, content available
- **FAILED**: Translation failed due to error

### Transition Rules
- PENDING → PROCESSING: When translation service starts processing
- PROCESSING → COMPLETED: When translation completes successfully
- PROCESSING → FAILED: When translation encounters an error
- State cannot transition backwards

## Indexes and Performance Considerations

### Required Indexes
1. **User Session**: Index on `userId` (primary)
2. **Chapter Content**: Index on `chapterId` (primary), `slug` (unique)
3. **Translation Request**: Index on `userId`, `chapterId`, `status`, `createdAt`

### Performance Optimizations
- Cache frequently accessed chapter content
- Index user sessions for fast lookup
- Time-based cleanup of completed requests (after 24 hours)
- Asynchronous processing for long-running requests