# -*- coding: utf-8 -*-
"""
This module provides functions to preprocess the search text.


"""
import string


custom_stop_words = {'project'}


class PreProcessor:
    
    __config = dict()

    def __init__(self, config=None):
        pass

    def preprocess(self, search_text, parameter=None):
        pass


class UMLSPreProcessor(PreProcessor):

    def preprocess(self, search_text, parameter=None):
        """Preprocess the search text before feed to subsequent steps.
        
        """
        # Simply remove the spaces 
        
        return search_text.strip()
