"""
API Testing Script
Comprehensive testing of the SMS Transactions REST API
"""

import requests
import base64
import json
import time
from typing import Dict, List, Optional


class APITester:
    """Test suite for the SMS Transactions REST API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.valid_credentials = {
            'admin': 'password123',
            'user': 'user123',
            'demo': 'demo123'
        }
        self.test_results = []
    
    def get_auth_header(self, username: str, password: str) -> Dict[str, str]:
        """Create Basic Auth header."""
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode("ascii")
        return {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json"
        }
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results."""
        status = "PASS" if success else "FAIL"
        result = {
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.test_results.append(result)
        print(f"[{status}] {test_name}: {details}")
    
    def test_authentication(self):
        """Test authentication with valid and invalid credentials."""
        print("\n=== Testing Authentication ===")
        
        # Test valid credentials
        for username, password in self.valid_credentials.items():
            try:
                headers = self.get_auth_header(username, password)
                response = requests.get(f"{self.base_url}/transactions", headers=headers)
                
                if response.status_code == 200:
                    self.log_test(f"Valid Auth ({username})", True, 
                                f"Status: {response.status_code}")
                else:
                    self.log_test(f"Valid Auth ({username})", False,
                                f"Unexpected status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Valid Auth ({username})", False, f"Exception: {str(e)}")
        
        # Test invalid credentials
        invalid_creds = [
            ('admin', 'wrongpassword'),
            ('nonuser', 'password123'),
            ('', ''),
        ]
        
        for username, password in invalid_creds:
            try:
                headers = self.get_auth_header(username, password)
                response = requests.get(f"{self.base_url}/transactions", headers=headers)
                
                if response.status_code == 401:
                    self.log_test(f"Invalid Auth ({username})", True,
                                f"Correctly rejected with 401")
                else:
                    self.log_test(f"Invalid Auth ({username})", False,
                                f"Should be 401, got: {response.status_code}")
            except Exception as e:
                self.log_test(f"Invalid Auth ({username})", False, f"Exception: {str(e)}")
        
        # Test missing authentication
        try:
            response = requests.get(f"{self.base_url}/transactions")
            if response.status_code == 401:
                self.log_test("No Auth Header", True, "Correctly rejected with 401")
            else:
                self.log_test("No Auth Header", False,
                            f"Should be 401, got: {response.status_code}")
        except Exception as e:
            self.log_test("No Auth Header", False, f"Exception: {str(e)}")
    
    def test_get_endpoints(self):
        """Test GET endpoints."""
        print("\n=== Testing GET Endpoints ===")
        
        headers = self.get_auth_header('admin', 'password123')
        
        # Test GET all transactions
        try:
            response = requests.get(f"{self.base_url}/transactions", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if 'transactions' in data and 'total_count' in data:
                    self.log_test("GET All Transactions", True,
                                f"Retrieved {data['total_count']} transactions")
                else:
                    self.log_test("GET All Transactions", False, "Invalid response format")
            else:
                self.log_test("GET All Transactions", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("GET All Transactions", False, f"Exception: {str(e)}")
        
        # Test GET specific transaction (existing)
        try:
            response = requests.get(f"{self.base_url}/transactions/1", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if 'transaction' in data and data['transaction']['id'] == 1:
                    self.log_test("GET Specific Transaction (ID=1)", True,
                                "Successfully retrieved transaction")
                else:
                    self.log_test("GET Specific Transaction (ID=1)", False,
                                "Invalid response format")
            else:
                self.log_test("GET Specific Transaction (ID=1)", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("GET Specific Transaction (ID=1)", False, f"Exception: {str(e)}")
        
        # Test GET non-existent transaction
        try:
            response = requests.get(f"{self.base_url}/transactions/999", headers=headers)
            if response.status_code == 404:
                self.log_test("GET Non-existent Transaction", True,
                            "Correctly returned 404")
            else:
                self.log_test("GET Non-existent Transaction", False,
                            f"Should be 404, got: {response.status_code}")
        except Exception as e:
            self.log_test("GET Non-existent Transaction", False, f"Exception: {str(e)}")
        
        # Test GET with filters
        try:
            response = requests.get(f"{self.base_url}/transactions?status=COMPLETED", 
                                  headers=headers)
            if response.status_code == 200:
                data = response.json()
                completed_count = sum(1 for t in data['transactions'] 
                                    if t['status'] == 'COMPLETED')
                if completed_count == len(data['transactions']):
                    self.log_test("GET with Status Filter", True,
                                f"Filtered {completed_count} COMPLETED transactions")
                else:
                    self.log_test("GET with Status Filter", False,
                                "Filter not working correctly")
            else:
                self.log_test("GET with Status Filter", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("GET with Status Filter", False, f"Exception: {str(e)}")
    
    def test_post_endpoint(self):
        """Test POST endpoint (create transaction)."""
        print("\n=== Testing POST Endpoint ===")
        
        headers = self.get_auth_header('admin', 'password123')
        
        # Valid POST request
        new_transaction = {
            "type": "SEND_MONEY",
            "amount": 1500.75,
            "sender": "+1111111111",
            "receiver": "+2222222222",
            "reference": "TEST_TXN_001",
            "status": "PENDING"
        }
        
        try:
            response = requests.post(f"{self.base_url}/transactions", 
                                   headers=headers, 
                                   json=new_transaction)
            if response.status_code == 201:
                data = response.json()
                if 'transaction' in data and data['transaction']['reference'] == "TEST_TXN_001":
                    created_id = data['transaction']['id']
                    self.log_test("POST Create Transaction", True,
                                f"Created transaction with ID {created_id}")
                    
                    # Store ID for cleanup
                    self.created_transaction_id = created_id
                else:
                    self.log_test("POST Create Transaction", False,
                                "Invalid response format")
            else:
                self.log_test("POST Create Transaction", False,
                            f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("POST Create Transaction", False, f"Exception: {str(e)}")
        
        # Invalid POST request (missing required fields)
        invalid_transaction = {
            "type": "SEND_MONEY",
            "amount": 100.0
            # Missing sender, receiver, reference
        }
        
        try:
            response = requests.post(f"{self.base_url}/transactions", 
                                   headers=headers, 
                                   json=invalid_transaction)
            if response.status_code == 400:
                self.log_test("POST Invalid Data", True, "Correctly rejected with 400")
            else:
                self.log_test("POST Invalid Data", False,
                            f"Should be 400, got: {response.status_code}")
        except Exception as e:
            self.log_test("POST Invalid Data", False, f"Exception: {str(e)}")
    
    def test_put_endpoint(self):
        """Test PUT endpoint (update transaction)."""
        print("\n=== Testing PUT Endpoint ===")
        
        headers = self.get_auth_header('admin', 'password123')
        
        # Use the created transaction ID if available, otherwise use ID 1
        test_id = getattr(self, 'created_transaction_id', 1)
        
        # Valid PUT request
        update_data = {
            "status": "COMPLETED",
            "amount": 1600.00
        }
        
        try:
            response = requests.put(f"{self.base_url}/transactions/{test_id}", 
                                  headers=headers, 
                                  json=update_data)
            if response.status_code == 200:
                data = response.json()
                if ('transaction' in data and 
                    data['transaction']['status'] == 'COMPLETED' and
                    data['transaction']['amount'] == 1600.00):
                    self.log_test("PUT Update Transaction", True,
                                f"Updated transaction ID {test_id}")
                else:
                    self.log_test("PUT Update Transaction", False,
                                "Update not reflected in response")
            else:
                self.log_test("PUT Update Transaction", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("PUT Update Transaction", False, f"Exception: {str(e)}")
        
        # Invalid PUT request (non-existent ID)
        try:
            response = requests.put(f"{self.base_url}/transactions/999", 
                                  headers=headers, 
                                  json=update_data)
            if response.status_code == 404:
                self.log_test("PUT Non-existent Transaction", True,
                            "Correctly returned 404")
            else:
                self.log_test("PUT Non-existent Transaction", False,
                            f"Should be 404, got: {response.status_code}")
        except Exception as e:
            self.log_test("PUT Non-existent Transaction", False, f"Exception: {str(e)}")
    
    def test_delete_endpoint(self):
        """Test DELETE endpoint."""
        print("\n=== Testing DELETE Endpoint ===")
        
        headers = self.get_auth_header('admin', 'password123')
        
        # Use the created transaction ID if available
        if hasattr(self, 'created_transaction_id'):
            test_id = self.created_transaction_id
            
            try:
                response = requests.delete(f"{self.base_url}/transactions/{test_id}", 
                                         headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    if 'deleted_transaction' in data:
                        self.log_test("DELETE Transaction", True,
                                    f"Deleted transaction ID {test_id}")
                    else:
                        self.log_test("DELETE Transaction", False,
                                    "Invalid response format")
                else:
                    self.log_test("DELETE Transaction", False,
                                f"Status: {response.status_code}")
            except Exception as e:
                self.log_test("DELETE Transaction", False, f"Exception: {str(e)}")
        else:
            self.log_test("DELETE Transaction", False, "No transaction ID to delete")
        
        # Invalid DELETE request (non-existent ID)
        try:
            response = requests.delete(f"{self.base_url}/transactions/999", 
                                     headers=headers)
            if response.status_code == 404:
                self.log_test("DELETE Non-existent Transaction", True,
                            "Correctly returned 404")
            else:
                self.log_test("DELETE Non-existent Transaction", False,
                            f"Should be 404, got: {response.status_code}")
        except Exception as e:
            self.log_test("DELETE Non-existent Transaction", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all API tests."""
        print("Starting comprehensive API testing...")
        print(f"Testing API at: {self.base_url}")
        
        # Check if server is running
        try:
            response = requests.get(self.base_url, timeout=5)
        except requests.exceptions.ConnectionError:
            print(f"\n❌ ERROR: Cannot connect to API server at {self.base_url}")
            print("Make sure the server is running with: python api/server.py")
            return False
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            return False
        
        # Run test suites
        self.test_authentication()
        self.test_get_endpoints()
        self.test_post_endpoint()
        self.test_put_endpoint()
        self.test_delete_endpoint()
        
        # Print summary
        self.print_test_summary()
        return True
    
    def print_test_summary(self):
        """Print test results summary."""
        print("\n" + "="*60)
        print("TEST RESULTS SUMMARY")
        print("="*60)
        
        passed = sum(1 for result in self.test_results if result['status'] == 'PASS')
        failed = sum(1 for result in self.test_results if result['status'] == 'FAIL')
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "N/A")
        
        if failed > 0:
            print(f"\nFailed Tests:")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(f"  ❌ {result['test']}: {result['details']}")
        
        print("\nDetailed Results:")
        for result in self.test_results:
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            print(f"  {status_icon} {result['test']}")


def main():
    """Main function to run API tests."""
    tester = APITester()
    success = tester.run_all_tests()
    
    if success:
        print(f"\n🎉 Testing completed! Check the results above.")
    else:
        print(f"\n❌ Testing failed to run. Check server status.")


if __name__ == "__main__":
    main()