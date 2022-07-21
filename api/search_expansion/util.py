# -*- coding: utf-8 -*-
"""
This module provide some utility function/class that used by other modules.


"""
from enum import Enum

class QueryAPI:
    gremlin = 'Gremlin'
    sql = 'SQL'


def count_entities(ner_result):
    """ Count the numebr of entities indentified by the NER service.
    
    """

    disease_class = 'Disease'
    disease_instance = 0
    disease_name = None

    if ner_result is None:
        return disease_instance, disease_name

    for entity in ner_result['tags']:
        if entity['class'] == disease_class:
            disease_instance += 1
            disease_name = entity['text']

    return disease_instance, disease_name