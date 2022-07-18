# -*- coding: utf-8 -*-
"""
This module provides functions extract relevant entity from Knowledge Graph.


"""
from search_expansion.kg.graph_db import CosmosDBClient
import logging
import search_expansion.util as util

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


class UMLSKnowledgeExtractor(KnowledgeExtractor):
    
    def __init__(self, config):
        self.client = CosmosDBClient(config)

    def extract_hyponyms_disease(self, disease_name, query_api=util.QueryAPI.gremlin):
        """Extract the child class diseases of the user specified one.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            disease_name: the name of the candidate disease
            query_api: the API used for Cosmos DB. It could be Gremlin or SQL.

        Returns:
            The set of relevant entities in dictionary.

        """
        query = f"g.V().haslabel('disease').has('name', '{disease_name}').out('is subclass of').values('name')"

        logger.debug(f"Gremlin Query: {query}")
    
        results = self.client.execute_traversal(query)

        similar_diseases = []

        # The result is returned in batch
        for result in results:
            similar_diseases.extend(result)

        # Remove duplication if any
        similar_diseases = list(dict.fromkeys(similar_diseases))

        return similar_diseases

    def extract_hypernyms_disease(self, disease_name, query_api=util.QueryAPI.gremlin):
        """Extract the parrent class disease of the user specified one.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            disease_name: the name of the candidate disease
            query_api: the API used for Cosmos DB. It could be Gremlin or SQL.

        Returns:
            The set of relevant entities in dictionary.

        """
        query = f"g.V().haslabel('disease').has('name', '{disease_name}').in('is subclass of').values('name')"

        logger.debug(f"Gremlin Query: {query}")
    
        results = self.client.execute_traversal(query)

        similar_diseases = []

        # The result is returned in batch
        for result in results:
            similar_diseases.extend(result)

        # Remove duplication if any
        similar_diseases = list(dict.fromkeys(similar_diseases))

        return similar_diseases

    def extract_similar_disease(self, disease_name, query_api=util.QueryAPI.gremlin):
        """Extract similar the similar diseases of the user specified one.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            disease_name: the name of the candidate disease
            query_api: the API used for Cosmos DB. It could be Gremlin or SQL.

        Returns:
            The set of relevant entities in dictionary.

        """

        hyponyms = self.extract_hyponyms_disease(disease_name)
        hypernyms = self.extract_hypernyms_disease(disease_name)

        return [hyponyms, hypernyms]


    def extract_relevant_entities(self, ner_result):
        """Extract similar disease from KG.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            ner_result: The ner_result in dictonary.

        Returns:
            The set of relevant entities in dictionary.

        """

        disease_instance, disease_name = util.count_entities(ner_result)

        relevant_entities = {}

        if disease_instance > 1:
            logger.warn("Only one disease can be specified in the query. "
                        "Stop retrieving relevant entities.")
            return None  

        elif disease_name is not None:
            similar_diseases = self.extract_similar_disease(disease_name)
            if similar_diseases is not None:
                relevant_entities = similar_diseases
            else:
                return None

        else:
            return None
        
        return relevant_entities