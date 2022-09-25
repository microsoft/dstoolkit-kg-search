# -*- coding: utf-8 -*-
"""
This module provides functions extract relevant entity from Knowledge Graph.


"""
from api.search_expansion.kg.graph_db import CosmosDBClient
import logging
import api.search_expansion.util as util

logger = logging.getLogger(__name__)

class KnowledgeExtractor:
    
    __config = dict()

    def __init__(self, config):
        pass

    def extract_relevant_entities(self, ner_result):
        """Extract relevant entities to the input entities.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            ner_result: The ner_result in dictonary.

        Returns:
            The set of relevant entities in dictionary.

        """
        pass

class AircraftKnowledgeExtractor(KnowledgeExtractor):
    
    def __init__(self, config):
        self.config = config

    def extract_relevant_bulletin(self, aircraft_rego, aircraft_system_name, query_api=util.QueryAPI.gremlin):
        """Extract the bulletin.
        
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            aircraft_rego: the id of the aircraft.
            aircraft_system_name: the sub-system in the aircraft.
            query_api: the API used for Cosmos DB. It could be Gremlin or SQL.

        Returns:
            The set of relevant entities in dictionary.

        """
        # query = f"g.V().haslabel('disease').has('name', '{disease_name}').in('is subclass of').values('name')"

        # logger.debug(f"Gremlin Query: {query}")
    
        # results = self.client.execute_traversal(query)

        # similar_diseases = []

        # # The result is returned in batch
        # for result in results:
        #     similar_diseases.extend(result)

        # # Remove duplication if any
        # similar_diseases = list(dict.fromkeys(similar_diseases))

        relevant_bulletin = ['communique 2015-05']

        return relevant_bulletin

    def extract_relevant_maintenance_log(self, aircraft_rego, aircraft_system_name, query_api=util.QueryAPI.gremlin):
        """Extract the maintenance log.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            aircraft_rego: the id of the aircraft.
            aircraft_system_name: the sub-system in the aircraft.
            query_api: the API used for Cosmos DB. It could be Gremlin or SQL.

        Returns:
            The set of relevant entities in dictionary.

        """
        # query = f"g.V().haslabel('Aircraft').has('rego', '{aircraft_rego}').out('is subclass of').values('name')"

        # logger.debug(f"Gremlin Query: {query}")
    
        # results = self.client.execute_traversal(query)

        # similar_diseases = []

        # # The result is returned in batch
        # for result in results:
        #     similar_diseases.extend(result)

        # # Remove duplication if any
        # similar_diseases = list(dict.fromkeys(similar_diseases))

        relavant_maintenance_log = ['MLOG_298601']

        return relavant_maintenance_log

    def extract_relevant_log(self, aircraft_rego, aircraft_system_name, query_api=util.QueryAPI.gremlin):
        """Extract relevant log for the corresponding aircraft and its sub system.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            aircraft_rego: the id of the aircraft.
            aircraft_system_name: the sub-system in the aircraft.
            query_api: the API used for Cosmos DB. It could be Gremlin or SQL.

        Returns:
            The set of relevant entities in dictionary.

        """
        
        maintenance_log = self.extract_relevant_maintenance_log(aircraft_rego, aircraft_system_name)
        bulletin = self.extract_relevant_bulletin(aircraft_rego, aircraft_system_name)
        
        return [maintenance_log, bulletin]


    def extract_relevant_entities(self, ner_result):
        """Extract similar disease from KG.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            ner_result: The ner_result in dictonary.

        Returns:
            The set of relevant entities in dictionary.

        """
        # TODO CosmosDB will close the connection automatically after being idle for 1 hour. 
        # So we just simply create the connection all the time. 
        # A better workaround is to implement some keep-alive logic.

        self.client = CosmosDBClient(self.config)
        
        aircraft_instance, aircraft_rego, aircraft_system_instance, aircraft_system_name = util.count_entities(ner_result)

        relevant_entities = {}

        if aircraft_instance > 1 or aircraft_system_instance > 1:
            logger.warn("Only one aircraft can be specified in the query. "
                        "Stop retrieving relevant entities.")
            return None  

        elif aircraft_rego is not None and aircraft_system_name is not None:
            relevant_logs = self.extract_relevant_log(aircraft_rego, aircraft_system_name)
            if relevant_logs is not None:
                relevant_entities = relevant_logs
            else:
                return None

        else:
            return None
        
        return relevant_entities