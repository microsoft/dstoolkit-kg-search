# -*- coding: utf-8 -*-
"""
This is the main module to control the whole logic for query expansion.


"""
import os
import sys
import logging
import asyncio
import argparse
import time
from dotenv import load_dotenv

sys.path.append('../')

from search_expansion.preprocessing.preprocessor import UMLSPreProcessor
from search_expansion.nerprocessing.ner import UMLSNer
from search_expansion.kg.knowledge_extractor import UMLSKnowledgeExtractor
from search_expansion.rewriting.query_rewriter import UMLSQueryRewriter
from search_expansion.postprocessing.postprocessor import UMLSPostProcessor
from search_expansion.search_sdk import SearchSDK

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# logging.config.fileConfig('../config/logging.config')
logger = logging.getLogger(__name__)


class SearchExpander:
    
    __config = dict()

    def __init__(self):
        pass

    def expand(self, search_text="*", parameters=None):
        """Entry function to perform query expansion.

        Args:
            search_text: The search query.
            parameters: The parameter input to underlying search engine in dictionary.

        Returns:
            The expanded search result.

        """
        pass

class UMLSSearchExpander(SearchExpander):
    
    def __init__(self):
        load_dotenv() 
        
        # Initialize the preprocessor
        self.preprocessor_config = {}
        self.preprocessor = UMLSPreProcessor(self.preprocessor_config)
        
        # Initialize the NER processor
        self.ner_config = {}
        self.ner_config['endpoint'] = os.environ['NER_ENDPOINT']
        self.ner_config['token'] = os.environ['NER_BEAR_TOKEN']
        self.ner = UMLSNer(self.ner_config)

        # Initialize the knowledge extractor
        self.knowledge_extractor_config = {}
        self.knowledge_extractor_config['server'] = os.environ['COSMOS_DB_SERVER']
        self.knowledge_extractor_config['db'] = os.environ['COSMOS_DB_DATABASE']
        self.knowledge_extractor_config['graph'] = os.environ['COSMOS_DB_GRAPH']
        self.knowledge_extractor_config['password'] = os.environ['COSMOS_DB_PASSWORD']
        self.knowledge_extractor = UMLSKnowledgeExtractor(self.knowledge_extractor_config)

        # Initialize the query rewriter
        self.rewriter_config = {}
        self.rewriter = UMLSQueryRewriter(self.rewriter_config)

        # Initialize the search engine configuration
        self.acs_config = {}
        self.acs_config['endpoint'] = os.environ['ACS_ENDPOINT']
        self.acs_config['api_key'] = os.environ['ACS_API_KEY']
        self.acs_config['index_name'] = os.environ['ACS_INDEX_NAME']
        self.acs_config['api_version'] = os.environ['ACS_API_VERSION']

        self.search_client = SearchSDK(self.acs_config)

        # Initialize the postprocessor
        self.postprocessor_config = {}
        self.postprocessor = UMLSPostProcessor(self.postprocessor_config)


    def search(self, search_text, parameters=None):
        """Sumbit each query to the underlying search engine. 

        Args:
            search_text: The search query.
            se: The parameter input to underlying search engine in dictionary.

        Returns:
            The search result.

        """
        try:
            if parameters is None:
                # Default parameters
                parameters = {
                    "queryType": "simple",
                    "queryLanguage": "en-us",
                    "select": "title",
                    "top": 20,
                    "count": True
                }
            # Include all parameters
            payload = parameters

            # Input search query
            payload["search"] = search_text

        except (AttributeError, TypeError):
            raise AssertionError('parameters should be dictionary')

        code, results = self.search_client.advanced_search(payload)

        return results, code 

    def expand(self, search_text="*", parameters=None):
        """Entry function to perform query expansion, submision to ACS and 
        post-processing of the result. The query expansion is based on the 
        equipment similarity and plant similarity. 

        Note:
            Some ACS parameters, like queryType, searchMode will be fully 
            controlled by the expand function.

        Args:
            search_text: The search query.
            parameters: The parameter input to underlying search engine in dictionary.

        Returns:
            The expanded search result.

        """
        start_time = time.time()
        logger.info("********** Start query expansion **********")
        logger.info("--------------------------------------------------")

        logger.info("********** Preprocess the original query **********")
        logger.info("--------------------------------------------------")
        preprocessed_text = self.preprocessor.preprocess(search_text)
        logger.info(f"Preprocessed text: {preprocessed_text}")
        logger.info(f"Time for preprocessing: {time.time() - start_time} seconds")

        start_time = time.time()
        logger.info("********** Conduct NER **********")
        logger.info("--------------------------------------------------")
        ner_result = self.ner.extract_entities(preprocessed_text)
        logger.info(f"NER result: {ner_result}")
        logger.info(f"Time for NER: {time.time() - start_time} seconds")

        start_time = time.time()
        logger.info("********** Retrieve relevant entities from KG **********")
        logger.info("--------------------------------------------------")
        relevant_entities = self.knowledge_extractor.extract_relevant_entities(ner_result)
        logger.info(f"KG result: {relevant_entities}")
        logger.info(f"Time for KG: {time.time() - start_time} seconds")

        start_time = time.time()
        logger.info("********** Perform query rewriting **********")
        logger.info("--------------------------------------------------")
        rewritten_query = self.rewriter.rewrite(preprocessed_text, ner_result, relevant_entities)

        expanded = True
        # No rewritten at all
        if rewritten_query == preprocessed_text:
            # Just use the original one
            rewritten_query = search_text
            expanded = False
        
        logger.info(f"Rewrittern query: {rewritten_query}")
        logger.info(f"Time for rewriting: {time.time() - start_time} seconds")

        start_time = time.time()
        logger.info("********** Submit the rewritten query **********")
        logger.info("--------------------------------------------------")
        initial_results, code = self.search(rewritten_query, parameters)
        

        logger.info("********** Postprocess the search result **********")
        logger.info("--------------------------------------------------")
        postprocessed_result = self.postprocessor.postprocess(initial_results, expanded)
        logger.info(f"Time for Final Result: {time.time() - start_time} seconds")

        return postprocessed_result, code 


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='KG-based Search Expansion')
    parser.add_argument('search_text', type=str, help='the original search text')

    args = parser.parse_args()

    search_text = args.search_text
    search_expander = UMLSSearchExpander()

    logger.info(f"Original query: {search_text}\n")

    start_time = time.time()
    final_result = search_expander.expand(search_text)
    logger.info(f"Final result: ")

    count = 0
    for result in final_result['value']:
        
        if count % 10 == 0:
            logger.info(f"Top {count+1} to {count+10}:")

        logger.info(result)
        count += 1

    logger.info(f"Time e2e: {time.time() - start_time} seconds")
    
    