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

    aircraft_class = 'Aircraft'
    aircraft_instance = 0
    aircraft_rego = None

    aircraft_system_class = 'Aircraft_System'
    aircraft_system_instance = 0
    aircraft_system_name = None    

    if ner_result is None:
        return aircraft_instance, aircraft_rego, aircraft_system_instance, aircraft_system_name

    for entity in ner_result['tags']:
        if entity['class'] == aircraft_class:
            aircraft_instance += 1
            aircraft_rego = entity['text']

        if entity['class'] == aircraft_system_class:
            aircraft_system_instance += 1
            aircraft_system_name = entity['text']

    return aircraft_instance, aircraft_rego, aircraft_system_instance, aircraft_system_name