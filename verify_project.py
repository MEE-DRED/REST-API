"""
Quick verification script to test the project components
"""

import os
import sys

def test_xml_parsing():
    """Test XML parsing functionality"""
    print("Testing XML parsing...")
    
    # Add the dsa directory to Python path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'dsa'))
    
    try:
        from xml_parser import TransactionParser
        
        parser = TransactionParser('data/modified_sms_v2.xml')
        transactions = parser.parse_xml_to_json()
        
        print(f"Successfully parsed {len(transactions)} transactions")
        
        if len(transactions) > 0:
            first_transaction = transactions[0]
            print(f"Sample transaction: ID={first_transaction['id']}, Type={first_transaction['type']}, Amount=${first_transaction['amount']}")
            
        return True
        
    except Exception as e:
        print(f"XML parsing failed: {e}")
        return False

def test_search_algorithms():
    """Test search algorithm performance"""
    print("\nTesting search algorithms...")
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'dsa'))
        from xml_parser import TransactionParser, SearchAlgorithms
        
        # Load data
        parser = TransactionParser('data/modified_sms_v2.xml')
        transactions = parser.parse_xml_to_json()
        
        # Initialize search algorithms
        search_algo = SearchAlgorithms(transactions, parser.transactions_dict)
        
        # Test searches
        test_ids = [1, 5, 10, 15, 999]  # Mix of existing and non-existing IDs
        
        for test_id in test_ids:
            linear_result = search_algo.linear_search(test_id)
            dict_result = search_algo.dictionary_lookup(test_id)
            
            # Verify both methods return the same result
            if linear_result == dict_result:
                status = "Found" if linear_result else "Not Found"
                print(f"ID {test_id}: {status} (both methods agree)")
            else:
                print(f"ID {test_id}: Methods disagree!")
                return False
        
        # Quick performance test
        existing_ids = [t['id'] for t in transactions[:5]]
        results = search_algo.compare_search_efficiency(existing_ids, iterations=10)
        
        print(f"Performance test completed")
        print(f"   Dictionary lookup is {results['speedup_factor']:.1f}x faster")
        
        return True
        
    except Exception as e:
        print(f"Search algorithm test failed: {e}")
        return False

def test_server_import():
    """Test that the server module can be imported"""
    print("\nTesting server module...")
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))
        import server
        
        print("Server module imported successfully")
        print(f"Found {len(server.TransactionAPIHandler.VALID_CREDENTIALS)} valid credential sets")
        
        return True
        
    except Exception as e:
        print(f"Server import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("SMS TRANSACTIONS API - QUICK VERIFICATION")
    print("=" * 60)
    
    tests = [
        test_xml_parsing,
        test_search_algorithms,
        test_server_import
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("VERIFICATION RESULTS")
    print("=" * 60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/(passed+failed)*100):.1f}%" if (passed+failed) > 0 else "N/A")
    
    if failed == 0:
        print("\nAll components verified successfully!")
        print("\nNext steps:")
        print("1. Start the API server: python api/server.py")
        print("2. Test the API: python api/test_api.py")
        print("3. Or use the curl script: test_api_curl.bat")
    else:
        print(f"\n{failed} component(s) need attention.")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()
