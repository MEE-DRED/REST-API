# SMS Transactions REST API Documentation

## Overview
This REST API provides secure access to SMS transaction data from a mobile money service. The API implements full CRUD operations with Basic Authentication for security.

## Base URL
```
http://localhost:8000
```

## Authentication
All endpoints require **Basic Authentication**. Include the `Authorization` header with base64-encoded credentials:

```
Authorization: Basic <base64(username:password)>
```

### Valid Credentials
| Username | Password |
|----------|----------|
| admin    | password123 |
| user     | user123 |
| demo     | demo123 |

## Data Model
Transaction objects contain the following fields:

```json
{
  "id": 1,
  "type": "SEND_MONEY",
  "amount": 5000.00,
  "sender": "+1234567890",
  "receiver": "+0987654321",
  "timestamp": "2024-01-15T10:30:00Z",
  "reference": "TXN001",
  "status": "COMPLETED"
}
```

### Field Descriptions
- **id**: Unique transaction identifier (integer)
- **type**: Transaction type (SEND_MONEY, RECEIVE_MONEY, WITHDRAW, DEPOSIT, BILL_PAYMENT)
- **amount**: Transaction amount (float)
- **sender**: Sender phone number or agent ID (string)
- **receiver**: Receiver phone number or service ID (string)
- **timestamp**: ISO 8601 formatted timestamp (string)
- **reference**: Unique transaction reference (string)
- **status**: Transaction status (PENDING, COMPLETED, FAILED)

## Endpoints

### 1. List All Transactions
Retrieve all SMS transactions with optional filtering.

**Endpoint**: `GET /transactions`

**Query Parameters** (Optional):
- `status`: Filter by status (PENDING, COMPLETED, FAILED)
- `type`: Filter by transaction type

**Request Example**:
```bash
curl -X GET http://localhost:8000/transactions \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json"
```

**Request Example with Filtering**:
```bash
curl -X GET "http://localhost:8000/transactions?status=COMPLETED&type=SEND_MONEY" \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="
```

**Response Example** (200 OK):
```json
{
  "transactions": [
    {
      "id": 1,
      "type": "SEND_MONEY",
      "amount": 5000.0,
      "sender": "+1234567890",
      "receiver": "+0987654321",
      "timestamp": "2024-01-15T10:30:00Z",
      "reference": "TXN001",
      "status": "COMPLETED"
    },
    {
      "id": 2,
      "type": "RECEIVE_MONEY",
      "amount": 2500.5,
      "sender": "+0987654321",
      "receiver": "+1234567890",
      "timestamp": "2024-01-15T11:45:00Z",
      "reference": "TXN002",
      "status": "COMPLETED"
    }
  ],
  "total_count": 2,
  "message": "Transactions retrieved successfully"
}
```

### 2. Get Specific Transaction
Retrieve a single transaction by its ID.

**Endpoint**: `GET /transactions/{id}`

**Path Parameters**:
- `id`: Transaction ID (integer)

**Request Example**:
```bash
curl -X GET http://localhost:8000/transactions/1 \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json"
```

**Response Example** (200 OK):
```json
{
  "transaction": {
    "id": 1,
    "type": "SEND_MONEY",
    "amount": 5000.0,
    "sender": "+1234567890",
    "receiver": "+0987654321",
    "timestamp": "2024-01-15T10:30:00Z",
    "reference": "TXN001",
    "status": "COMPLETED"
  },
  "message": "Transaction found"
}
```

### 3. Create New Transaction
Add a new SMS transaction record.

**Endpoint**: `POST /transactions`

**Request Body** (Required fields):
```json
{
  "type": "SEND_MONEY",
  "amount": 1500.75,
  "sender": "+1111111111",
  "receiver": "+2222222222",
  "reference": "TXN999"
}
```

**Optional fields**:
- `timestamp`: Will default to current time if not provided
- `status`: Will default to "PENDING" if not provided

**Request Example**:
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "SEND_MONEY",
    "amount": 1500.75,
    "sender": "+1111111111",
    "receiver": "+2222222222",
    "reference": "TXN999",
    "status": "PENDING"
  }'
```

**Response Example** (201 Created):
```json
{
  "message": "Transaction created successfully",
  "transaction": {
    "id": 21,
    "type": "SEND_MONEY",
    "amount": 1500.75,
    "sender": "+1111111111",
    "receiver": "+2222222222",
    "timestamp": "2024-01-22T10:15:30Z",
    "reference": "TXN999",
    "status": "PENDING"
  }
}
```

### 4. Update Transaction
Update an existing transaction record.

**Endpoint**: `PUT /transactions/{id}`

**Path Parameters**:
- `id`: Transaction ID (integer)

**Request Body** (Include only fields to update):
```json
{
  "status": "COMPLETED",
  "amount": 1600.00
}
```

**Request Example**:
```bash
curl -X PUT http://localhost:8000/transactions/21 \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "COMPLETED",
    "amount": 1600.00
  }'
```

**Response Example** (200 OK):
```json
{
  "message": "Transaction updated successfully",
  "transaction": {
    "id": 21,
    "type": "SEND_MONEY",
    "amount": 1600.0,
    "sender": "+1111111111",
    "receiver": "+2222222222",
    "timestamp": "2024-01-22T10:15:30Z",
    "reference": "TXN999",
    "status": "COMPLETED"
  }
}
```

### 5. Delete Transaction
Remove a transaction record.

**Endpoint**: `DELETE /transactions/{id}`

**Path Parameters**:
- `id`: Transaction ID (integer)

**Request Example**:
```bash
curl -X DELETE http://localhost:8000/transactions/21 \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="
```

**Response Example** (200 OK):
```json
{
  "message": "Transaction deleted successfully",
  "deleted_transaction": {
    "id": 21,
    "type": "SEND_MONEY",
    "amount": 1600.0,
    "sender": "+1111111111",
    "receiver": "+2222222222",
    "timestamp": "2024-01-22T10:15:30Z",
    "reference": "TXN999",
    "status": "COMPLETED"
  }
}
```

## Error Codes

### HTTP Status Codes
| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required or failed |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

### Error Response Format
```json
{
  "error": "Error description",
  "status_code": 400,
  "message": "Additional error details"
}
```

### Common Error Examples

**Unauthorized Access** (401):
```json
{
  "error": "Unauthorized - Invalid or missing credentials",
  "status_code": 401,
  "message": "Please provide valid Basic Authentication credentials"
}
```

**Transaction Not Found** (404):
```json
{
  "error": "Transaction not found",
  "status_code": 404
}
```

**Invalid JSON Data** (400):
```json
{
  "error": "Invalid JSON data",
  "status_code": 400
}
```

**Missing Required Fields** (400):
```json
{
  "error": "Missing required field: amount",
  "status_code": 400
}
```

## Security Considerations

### Basic Authentication Limitations
While this API uses Basic Authentication for simplicity, it has significant limitations:

1. **Credentials in Clear Text**: Base64 encoding is not encryption - credentials are easily decoded
2. **No Session Management**: Credentials must be sent with every request
3. **No Token Expiration**: Credentials remain valid until changed
4. **Vulnerable to Replay Attacks**: No protection against request interception

### Recommended Improvements
For production use, consider these stronger alternatives:

1. **JWT (JSON Web Tokens)**:
   - Stateless authentication
   - Token expiration
   - Digital signatures for integrity

2. **OAuth 2.0**:
   - Industry standard
   - Delegated authorization
   - Refresh token support

3. **API Keys**:
   - Simple implementation
   - Rate limiting support
   - Easy revocation

4. **Additional Security Measures**:
   - HTTPS/TLS encryption
   - Rate limiting
   - Input validation and sanitization
   - CORS configuration
   - Request logging and monitoring

## Testing the API

### Using curl
Examples of testing each endpoint with curl are provided in the endpoint documentation above.

### Using Postman
1. Create a new request
2. Set the method (GET, POST, PUT, DELETE)
3. Enter the URL (e.g., `http://localhost:8000/transactions`)
4. Add Authorization header:
   - Type: Basic Auth
   - Username: admin
   - Password: password123
5. For POST/PUT requests, add JSON body in the request body section

### Python Testing Script
```python
import requests
import base64

# Setup
base_url = "http://localhost:8000"
credentials = base64.b64encode(b"admin:password123").decode("ascii")
headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/json"
}

# Test GET all transactions
response = requests.get(f"{base_url}/transactions", headers=headers)
print("GET /transactions:", response.status_code)
print(response.json())

# Test GET specific transaction
response = requests.get(f"{base_url}/transactions/1", headers=headers)
print("GET /transactions/1:", response.status_code)
print(response.json())
```

## Setup and Installation

1. **Prerequisites**:
   - Python 3.7 or higher
   - No additional dependencies required (uses only standard library)

2. **Run the Server**:
   ```bash
   cd api
   python server.py
   ```

3. **Server will start on**: `http://localhost:8000`

4. **Test the API**: Use the curl examples or testing tools mentioned above