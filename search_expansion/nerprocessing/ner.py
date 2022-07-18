# -*- coding: utf-8 -*-
"""
This module provides the NER function.

"""

import requests
import logging
import json
import re

logger = logging.getLogger(__name__)

class Ner:
    
    __config = dict()

    def __init__(self, config):
        pass

    def extract_entities(self, processed_text, original_text):
        """Entry function to perform entities recognition.

        Args:
            processed_text: the text that the ner will actually work on
            original_text: the orginal search text

        Returns:
            The entiry recognition result in dict.

        """
        return None


class UMLSNer(Ner):
    
    def __init__(self, config):
        pass

    def extract_entities(self, processed_text, original_text=None):
        """Entry function to perform entities recognition. Language studio
        model will be used.

        Args:
            processed_text: the text that the ner will actually work on
            original_text: the orginal search text

        Returns:
            The entity recognition result in dict. 
        """

        if original_text is None:
            original_text = processed_text

        ner_result = None
        
        keratoconus_subclass1 = 'stable condition keratoconus'
        match_1 = re.search(keratoconus_subclass1, processed_text)

        tags = []
        if match_1 is not None:
            keratoconus_subclass1_tag = {
                        "category": "Disease",
                        "class": "Disease",
                        "length": len(keratoconus_subclass1),
                        "offset": match_1.start(),
                        "text": keratoconus_subclass1
                    }
            tags.append(keratoconus_subclass1_tag)

        keratoconus_subclass2 = 'acute hydrops keratoconus'
        match_2 = re.search(keratoconus_subclass2, processed_text)

        if match_2 is not None:
            keratoconus_subclass2_tag = {
                        "category": "Disease",
                        "class": "Disease",
                        "length": len(keratoconus_subclass2),
                        "offset": match_2.start(),
                        "text": keratoconus_subclass2
                    }
            tags.append(keratoconus_subclass2_tag)
            
        if match_1 is None and match_2 is None:
            keratoconus = 'keratoconus'
            match = re.search(keratoconus, processed_text)

            if match is not None:
                keratoconus_tag = {
                            "category": "Disease",
                            "class": "Disease",
                            "length": len(keratoconus),
                            "offset": match.start(),
                            "text": keratoconus
                        }
                tags.append(keratoconus_tag)

        if len(tags) > 0:
            ner_result = {
                "tags": tags
            }

        return ner_result