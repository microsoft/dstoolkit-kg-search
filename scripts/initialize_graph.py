from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import os
import sys
import logging
from dotenv import load_dotenv

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

work_dir = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':

    try:
        load_dotenv() 

        server = os.environ['COSMOS_DB_SERVER']
        db = os.environ['COSMOS_DB_DATABASE']
        graph = os.environ['COSMOS_DB_GRAPH']
        password = os.environ['COSMOS_DB_PASSWORD']
    
        client = client.Client(server, 'g',
                    username="/dbs/{}/colls/{}".format(db, graph),
                    password=password,
                    message_serializer=serializer.GraphSONSerializersV2d0()
                    )

        vertex_file_name = os.path.join(work_dir, 'graph_vertex.txt')
        edge_file_name = os.path.join(work_dir, 'graph_edge.txt')

        # Insert vertex
        print("Adding vertex.....")
        with open(vertex_file_name, 'r') as vertex_file:
            for line in vertex_file.readlines():
                query = line.strip()

                # It is an vertex insertion query
                if query.startswith('g.addV'):
                    callback = client.submitAsync(query)
                    if callback.result() is not None:
                        logger.debug("Inserted these vertices: {}".format(
                            callback.result().all().result()))

        # Insert edge
        print("Adding edges.....")
        with open(edge_file_name, 'r') as edge_file:
            for line in edge_file.readlines():
                query = line.strip()

                # It is an edge insertion query
                if query.startswith('g.V'):
                    callback = client.submitAsync(query)
                    if callback.result() is not None:
                        logger.debug("Inserted these vertices: {}".format(
                            callback.result().all().result()))
    
    except GremlinServerError as e:
        logger.error('Code: {0}, Attributes: {1}'.format(e.status_code, e.status_attributes))

        if e.status_attributes['x-ms-status-code'] == 409:
            logger.error('Cannot insert duplicated vertex!')  
