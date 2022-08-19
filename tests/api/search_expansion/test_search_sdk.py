import unittest
import os
import json
import time
from dotenv import load_dotenv
from api.search_expansion.search_sdk import SearchSDK

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

load_dotenv() 

class SearchSDKTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Method called to prepare the test fixture.
        """
        config = {}
        config['endpoint'] = os.environ['ACS_ENDPOINT']
        config['api_key'] = os.environ['ACS_API_KEY']
        config['index_name'] = os.environ['ACS_INDEX_NAME']
        config['api_version'] = os.environ['ACS_API_VERSION']
        cls.search_client = SearchSDK(config)

    @classmethod
    def tearDownClass(cls):
        """Method called after all the test method have been called 
        and the result recorded.
        """
        pass

    def test_advanced_search(self):
        """Test the search function.
        """

        # return 
        search_list = ["keratoconus treatment"]

        for query in search_list:
            payload = {
                "search": query,
                "queryType": "simple",
                "queryLanguage": "en-us",
                "select": "title",
                "top": 10,
                "count": True
            }
            
            code, result = SearchSDKTest.search_client.advanced_search(payload)
            print(f"Code: {code}")
            
            count = 0
            # print(result)
            print(f"Result for query: {query}")
            for doc in result['value']:
                print(doc)