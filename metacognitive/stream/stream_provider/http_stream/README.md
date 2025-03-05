# HTTP Stream API Documentation

This documentation describes the API endpoints provided by the HTTP Stream service.

## Overview

The HTTP Stream API provides real-time communication capabilities between clients and the server. It allows creating chat sessions, sending messages, and receiving responses in real-time through Server-Sent Events (SSE).

### User ID

The `user_id` parameter is a crucial concept in this API:

*   Each `user_id` represents a unique individual user in the developer's application
*   Levia uses the `user_id` to store and differentiate chat contexts between different users
*   Developers are responsible for generating and managing unique user IDs for their user base
*   Each user's conversation history and context is isolated based on their `user_id`
*   The same `user_id` should be used consistently across sessions for the same user to maintain context


## Base URL

All API endpoints are relative to the base URL:

```
https://api.levia.us
```

## Authentication

Authentication for this API requires an API key that must be included in the header of all requests.

### API Key Authentication

1. Register a developer account on the developer platform
2. Obtain an API key from your developer dashboard
3. Include the API key in the request header as follows:

```
Authorization: Bearer YOUR_API_KEY
```

All requests without a valid API key will be rejected with a `401 Unauthorized` response.

---

## Endpoints

### Create Chat Session

Creates a new chat session for a user.

**URL**: `/levia/chat/create`

**Method**: `POST`

**Request Body**:

```json
{
  "user_id": "string" // Required: Unique identifier for the user
}
```

**Success Response**:

- **Code**: `201 CREATED`
- **Content**:

```json
{
  "status": "success",
  "session_id": "uuid-string",
  "message": "New chat session created"
}
```

**Error Response**:

- **Code**: `400 BAD REQUEST`
- **Content**:

```json
{
  "status": "error",
  "message": "Missing user_id parameter"
}
```

OR

- **Code**: `500 INTERNAL SERVER ERROR`
- **Content**:

```json
{
  "status": "error",
  "message": "Error description"
}
```

**Notes**:

- Session IDs are automatically generated using UUID4
- Sessions expire after 72 hours (259200 seconds)

---

### Send Chat Message

Processes a chat message and returns a request ID for streaming the response.

**URL**: `/levia/chat`

**Method**: `POST`

**Request Body**:

```json
{
  "user_id": "string",     // Required: Unique identifier for the user
  "intent": "string",      // Required: The message or intent to process
  "session_id": "string"   // Required: Valid session ID from create chat endpoint
}
```

**Success Response**:

- **Code**: `202 ACCEPTED`
- **Content**:

```json
{
  "status": "success",
  "request_id": "uuid-string",
  "message": "Processing started, connect to /levia/chat/stream/{request_id} for updates"
}
```

**Error Response**:

- **Code**: `401 UNAUTHORIZED`
- **Content**:

```json
{
  "status": "error",
  "message": "Session ID does not exist or has expired"
}
```

OR

- **Code**: `401 UNAUTHORIZED`
- **Content**:

```json
{
  "status": "error",
  "message": "Session ID does not belong to this user"
}
```

**Notes**:

- The returned `request_id` should be used to connect to the streaming endpoint
- Processing occurs asynchronously in a background thread
- Request processing status is stored in Redis with a 30-minute (1800 seconds) TTL

---

### Stream Chat Response

Streams the real-time response to a chat message using Server-Sent Events (SSE).

**URL**: `/levia/chat/stream/{request_id}`

**Method**: `GET`

**URL Parameters**:

- `request_id`: The UUID returned by the chat endpoint

**Response**:

The response is a Server-Sent Events (SSE) stream with `text/event-stream` content type.

**Event Data Formats**:

1. **Stream Update**:
```json
{
  "type": "stream",
  "data": {
    "content": "string",
    "type": "string",
    "ch_id": "string"
  }
}
```

2. **Completion Event**:
```json
{
  "type": "complete",
  "data": {
    "reply": "string"
  }
}
```

3. **Error Event**:
```json
{
  "type": "error",
  "data": {
    "error": "Error description"
  }
}
```

**Notes**:

- The connection stays open until a `complete` or `error` event is received
- Upon connection, any existing logs for the request will be sent first
- If the request ID is invalid or expired, an error event will be sent
- Completed responses are cached for 5 minutes (300 seconds) for reconnections

---

### Get User's Active Request

Returns the active request ID for a specific user.

**URL**: `/levia/chat/request/{user_id}`

**Method**: `GET`

**URL Parameters**:

- `user_id`: The unique identifier for the user

**Success Response**:

- **Code**: `200 OK`
- **Content**:

```json
{
  "status": "success",
  "request_id": "uuid-string"
}
```

**Error Response**:

- **Code**: `404 NOT FOUND`
- **Content**:

```json
{
  "status": "error",
  "message": "No active request found for this user"
}
```

**Notes**:

- This endpoint is useful for clients that need to reconnect to an ongoing request

---

## Data Lifecycle

1. Session data is stored for 72 hours (259200 seconds)
2. Request processing data has a TTL of 30 minutes (1800 seconds)
3. Result cache is stored for 5 minutes (300 seconds)
4. Logs for each request are stored for 30 minutes (1800 seconds)

## Error Handling

The API returns appropriate HTTP status codes and error messages in JSON format:

- `400`: Bad Request - Missing or invalid parameters
- `401`: Unauthorized - Invalid or expired session
- `404`: Not Found - Resource not available
- `500`: Internal Server Error - Server-side error

## Implementation Notes

- Uses Redis for pub/sub messaging, data storage, and caching
- Implements a singleton pattern to ensure only one server instance per port
- Generates unique node IDs for server instances
- Handles reconnection scenarios by caching logs and results