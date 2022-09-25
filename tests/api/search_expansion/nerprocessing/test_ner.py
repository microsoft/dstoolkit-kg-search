import unittest
import os
from api.search_expansion.nerprocessing.ner import AircraftNer
from api.search_expansion.preprocessing.preprocessor import AircraftPreProcessor
from dotenv import load_dotenv
import uuid
import time

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

class DemoNERTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Method called to prepare the test fixture.
        """

        load_dotenv() 
        
        config = {}
        config['endpoint'] = os.environ.get('NER_ENDPOINT', None)
        config['token'] = os.environ.get('NER_BEAR_TOKEN', None)
        
        cls.ner = AircraftNer(config)

    @classmethod
    def tearDownClass(cls):
        """Method called immediately after the test method has been called 
        and the result recorded.
        """
        pass

    def test_extract_entities(self):
        """Test extracting entities.
        """
        search_text = 'treatment of stable condition keratoconus'

        preprocessed_text = AircraftPreProcessor().preprocess(search_text)

        ner_result = DemoNERTest.ner.extract_entities(preprocessed_text, search_text)
        
        assert ner_result == {
                                "tags": [
                                    {
                                        "category": "Disease",
                                        "class": "Disease",
                                        "length": 28,
                                        "offset": 13,
                                        "text": "stable condition keratoconus"
                                    }
                                ]
                            }

        search_text = 'treatment of stable condition keratoconus and acute hydrops keratoconus'

        preprocessed_text = AircraftPreProcessor().preprocess(search_text)

        ner_result = DemoNERTest.ner.extract_entities(preprocessed_text, search_text)
        
        assert ner_result == {
                                "tags": [
                                    {
                                        "category": "Disease",
                                        "class": "Disease",
                                        "length": 28,
                                        "offset": 13,
                                        "text": "stable condition keratoconus"
                                    },
                                    {
                                        "category": "Disease",
                                        "class": "Disease",
                                        "length": 25,
                                        "offset": 46,
                                        "text": "acute hydrops keratoconus"
                                    }
                                ]
                            }

        search_text = 'treatment of keratoconus'
        
        preprocessed_text = AircraftPreProcessor().preprocess(search_text)

        ner_result = DemoNERTest.ner.extract_entities(preprocessed_text, search_text)
        
        assert ner_result == {
                                "tags": [
                                    {
                                        "category": "Disease",
                                        "class": "Disease",
                                        "length": 11,
                                        "offset": 13,
                                        "text": "keratoconus"
                                    }
                                ]
                            }