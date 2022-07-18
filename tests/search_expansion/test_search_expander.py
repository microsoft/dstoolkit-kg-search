import unittest
import os
import time
from search_expansion.search_expander import UMLSSearchExpander

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

class SearchExpanderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Method called to prepare the test fixture.
        """
        
        cls.search_expander = UMLSSearchExpander()

    @classmethod
    def tearDownClass(cls):
        """Method called after all the test method have been called 
        and the result recorded.
        """
        pass

    def test_search(self):
        """Test the search function.
        """

        search_list = ["keratoconus treatment"]

        for query in search_list:
            code, result = SearchExpanderTest.search_expander.search(query)
            
            print(f"Result for query: {query}")
            # print(result)
            for doc in result['value']:
                print(doc)

    def test_expand(self):
        """Test the expand function.
        """
        # Test no match on plant
        search_text = "keratoconus treatment"

        start_time = time.time()
        result = SearchExpanderTest.search_expander.expand(search_text)
        print(f"Execution time: {time.time() - start_time} second")

        print(f"Result for query: {search_text}")
        # print(result)
        for doc in result['value']:
            print(doc)

    