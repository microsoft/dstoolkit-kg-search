import unittest
import os
import json
import time
from search_expansion.util import *

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


class UtilTest(unittest.TestCase):


    def test_count_entities(self):
        """Test the search function.
        """

        ner_result = {
            "tags": [
                {
                    "category": "Disease",
                    "class": "Disease",
                    "length": 11,
                    "offset": 0,
                    "text": "keratoconus"
                }
            ]
        }

        disease_instance, disease_name = count_entities(ner_result)

        assert disease_instance == 1
        assert disease_name == 'keratoconus'
