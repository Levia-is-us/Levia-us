import pytest
import json
import uuid
from unittest.mock import Mock, patch
import os
import sys
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from metacognitive.stream.stream_provider.http_stream.http_stream import HTTPStream

@pytest.fixture
def app():
    stream = HTTPStream(port=7073)  # Using different port to avoid conflicts
    return stream.app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_redis():
    with patch('metacognitive.stream.stream_provider.http_stream.http_stream.redis_tool') as mock:
        yield mock

def test_create_chat_session(client, mock_redis):
    """Test chat session creation endpoint"""
    # Prepare test data
    test_user_id = "test_user_123"
    
    # Send POST request
    response = client.post(
        '/levia/chat/create',
        json={'user_id': test_user_id}
    )
    
    # Verify response
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'session_id' in data
    assert isinstance(data['session_id'], str)
    
    # Verify Redis operation
    mock_redis.setex.assert_called_once()

def test_create_chat_session_missing_user_id(client):
    """Test chat session creation with missing user_id parameter"""
    response = client.post('/levia/chat/create', json={})
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'Missing user_id parameter' in data['message']

@pytest.mark.asyncio
async def test_chat_endpoint(client, mock_redis):
    """Test chat endpoint"""
    # Mock data
    test_data = {
        'user_id': 'test_user_123',
        'intent': 'test intent',
        'session_id': str(uuid.uuid4())
    }
    
    # Mock Redis session_id return
    mock_redis.get_value.return_value = test_data['session_id']
    
    # Send request
    response = client.post(
        '/levia/chat',
        json=test_data
    )
    
    # Verify response
    assert response.status_code == 202
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'request_id' in data

def test_get_user_request(client, mock_redis):
    """Test get user request ID endpoint"""
    test_user_id = "test_user_123"
    test_request_id = str(uuid.uuid4())
    
    # Mock Redis request_id return
    mock_redis.get_value.return_value = test_request_id
    
    # Send request
    response = client.get(f'/levia/chat/request/{test_user_id}')
    
    # Verify response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['request_id'] == test_request_id

def test_get_user_request_not_found(client, mock_redis):
    """Test get non-existent user request ID"""
    test_user_id = "nonexistent_user"
    
    # Mock Redis return None
    mock_redis.get_value.return_value = None
    
    # Send request
    response = client.get(f'/levia/chat/request/{test_user_id}')
    
    # Verify response
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'No active request found' in data['message']