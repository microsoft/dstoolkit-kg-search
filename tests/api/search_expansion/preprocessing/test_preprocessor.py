import unittest
import os
import time
from api.search_expansion.preprocessing.preprocessor import AircraftPreProcessor

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

class PreprocessorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Method called to prepare the test fixture.
        """
        
        cls.preprocessor = AircraftPreProcessor()

    @classmethod
    def tearDownClass(cls):
        """Method called after all the test method have been called 
        and the result recorded.
        """
        pass

    def test_preprocess(self):
        """Test the preprocess function.
        """
        search_text = " keratoconus "
        
        preprocessed_text = PreprocessorTest.preprocessor.preprocess(search_text)
        assert preprocessed_text == "keratoconus"