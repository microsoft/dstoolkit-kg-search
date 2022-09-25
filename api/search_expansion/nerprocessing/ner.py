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


class AircraftNer(Ner):
    
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
        
        aircraft_class = 'VH-ACX'
        match_aircraft = re.search(aircraft_class, processed_text)

        tags = []
        if match_aircraft is not None:
            aircraft_tag = {
                        "category": "Aircraft",
                        "class": "Aircraft",
                        "length": len(aircraft_class),
                        "offset": match_aircraft.start(),
                        "text": aircraft_class
                    }
            tags.append(aircraft_tag)

        aircraft_system_class = 'air conditioning'
        match_aircraft_system = re.search(aircraft_system_class, processed_text)

        if match_aircraft_system is not None:
            aircraft_system_tag = {
                        "category": "Aircraft_System",
                        "class": "Aircraft_System",
                        "length": len(aircraft_system_class),
                        "offset": match_aircraft_system.start(),
                        "text": aircraft_system_class
                    }
            tags.append(aircraft_system_tag)
            

        if len(tags) > 0:
            ner_result = {
                "tags": tags
            }

        return ner_result