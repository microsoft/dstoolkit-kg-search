# -*- coding: utf-8 -*-
"""
This is the module provides functions to connect to the underlying search engine.


"""

import requests
import json
import logging
from os.path import dirname, join, realpath
import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    ComplexField,
    CorsOptions,
    SearchIndex,
    ScoringProfile,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    SynonymMap
)


# set logging level
logging.basicConfig(level=logging.INFO)

class SearchSDK:
    def __init__(self, config):
        # retrieve search instance config
        self.search_endpoint = config['endpoint']
        self.search_api_key = config['api_key']
        self.index_name = config['index_name']
        self.api_version = config['api_version']

        # construct official clients
        self.search_client = SearchClient(self.search_endpoint, self.index_name, AzureKeyCredential(self.search_api_key))
        self.indexers_client = SearchIndexerClient(self.search_endpoint, AzureKeyCredential(self.search_api_key))
        self.index_client = SearchIndexClient(self.search_endpoint, AzureKeyCredential(self.search_api_key))
    
    ''' Query '''
    def advanced_search(self, payload):
        headers = {
            'Content-Type': 'application/json',
            'api-key': self.search_api_key
        }
        payload = json.dumps(payload)
        url = f'{self.search_endpoint}/indexes/{self.index_name}/docs/search?api-version={self.api_version}'
        r = requests.post(url, headers=headers, data=payload)
        return r.status_code, r.json()


    def simple_text_query(self, query_string):
        results = self.search_client.search(search_text=query_string)
        return results


    def filter_query(self, select_cols, keywords, filters):
        results = self.search_client.search(
            search_text=keywords if keywords else '*',
            filter=filters if filters else '', ##"field eq 'value' refer to odata $filter syntax",
            select=",".join(select_cols) if select_cols else '*'
        )
        return results

    ''' Indexer '''
    def list_indexers(self):
        result = self.indexers_client.get_indexers()
        return [x.name for x in result]
        

    ''' Documents'''
    def upload_document(self, documents):
        result = self.search_client.upload_documents(documents=documents)
        print("Upload of new document succeeded: {}".format(result[0].succeeded))


    def merge_document(self, documents):
        result = self.search_client.merge_documents(documents=documents)
        return f"Merge into new document succeeded: {result[0].succeeded}"

    
    def delete_document(self, documents):
        result = self.search_client.delete_documents(documents=documents)

        print("Delete new document succeeded: {}".format(result[0].succeeded))


    ''' Index '''
    def create_index(self, index_name, fields):
        cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
        
        index = SearchIndex(
            name=index_name,
            fields=fields,
            cors_options=cors_options)

        result = self.index_client.create_index(index_name)
        

    def get_index(self, index_name):
        result = self.index_client.get_index(index_name)


    def update_index(self, index_name, fields):
        cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
        index = SearchIndex(
            name=index_name,
            fields=fields,
            cors_options=cors_options)

        result = self.index_client.create_or_update_index(index=index)


    def delete_index(self, index_name):
        self.index_client.delete_index(index_name)


    def create_synonym_map(self, synonyms, synonym_map_name):
        # synonyms = [
        #     "USA, United States, United States of America",
        #     "Washington, Wash. => WA",
        # ]
        try:
            synonym_map = SynonymMap(name=synonym_map_name, synonyms=synonyms)
            result = self.index_client.create_synonym_map(synonym_map)
            logging.info(f'[INFO] Created synonym map {synonym_map_name}')
            return result

        except Exception as e:
            logging.error(f'[ERROR]', e.args)
            return None


    
    def create_or_update_synonym_map(self, synonyms, synonym_map_name):
        # synonyms = [
        #     "USA, United States, United States of America",
        #     "Washington, Wash. => WA",
        # ]
        try:
            synonym_map = SynonymMap(name=synonym_map_name, synonyms=synonyms)
            result = self.index_client.create_or_update_synonym_map(synonym_map)
            logging.info(f'[INFO] Created or updated synonym map {synonym_map_name}')
            return result

        except Exception as e:
            logging.error(f'[ERROR]', e.args)
            return None



    def create_synonym_map_from_file(self, synonym_map_name, file_path):
        try:
            CWD = dirname(realpath(__file__))
            file_path = join(CWD, file_path)
            with open(file_path, "r") as f:
                solr_format_synonyms = f.read()
                synonyms = solr_format_synonyms.split("\n")
                synonym_map = SynonymMap(
                    name=synonym_map_name, synonyms=synonyms)
                result = self.index_client.create_synonym_map(synonym_map)
                logging.info(f'[INFO] Created synonym map {synonym_map_name}')
                return result
        except Exception as e:
            logging.error(f'[ERROR]', e.args)
            return None


    def get_synonym_maps(self):
        try:
            result = self.index_client.get_synonym_maps()
            names = [x.name for x in result]
            logging.info(
                f'[INFO] Found {len(result)} synonym maps: {", ".join(names)}')

            return names

        except Exception as e:
            logging.error(f'[ERROR]', e.args)
            return None

    def get_synonym_map(self, synonym_map_name):
        try:
            result = self.index_client.get_synonym_map(synonym_map_name)
            logging.info(f'[INFO] Found synonym map {synonym_map_name}')
            return result

        except Exception as e:
            logging.error(f'[ERROR]', e.args)
            return None


    def delete_synonym_map(self, synonym_map_name):
        try:
            self.index_client.delete_synonym_map(synonym_map_name)
            logging.info(f'[INFO] Delete synonym map {synonym_map_name}')

        except Exception as e:
            logging.error(f'[ERROR]', e.args)
