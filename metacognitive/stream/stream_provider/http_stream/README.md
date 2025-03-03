# HTTP Stream API Documentation

This document outlines the HTTP Stream API that provides real-time communication capabilities using Server-Sent Events (SSE) for chat applications.

## Overview

The HTTP Stream API enables clients to:
- Create new chat sessions
- Send chat messages and receive streaming responses
- Reconnect to active streams in case of disconnection
- Retrieve session and request information

All communication is based on HTTP, with streaming responses delivered through Server-Sent Events (SSE).

## Base URL

All API endpoints share the base URL:

```
http://127.0.0.1:7072/levia
```

## Authentication

Session management is handled through session IDs. A valid session ID must be obtained through the session creation endpoint and included in subsequent requests.

## Endpoints

### Create Chat Session

Creates a new chat session for a user.

**Endpoint:** `POST /chat/create`

**Request Body:**
```json
{
  "user_id": "string"
}
```

**Response:**
```json
{
  "status": "success",
  "session_id": "uuid-string",
  "message": "New chat session created"
}
```

**Status Codes:**
- `201`: Session created successfully
- `400`: Missing required parameters
- `500`: Server error

**Notes:**
- Session IDs are valid for 72 hours (259200 seconds)
- Each user can have only one active session at a time

### Send Chat Message

Sends a chat message and initiates a streaming response.

**Endpoint:** `POST /chat`

**Request Body:**
```json
{
  "user_id": "string",
  "intent": "string",
  "session_id": "uuid-string"
}
```

**Response:**
```json
{
  "status": "success",
  "request_id": "uuid-string",
  "message": "Processing started, connect to /levia/chat/stream/{request_id} for updates"
}
```

**Status Codes:**
- `202`: Request accepted for processing
- `400`: Missing required parameters
- `401`: Invalid or expired session ID
- `500`: Server error

**Notes:**
- The `request_id` returned should be used to connect to the streaming endpoint
- Processing occurs asynchronously

### Stream Chat Response

Streams the chat response in real-time using Server-Sent Events (SSE).

**Endpoint:** `GET /chat/stream/{request_id}`

**Parameters:**
- `request_id`: UUID string obtained from the `/chat` endpoint

**Response:**
Server-Sent Events stream with event data in the following format:

```
data: {"type": "log", "data": {"content": "string", "type": "string", "ch_id": "string"}}

data: {"type": "complete", "data": {"reply": "string"}}

data: {"type": "error", "data": {"error": "string"}}
```

**Event Types:**
- `log`: Intermediate log messages during processing
- `complete`: Final response message
- `error`: Error message if processing fails

**Notes:**
- The stream automatically closes after receiving a `complete` or `error` event
- Stream reconnection is supported and will replay any missed log messages
- Cached results are available for 5 minutes after completion

### Get User's Active Request

Retrieves the current active request ID for a user.

**Endpoint:** `GET /chat/request/{user_id}`

**Parameters:**
- `user_id`: The user's unique identifier

**Response:**
```json
{
  "status": "success",
  "request_id": "uuid-string"
}
```

**Status Codes:**
- `200`: Request ID found
- `404`: No active request found for the user
- `500`: Server error

## Data Retention

- Session IDs: 72 hours
- Request processing data: 30 minutes
- Result cache: 5 minutes after completion

## Error Handling

All errors are returned with appropriate HTTP status codes and a JSON response body:

```json
{
  "status": "error",
  "message": "Error description"
}
```

## SSE Connection Management

Clients should implement appropriate reconnection logic for the SSE stream. The server supports reconnection by:
- Maintaining logs of previous messages
- Providing cached results for completed requests
- Handling connection timeouts gracefully

## Usage Examples

### Complete Chat Flow

1. Create a session:
```bash
curl -X POST http://127.0.0.1:7072/levia/chat/create \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'
```

2. Send a chat message:
```bash
curl -X POST http://127.0.0.1:7072/levia/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "intent": "Hello, how are you?", "session_id": "received-session-id"}'
```

3. Connect to the SSE stream:
```bash
curl -N http://127.0.0.1:7072/levia/chat/stream/received-request-id
```

4. Check active request (optional):
```bash
curl http://127.0.0.1:7072/levia/chat/request/user123
```