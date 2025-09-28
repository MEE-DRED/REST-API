"""
XML Parser and Data Structures Module
This module handles XML parsing and implements different search algorithms for comparison.
"""

import xml.etree.ElementTree as ET
import json
import time
from typing import List, Dict, Optional, Any


class TransactionParser:
    """Handles parsing of SMS transaction XML data."""
    
    def __init__(self, xml_file_path: str):
        self.xml_file_path = xml_file_path
        self.transactions_list = []
        self.transactions_dict = {}
    
    def parse_xml_to_json(self) -> List[Dict[str, Any]]:
        """
        Parse XML file and convert to list of dictionaries (JSON format).
        
        Returns:
            List[Dict]: List of transaction dictionaries
        """
        try:
            tree = ET.parse(self.xml_file_path)
            root = tree.getroot()
            
            transactions = []
            
            for transaction_elem in root.findall('transaction'):
                transaction = {
                    'id': int(transaction_elem.get('id')),
                    'type': transaction_elem.find('type').text,
                    'amount': float(transaction_elem.find('amount').text),
                    'sender': transaction_elem.find('sender').text,
                    'receiver': transaction_elem.find('receiver').text,
                    'timestamp': transaction_elem.find('timestamp').text,
                    'reference': transaction_elem.find('reference').text,
                    'status': transaction_elem.find('status').text
                }
                transactions.append(transaction)
            
            self.transactions_list = transactions
            self._build_dictionary()
            
            return transactions
            
        except Exception as e:
            print(f"Error parsing XML: {e}")
            return []
    
    def _build_dictionary(self):
        """Build dictionary for O(1) lookup by transaction ID."""
        self.transactions_dict = {transaction['id']: transaction 
                                for transaction in self.transactions_list}
    
    def save_to_json_file(self, output_file: str):
        """Save parsed transactions to JSON file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.transactions_list, f, indent=2, ensure_ascii=False)
            print(f"Transactions saved to {output_file}")
        except Exception as e:
            print(f"Error saving JSON: {e}")


class SearchAlgorithms:
    """Implements and compares different search algorithms."""
    
    def __init__(self, transactions_list: List[Dict], transactions_dict: Dict):
        self.transactions_list = transactions_list
        self.transactions_dict = transactions_dict
    
    def linear_search(self, transaction_id: int) -> Optional[Dict[str, Any]]:
        """
        Linear search through the list to find transaction by ID.
        Time Complexity: O(n)
        
        Args:
            transaction_id (int): ID of the transaction to find
            
        Returns:
            Optional[Dict]: Transaction if found, None otherwise
        """
        for transaction in self.transactions_list:
            if transaction['id'] == transaction_id:
                return transaction
        return None
    
    def dictionary_lookup(self, transaction_id: int) -> Optional[Dict[str, Any]]:
        """
        Dictionary lookup to find transaction by ID.
        Time Complexity: O(1) average case
        
        Args:
            transaction_id (int): ID of the transaction to find
            
        Returns:
            Optional[Dict]: Transaction if found, None otherwise
        """
        return self.transactions_dict.get(transaction_id)
    
    def compare_search_efficiency(self, search_ids: List[int], iterations: int = 1000) -> Dict[str, float]:
        """
        Compare efficiency of linear search vs dictionary lookup.
        
        Args:
            search_ids (List[int]): List of IDs to search for
            iterations (int): Number of iterations for timing
            
        Returns:
            Dict[str, float]: Timing results for both methods
        """
        # Time linear search
        start_time = time.time()
        for _ in range(iterations):
            for search_id in search_ids:
                self.linear_search(search_id)
        linear_time = time.time() - start_time
        
        # Time dictionary lookup
        start_time = time.time()
        for _ in range(iterations):
            for search_id in search_ids:
                self.dictionary_lookup(search_id)
        dict_time = time.time() - start_time
        
        return {
            'linear_search_time': linear_time,
            'dictionary_lookup_time': dict_time,
            'speedup_factor': linear_time / dict_time if dict_time > 0 else float('inf'),
            'iterations': iterations,
            'search_operations': len(search_ids) * iterations
        }


def demonstrate_dsa_comparison():
    """Demonstrate and compare search algorithms."""
    print("=== Data Structures & Algorithms Comparison ===\n")
    
    # Initialize parser
    parser = TransactionParser('data/modified_sms_v2.xml')
    transactions = parser.parse_xml_to_json()
    
    if not transactions:
        print("No transactions found or error in parsing.")
        return
    
    print(f"Loaded {len(transactions)} transactions.")
    
    # Initialize search algorithms
    search_algo = SearchAlgorithms(transactions, parser.transactions_dict)
    
    # Test search methods with sample IDs
    test_ids = [1, 5, 10, 15, 20, 25, 30]  # Some IDs may not exist
    
    print("\n--- Individual Search Tests ---")
    for test_id in test_ids[:5]:  # Test first 5 IDs
        print(f"\nSearching for Transaction ID: {test_id}")
        
        # Linear search
        start_time = time.time()
        linear_result = search_algo.linear_search(test_id)
        linear_time = time.time() - start_time
        
        # Dictionary lookup
        start_time = time.time()
        dict_result = search_algo.dictionary_lookup(test_id)
        dict_time = time.time() - start_time
        
        print(f"Linear Search: {'Found' if linear_result else 'Not Found'} (Time: {linear_time:.8f}s)")
        print(f"Dict Lookup: {'Found' if dict_result else 'Not Found'} (Time: {dict_time:.8f}s)")
        
        if linear_result:
            print(f"Transaction: {linear_result['type']} - ${linear_result['amount']}")
    
    # Performance comparison
    print("\n--- Performance Comparison ---")
    existing_ids = [t['id'] for t in transactions[:20]]  # Use first 20 existing IDs
    
    results = search_algo.compare_search_efficiency(existing_ids, iterations=100)
    
    print(f"Linear Search Time: {results['linear_search_time']:.6f} seconds")
    print(f"Dictionary Lookup Time: {results['dictionary_lookup_time']:.6f} seconds")
    print(f"Speedup Factor: {results['speedup_factor']:.2f}x")
    print(f"Operations Performed: {results['search_operations']}")
    
    print(f"\n--- Analysis ---")
    print(f"Dictionary lookup is {results['speedup_factor']:.1f}x faster than linear search.")
    print("Why dictionary lookup is faster:")
    print("- Linear Search: O(n) - must check each element sequentially")
    print("- Dictionary Lookup: O(1) average - direct hash-based access")
    print("\nOther efficient data structures:")
    print("- Binary Search Tree: O(log n) search time")
    print("- Hash Set: O(1) for existence checks")
    print("- B-Tree: O(log n) but efficient for disk storage")
    
    return results


if __name__ == "__main__":
    demonstrate_dsa_comparison()