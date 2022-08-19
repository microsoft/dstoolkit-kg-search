import unittest
import os
from api.search_expansion.kg.graph_db import CosmosDBClient
from dotenv import load_dotenv
import uuid
import time

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

test_label = uuid.uuid4()

class CosmosDBClientTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Method called to prepare the test fixture.
        """

        load_dotenv() 
        
        config = {}
        config['server'] = os.environ['COSMOS_DB_SERVER']
        config['db'] = os.environ['COSMOS_DB_DATABASE']
        config['graph'] = os.environ['COSMOS_DB_GRAPH']
        config['password'] = os.environ['COSMOS_DB_PASSWORD']
        
        cls.client = CosmosDBClient(config)

    @classmethod
    def tearDownClass(cls):
        """Method called immediately after the test method has been called 
        and the result recorded.
        """

        cls.client.drop_vertices(test_label)

    def test_graph_travesal(self):
        """Test vertices insertion, edge insertion and graph traversal function in one test.
        """
        gremlin_insert_vertices = [
            f"g.addV('{test_label}').property('id', 'thomas').property('firstName', 'Thomas').property('age', 44).property('pk', 'pk')",
            f"g.addV('{test_label}').property('id', 'mary').property('firstName', 'Mary').property('lastName', 'Andersen').property('age', 39).property('pk', 'pk')",
            f"g.addV('{test_label}').property('id', 'ben').property('firstName', 'Ben').property('lastName', 'Miller').property('pk', 'pk')",
            f"g.addV('{test_label}').property('id', 'robin').property('firstName', 'Robin').property('lastName', 'Wakefield').property('pk', 'pk')"
        ]

        for query in gremlin_insert_vertices:
            status_code = CosmosDBClientTest.client.insert_vertices(query)['x-ms-status-code']
            assert status_code == 200

        gremlin_insert_edges = [
            "g.V('thomas').addE('knows').property('id', 'thomas knows mary').to(g.V('mary'))",
            "g.V('thomas').addE('knows').property('id', 'thomas knows ben').to(g.V('ben'))",
            "g.V('ben').addE('knows').property('id', 'ben knows robin').to(g.V('robin'))"
        ]

        start_time = time.time()
        for query in gremlin_insert_edges:
            status_code = CosmosDBClientTest.client.insert_edges(query)['x-ms-status-code']
            assert status_code == 200
        print(f"Average insertion time: {(time.time() - start_time)/len(gremlin_insert_edges)} second")

        query = f"g.V().hasLabel('{test_label}').has('age', gt(30)).values('firstName', 'age')"

        start_time = time.time()
        results = CosmosDBClientTest.client.execute_traversal(query)

        for r in results:
            assert r[0] == 'Thomas'
            assert r[1] == 44
        print(f"Travesal execution time: {time.time() - start_time} second")

        query = f"g.V().count()"

        start_time = time.time()
        results = CosmosDBClientTest.client.execute_traversal(query)

        for r in results:
            print(r)
        print(f"Travesal execution time: {time.time() - start_time} second")



