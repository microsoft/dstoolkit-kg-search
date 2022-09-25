import unittest
import os
from api.search_expansion.kg.knowledge_extractor import AircraftKnowledgeExtractor
from dotenv import load_dotenv
import uuid
import time

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

class KnowledgeExtractorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Method called to prepare the test fixture.
        """

        load_dotenv() 
        
        config = {}
        config['server'] = os.environ['COSMOS_DB_SERVER']
        config['db'] = os.environ['COSMOS_DB_DATABASE']
        config['graph'] = os.environ['COSMOS_DB_GRAPH']
        config['password'] = os.environ['COSMOS_DB_PASSWORD']
        
        cls.extractor = AircraftKnowledgeExtractor(config)

    @classmethod
    def tearDownClass(cls):
        """Method called immediately after the test method has been called 
        and the result recorded.
        """
        pass

    # def test_extract_hyponyms_disease(self):
    #     """Test extracting hyponyms disease
    #     """
  
    #     disease_name = 'keratoconus'

    #     similar_diseases = KnowledgeExtractorTest.extractor.extract_hyponyms_disease(disease_name)
        
    #     assert len(similar_diseases) > 0

    # def test_extract_hypernyms_disease(self):
    #     """Test extracting hypernyms disease
    #     """
  
    #     disease_name = 'keratoconus'

    #     similar_diseases = KnowledgeExtractorTest.extractor.extract_hypernyms_disease(disease_name)
        
    #     assert len(similar_diseases) > 0

    # def test_extract_similar_disease(self):
    #     """Test extracting similar equipments.
    #     """
    #     disease_name = 'keratoconus'
    #     similar_diseases = KnowledgeExtractorTest.extractor.extract_similar_disease(disease_name)
        
    #     assert len(similar_diseases) > 0


    def test_extract_relevant_entities(self):
        """Test the extract relevant entities function.
        """

        ner_result = {
                    "tags": [
                        {
                            "category": "Disease",
                            "class": "Disease",
                            "length": 11,
                            "offset": 0,
                            "text": "keratoconus"
                        },
                    ]
                }

        relevant_entities = KnowledgeExtractorTest.extractor.extract_relevant_entities(ner_result)

        assert len(relevant_entities) == 2