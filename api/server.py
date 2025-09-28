"""
REST API Server for SMS Transactions
Implements CRUD operations with Basic Authentication using Python's http.server
"""

import http.server
import socketserver
import json
import base64
import urllib.parse
from typing import Dict, List, Optional, Any
import sys
import os

# Add the dsa directory to Python path to import xml_parser
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dsa'))
from xml_parser import TransactionParser


class TransactionAPIHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for transaction API endpoints."""
    
    # In-memory storage (in production, use a proper database)
    transactions_list = []
    transactions_dict = {}
    next_id = 1
    
    # Basic Auth credentials (in production, use proper user management)
    VALID_CREDENTIALS = {
        'admin': 'password123',
        'user': 'user123',
        'demo': 'demo123'
    }
    
    @classmethod
    def load_data(cls):
        """Load transaction data from XML file."""
        try:
            parser = TransactionParser('data/modified_sms_v2.xml')
            cls.transactions_list = parser.parse_xml_to_json()
            cls.transactions_dict = {t['id']: t for t in cls.transactions_list}
            if cls.transactions_list:
                cls.next_id = max(t['id'] for t in cls.transactions_list) + 1
            print(f"Loaded {len(cls.transactions_list)} transactions from XML")
        except Exception as e:
            print(f"Error loading data: {e}")
            cls.transactions_list = []
            cls.transactions_dict = {}
    
    def authenticate(self) -> bool:
        """
        Verify Basic Authentication credentials.
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        auth_header = self.headers.get('Authorization')
        if not auth_header:
            return False
        
        try:
            # Extract credentials from "Basic <base64-encoded-credentials>"
            auth_type, auth_string = auth_header.split(' ', 1)
            if auth_type.lower() != 'basic':
                return False
            
            # Decode base64 credentials
            credentials = base64.b64decode(auth_string).decode('utf-8')
            username, password = credentials.split(':', 1)
            
            # Verify credentials
            return self.VALID_CREDENTIALS.get(username) == password
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def send_json_response(self, data: Any, status_code: int = 200):
        """Send JSON response with appropriate headers."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        response = json.dumps(data, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def send_error_response(self, message: str, status_code: int = 400):
        """Send error response."""
        error_data = {
            'error': message,
            'status_code': status_code
        }
        self.send_json_response(error_data, status_code)
    
    def send_unauthorized(self):
        """Send 401 Unauthorized response."""
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="SMS Transaction API"')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        error_response = {
            'error': 'Unauthorized - Invalid or missing credentials',
            'status_code': 401,
            'message': 'Please provide valid Basic Authentication credentials'
        }
        self.wfile.write(json.dumps(error_response, indent=2).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle preflight requests for CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        if not self.authenticate():
            self.send_unauthorized()
            return
        
        # Parse URL and query parameters
        parsed_url = urllib.parse.urlparse(self.path)
        path_parts = [p for p in parsed_url.path.split('/') if p]
        
        if not path_parts or path_parts[0] != 'transactions':
            self.send_error_response('Invalid endpoint', 404)
            return
        
        # GET /transactions - List all transactions
        if len(path_parts) == 1:
            query_params = urllib.parse.parse_qs(parsed_url.query)
            
            # Optional filtering by status, type, etc.
            filtered_transactions = self.transactions_list.copy()
            
            if 'status' in query_params:
                status_filter = query_params['status'][0].upper()
                filtered_transactions = [t for t in filtered_transactions 
                                       if t['status'] == status_filter]
            
            if 'type' in query_params:
                type_filter = query_params['type'][0].upper()
                filtered_transactions = [t for t in filtered_transactions 
                                       if t['type'] == type_filter]
            
            response_data = {
                'transactions': filtered_transactions,
                'total_count': len(filtered_transactions),
                'message': 'Transactions retrieved successfully'
            }
            self.send_json_response(response_data)
            return
        
        # GET /transactions/{id} - Get specific transaction
        if len(path_parts) == 2:
            try:
                transaction_id = int(path_parts[1])
                transaction = self.transactions_dict.get(transaction_id)
                
                if transaction:
                    response_data = {
                        'transaction': transaction,
                        'message': 'Transaction found'
                    }
                    self.send_json_response(response_data)
                else:
                    self.send_error_response('Transaction not found', 404)
                return
                
            except ValueError:
                self.send_error_response('Invalid transaction ID format', 400)
                return
        
        self.send_error_response('Invalid endpoint', 404)
    
    def do_POST(self):
        """Handle POST requests - Create new transaction."""
        if not self.authenticate():
            self.send_unauthorized()
            return
        
        # Parse URL
        parsed_url = urllib.parse.urlparse(self.path)
        path_parts = [p for p in parsed_url.path.split('/') if p]
        
        if len(path_parts) != 1 or path_parts[0] != 'transactions':
            self.send_error_response('Invalid endpoint for POST', 404)
            return
        
        # Read and parse request body
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            new_transaction_data = json.loads(post_data)
            
            # Validate required fields
            required_fields = ['type', 'amount', 'sender', 'receiver', 'reference']
            for field in required_fields:
                if field not in new_transaction_data:
                    self.send_error_response(f'Missing required field: {field}', 400)
                    return
            
            # Create new transaction with auto-generated ID and timestamp
            from datetime import datetime
            
            new_transaction = {
                'id': self.next_id,
                'type': new_transaction_data['type'].upper(),
                'amount': float(new_transaction_data['amount']),
                'sender': new_transaction_data['sender'],
                'receiver': new_transaction_data['receiver'],
                'timestamp': new_transaction_data.get('timestamp', 
                                                    datetime.utcnow().isoformat() + 'Z'),
                'reference': new_transaction_data['reference'],
                'status': new_transaction_data.get('status', 'PENDING').upper()
            }
            
            # Add to storage
            self.transactions_list.append(new_transaction)
            self.transactions_dict[new_transaction['id']] = new_transaction
            self.next_id += 1
            
            response_data = {
                'message': 'Transaction created successfully',
                'transaction': new_transaction
            }
            self.send_json_response(response_data, 201)
            
        except json.JSONDecodeError:
            self.send_error_response('Invalid JSON data', 400)
        except ValueError as e:
            self.send_error_response(f'Invalid data format: {str(e)}', 400)
        except Exception as e:
            self.send_error_response(f'Server error: {str(e)}', 500)
    
    def do_PUT(self):
        """Handle PUT requests - Update existing transaction."""
        if not self.authenticate():
            self.send_unauthorized()
            return
        
        # Parse URL
        parsed_url = urllib.parse.urlparse(self.path)
        path_parts = [p for p in parsed_url.path.split('/') if p]
        
        if len(path_parts) != 2 or path_parts[0] != 'transactions':
            self.send_error_response('Invalid endpoint for PUT', 404)
            return
        
        try:
            transaction_id = int(path_parts[1])
            
            if transaction_id not in self.transactions_dict:
                self.send_error_response('Transaction not found', 404)
                return
            
            # Read and parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            put_data = self.rfile.read(content_length).decode('utf-8')
            update_data = json.loads(put_data)
            
            # Update transaction
            transaction = self.transactions_dict[transaction_id]
            
            # Update allowed fields
            updatable_fields = ['type', 'amount', 'sender', 'receiver', 'status', 'reference']
            for field in updatable_fields:
                if field in update_data:
                    if field in ['type', 'status']:
                        transaction[field] = update_data[field].upper()
                    elif field == 'amount':
                        transaction[field] = float(update_data[field])
                    else:
                        transaction[field] = update_data[field]
            
            # Update in list as well
            for i, t in enumerate(self.transactions_list):
                if t['id'] == transaction_id:
                    self.transactions_list[i] = transaction
                    break
            
            response_data = {
                'message': 'Transaction updated successfully',
                'transaction': transaction
            }
            self.send_json_response(response_data)
            
        except ValueError as e:
            self.send_error_response(f'Invalid transaction ID or data: {str(e)}', 400)
        except json.JSONDecodeError:
            self.send_error_response('Invalid JSON data', 400)
        except Exception as e:
            self.send_error_response(f'Server error: {str(e)}', 500)
    
    def do_DELETE(self):
        """Handle DELETE requests - Delete transaction."""
        if not self.authenticate():
            self.send_unauthorized()
            return
        
        # Parse URL
        parsed_url = urllib.parse.urlparse(self.path)
        path_parts = [p for p in parsed_url.path.split('/') if p]
        
        if len(path_parts) != 2 or path_parts[0] != 'transactions':
            self.send_error_response('Invalid endpoint for DELETE', 404)
            return
        
        try:
            transaction_id = int(path_parts[1])
            
            if transaction_id not in self.transactions_dict:
                self.send_error_response('Transaction not found', 404)
                return
            
            # Remove from both storage structures
            deleted_transaction = self.transactions_dict.pop(transaction_id)
            self.transactions_list = [t for t in self.transactions_list 
                                    if t['id'] != transaction_id]
            
            response_data = {
                'message': 'Transaction deleted successfully',
                'deleted_transaction': deleted_transaction
            }
            self.send_json_response(response_data)
            
        except ValueError:
            self.send_error_response('Invalid transaction ID format', 400)
        except Exception as e:
            self.send_error_response(f'Server error: {str(e)}', 500)


def start_server(port: int = 8000):
    """Start the REST API server."""
    print("Starting SMS Transaction REST API Server...")
    
    # Load transaction data
    TransactionAPIHandler.load_data()
    
    # Create server
    with socketserver.TCPServer(("", port), TransactionAPIHandler) as httpd:
        print(f"Server running on http://localhost:{port}")
        print(f"Loaded {len(TransactionAPIHandler.transactions_list)} transactions")
        print("\nValid credentials:")
        for username, password in TransactionAPIHandler.VALID_CREDENTIALS.items():
            print(f"  Username: {username}, Password: {password}")
        
        print(f"\nAvailable endpoints:")
        print(f"  GET    /transactions       - List all transactions")
        print(f"  GET    /transactions/{{id}}  - Get specific transaction")
        print(f"  POST   /transactions       - Create new transaction")
        print(f"  PUT    /transactions/{{id}}  - Update transaction")
        print(f"  DELETE /transactions/{{id}}  - Delete transaction")
        print(f"\nPress Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")


if __name__ == "__main__":
    start_server()