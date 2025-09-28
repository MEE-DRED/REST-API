@echo off
echo ========================================
echo SMS Transactions API - Testing Script
echo ========================================
echo.

set BASE_URL=http://localhost:8000
set AUTH_HEADER=Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=

echo Testing server connection...
curl -s -o nul -w "HTTP Status: %%{http_code}\n" %BASE_URL%/transactions -H "%AUTH_HEADER%"
if errorlevel 1 (
    echo ERROR: Cannot connect to API server at %BASE_URL%
    echo Make sure the server is running with: python api/server.py
    pause
    exit /b 1
)

echo.
echo ========================================
echo 1. Testing Authentication
echo ========================================

echo.
echo [TEST] Valid credentials (admin:password123)
curl -X GET %BASE_URL%/transactions -H "%AUTH_HEADER%" -H "Content-Type: application/json"

echo.
echo.
echo [TEST] Invalid credentials
curl -X GET %BASE_URL%/transactions -H "Authorization: Basic aW52YWxpZDppbnZhbGlk" -H "Content-Type: application/json"

echo.
echo.
echo [TEST] No authentication
curl -X GET %BASE_URL%/transactions -H "Content-Type: application/json"

echo.
echo.
echo ========================================
echo 2. Testing GET Endpoints
echo ========================================

echo.
echo [TEST] GET all transactions
curl -X GET %BASE_URL%/transactions -H "%AUTH_HEADER%" -H "Content-Type: application/json"

echo.
echo.
echo [TEST] GET specific transaction (ID=1)
curl -X GET %BASE_URL%/transactions/1 -H "%AUTH_HEADER%" -H "Content-Type: application/json"

echo.
echo.
echo [TEST] GET non-existent transaction (ID=999)
curl -X GET %BASE_URL%/transactions/999 -H "%AUTH_HEADER%" -H "Content-Type: application/json"

echo.
echo.
echo [TEST] GET with status filter (COMPLETED)
curl -X GET "%BASE_URL%/transactions?status=COMPLETED" -H "%AUTH_HEADER%" -H "Content-Type: application/json"

echo.
echo.
echo ========================================
echo 3. Testing POST Endpoint
echo ========================================

echo.
echo [TEST] Create new transaction
curl -X POST %BASE_URL%/transactions -H "%AUTH_HEADER%" -H "Content-Type: application/json" -d "{\"type\": \"SEND_MONEY\", \"amount\": 1500.75, \"sender\": \"+1111111111\", \"receiver\": \"+2222222222\", \"reference\": \"TEST_CURL_001\", \"status\": \"PENDING\"}"

echo.
echo.
echo [TEST] Create transaction with missing fields (should fail)
curl -X POST %BASE_URL%/transactions -H "%AUTH_HEADER%" -H "Content-Type: application/json" -d "{\"type\": \"SEND_MONEY\", \"amount\": 100.0}"

echo.
echo.
echo ========================================
echo 4. Testing PUT Endpoint
echo ========================================

echo.
echo [TEST] Update transaction (ID=1)
curl -X PUT %BASE_URL%/transactions/1 -H "%AUTH_HEADER%" -H "Content-Type: application/json" -d "{\"status\": \"COMPLETED\", \"amount\": 5500.0}"

echo.
echo.
echo [TEST] Update non-existent transaction (ID=999)
curl -X PUT %BASE_URL%/transactions/999 -H "%AUTH_HEADER%" -H "Content-Type: application/json" -d "{\"status\": \"COMPLETED\"}"

echo.
echo.
echo ========================================
echo 5. Testing DELETE Endpoint
echo ========================================

echo.
echo [TEST] Delete transaction (you may need to adjust the ID)
echo Note: This will delete a transaction. Use with caution!
echo Skipping DELETE test to preserve data...
echo To test DELETE manually, run:
echo curl -X DELETE %BASE_URL%/transactions/[ID] -H "%AUTH_HEADER%"

echo.
echo.
echo ========================================
echo Testing Completed!
echo ========================================
echo.
echo For more detailed testing, use:
echo python api/test_api.py
echo.
pause