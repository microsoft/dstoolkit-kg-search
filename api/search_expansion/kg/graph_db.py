# -*- coding: utf-8 -*-
"""
This module provides functions to connect to the underlying Knowledge Graph store.


"""

from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import sys
import traceback
import logging

logger = logging.getLogger(__name__)

class Client:
    
    __config = dict()

    def __init__(self, config):
        pass

    def insert_vertices(self, query):
        """Insert vertices to graph db.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            query: The vertices insertion query.

        Returns:
            status indicates success or not.

        """
        pass

    def insert_edges(self, query):
        """Insert edges to graph db.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            query: The edges insertion query.

        Returns:
            status indicates success or not.

        """
        pass

    def update_vertices(self, query):
        """Update vertices in graph db.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            query: The vertices update query.

        Returns:
            status indicates success or not.

        """
        pass

    def execute_traversals(self, query):
        """Traverse the graph db.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            query: The graph traversal query.

        Returns:
            query result.

        """
        pass

    def drop_vertices(self, query):
        """Drop vertices in graph db.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            query: The vertices deletion query.

        Returns:
            status indicates success or not.

        """
        pass

    def drop_edges(self, query):
        """Drop edges in graph db.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            query: The edges deletion query.

        Returns:
            status indicates success or not.

        """
        pass

    def cleanup_graph(self):
        """Drop edges in graph db.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:

        Returns:
            status indicates success or not.

        """
        pass   


class CosmosDBClient(Client):

    def __init__(self, config):

        try:
            self.__config = config

            # Get connection information
            server = config['server']
            db = config['db']
            graph = config['graph']
            password = config['password']

            self.client = client.Client(server, 'g',
                            username="/dbs/{}/colls/{}".format(db, graph),
                            password=password,
                            message_serializer=serializer.GraphSONSerializersV2d0()
                            )

        except GremlinServerError as e:
            logger.error('Code: {0}, Attributes: {1}'.format(e.status_code, e.status_attributes))    

    def insert_vertices(self, query):
        """Insert vertices to graph db.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            query: The vertices insertion query.

        Returns:
            status indicates success or not.

        """
        logger.debug("Vertices insertion query:\n\t{0}".format(query))
        callback = self.client.submitAsync(query)
        if callback.result() is not None:
            logger.debug("Inserted these vertices: {}".format(
                callback.result().all().result()))

            return callback.result().status_attributes
        else:
            logger.error("Something went wrong with this query:\n\t{0}".format(query))
        
        
    def insert_edges(self, query):
        """Insert edges to graph db.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            query: The edges insertion query.

        Returns:
            status indicates success or not.

        """
        logger.debug("Edges insertion query:\n\t{0}".format(query))
        callback = self.client.submitAsync(query)
        if callback.result() is not None:
            logger.debug("Inserted these edges: {}".format(
                callback.result().all().result()))

            return callback.result().status_attributes
        else:
            logger.error("Something went wrong with this query:\n\t{0}".format(query))
              
    def execute_traversal(self, query):
        """Traverse the graph db.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            query: The graph traversal query.

        Returns:
            query result.

        """
        logger.debug("Graph travesal query:\n\t{0}".format(query))
        callback = self.client.submitAsync(query)
        
        return callback.result()

    def execute_traversal_sync(self, query):
        """Traverse the graph db.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            query: The graph traversal query.

        Returns:
            query result.

        """
        logger.debug("Graph travesal query:\n\t{0}".format(query))
        result = self.client.submit(query)
        
        return result

    def drop_vertices(self, label):
        """Drop vertices in graph db.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            label: The lable of node to drop

        Returns:
            status indicates success or not.

        """
        logger.debug("Graph droping nodel type:\n\t{0}".format(label))
        query = f"g.V().hasLabel('{label}').drop()"

        callback = self.client.submitAsync(query)

        return callback.result().status_attributes

    def cleanup_graph(self):
        """Drop edges in graph db.
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:

        Returns:
            status indicates success or not.

        """

        return 

        # gremlin_cleanup_graph = 'g.V().drop()'

        # callback = self.client.submitAsync(gremlin_cleanup_graph)
        # if callback.result() is not None:
        #     callback.result().all().result() 
        
        #     return callback.result().status_attributes