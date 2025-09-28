# SMS Transactions REST API

A secure REST API for managing mobile money SMS transaction data, built with Python's `http.server` module and featuring Basic Authentication, CRUD operations, and data structure algorithm comparisons.

##  Project Overview

This project implements a complete REST API system for processing SMS transaction data from a mobile money service. It includes:

- **XML Data Parsing**: Convert XML transaction records to JSON format
- **CRUD API Endpoints**: Full Create, Read, Update, Delete operations
- **Basic Authentication**: Secure endpoint access with credentials
- **Data Structure Algorithms**: Performance comparison between linear search and dictionary lookup
- **Comprehensive Testing**: Automated test suites and manual testing tools
- **Complete Documentation**: Detailed API documentation with examples

##  Quick Start

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Installation & Setup

1. **Clone or download this repository**
   ```bash
   cd "c:\Users\HP\Desktop\REST API"
   ```

2. **Start the API server**
   ```bash
   python api/server.py
   ```

3. **Server will run on** `http://localhost:8000`

### Testing the API

**Option 1: Automated Python Testing**
```bash
python api/test_api.py
```

**Option 2: Windows Batch Testing**
```batch
test_api_curl.bat
```

**Option 3: Manual curl Testing**
```bash
curl -X GET http://localhost:8000/transactions \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json"
```

## Project Structure

```
REST API/
├── api/                    # API implementation
│   ├── server.py          # Main REST API server
│   └── test_api.py        # Automated API testing
├── dsa/                   # Data Structures & Algorithms
│   └── xml_parser.py      # XML parsing and search comparison
├── data/                  # Data files
│   └── modified_sms_v2.xml # Sample SMS transaction data
├── docs/                  # Documentation
│   └── api_docs.md        # Complete API documentation
├── screenshots/           # Test screenshots (to be added)
├── test_api_curl.bat     # Windows curl testing script
└── README.md             # This file
```

##  Authentication

The API uses **Basic Authentication** with the following credentials:

| Username | Password    |
|----------|-------------|
| admin    | password123 |
| user     | user123     |
| demo     | demo123     |

**Example Authorization Header:**
```
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
```

## API Endpoints

### Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/transactions` | List all transactions |
| GET    | `/transactions/{id}` | Get specific transaction |
| POST   | `/transactions` | Create new transaction |
| PUT    | `/transactions/{id}` | Update transaction |
| DELETE | `/transactions/{id}` | Delete transaction |

### Example Usage

**Get All Transactions:**
```bash
curl -X GET http://localhost:8000/transactions \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="
```

**Create New Transaction:**
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "SEND_MONEY",
    "amount": 1500.75,
    "sender": "+1234567890",
    "receiver": "+0987654321",
    "reference": "TXN001"
  }'
```

##  Data Structure & Algorithm Analysis

### Implemented Search Methods

1. **Linear Search**: O(n) time complexity
   - Scans through list sequentially
   - Simple but inefficient for large datasets

2. **Dictionary Lookup**: O(1) average time complexity
   - Hash-based direct access
   - Significantly faster for lookups

### Performance Comparison

Run the DSA demonstration:
```bash
python dsa/xml_parser.py
```

**Sample Results:**
- Dictionary lookup is ~50-100x faster than linear search
- Performance difference increases with dataset size
- Dictionary uses more memory but provides constant-time access

### Alternative Data Structures
- **Binary Search Tree**: O(log n) search, maintains sorted order
- **Hash Set**: O(1) for existence checks
- **B-Tree**: Efficient for disk-based storage systems

##  Testing

### 1. Automated Python Testing
```bash
python api/test_api.py
```

Tests include:
- Authentication validation (valid/invalid credentials)
- All CRUD operations
- Error handling
- Response format validation

### 2. Windows Batch Script
```batch
test_api_curl.bat
```

Provides curl-based testing for Windows users.

### 3. Manual Testing with Postman
1. Import the endpoint URLs
2. Set Basic Authentication
3. Test each endpoint with sample data

### 4. Expected Test Results
- ✅ Authentication with valid credentials
- ❌ Authentication with invalid credentials  
- ✅ GET all transactions
- ✅ GET specific transaction
- ❌ GET non-existent transaction (404)
- ✅ POST create transaction
- ❌ POST with missing fields (400)
- ✅ PUT update transaction
- ✅ DELETE transaction

##  Security Analysis

### Basic Authentication Limitations
1. **Base64 Encoding**: Not encryption, easily decoded
2. **Credentials in Every Request**: No session management
3. **No Token Expiration**: Credentials valid indefinitely
4. **Replay Attack Vulnerability**: No request uniqueness

### Recommended Security Improvements
1. **JWT (JSON Web Tokens)**
   - Stateless authentication
   - Token expiration
   - Digital signatures

2. **OAuth 2.0**
   - Industry standard
   - Delegated authorization
   - Refresh token support

3. **Additional Measures**
   - HTTPS/TLS encryption
   - Rate limiting
   - Input validation
   - Request logging

##  Documentation

### Complete API Documentation
See [docs/api_docs.md](docs/api_docs.md) for:
- Detailed endpoint documentation
- Request/response examples
- Error codes and handling
- Security considerations

### Data Model
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

##  Assignment Requirements Checklist

- **Data Parsing**: XML parsed to JSON objects
- **API Implementation**: All CRUD endpoints functional
- **Authentication**: Basic Auth with 401 error handling
- **API Documentation**: Complete with examples and error codes
- **DSA Integration**: Linear search vs dictionary lookup comparison
- **Testing**: Comprehensive test suite with multiple methods

