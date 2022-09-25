# -*- coding: utf-8 -*-
"""
This module provides functions to rewrite the original search text based 
on the relevant entities retrieved from the Knowledge Graph.

"""

import enum
import sys
import re
import logging
import api.search_expansion.util as util

logger = logging.getLogger(__name__)


class QueryRewriter:
    
    __config = dict()

    def __init__(self, config=None):
        pass

    def rewrite(self, search_text, ner_result, relevant_entities):
        """Entry function to perform query rewriting. 

        Args:
            search_text: The search query.
            ner_result: The ner result of the search query
            relevant_entities: The relevant entities to the oroginal entities in search text.

        Returns:
            The rewritten query in string.

        """
        return search_text

class AircraftQueryRewriter(QueryRewriter):
    

    def process_disease_name(self, disease_name):
        """Specical processing to disease name such that it can be matched by expectation.

        """
        # Make sure we dont double quote
        disease_name.strip('\"')

        return f"\"{disease_name}\""
    
    def construct_sub_query(self, tokenized_text, original_entity, target_entity, repeat=1):
        """Construct the sub-query by replacing the original entity to target entity. Repeating the 
        entity can improve the keywork match score.
        
        """
        optional_terms_before_orginal_entity = []
        optional_terms_after_original_entity = []
        original_entity_hit = False

        logger.debug(f"Original entity: {original_entity}, Target entity: {target_entity}")
        for term in tokenized_text:
           
            if not term[0] and not original_entity_hit:
                # optional terms only and not reach the original entity yet
                optional_terms_before_orginal_entity.append(term[1])
            elif term[0] and not original_entity_hit:
                # plant or equipment hit
                assert len(term) == 3
                if term[1] == original_entity:
                    original_entity_hit = True
                else:
                    # It is not out expansion target
                    optional_terms_before_orginal_entity.append(term[1])
            elif original_entity_hit:
                # optional terms after the original entity            
                optional_terms_after_original_entity.append(term[1])

        target_entity_repeated = []
        for i in range(0, repeat):
            # Repeat the term will increase the keyword match score in ACS
            target_entity_repeated.append(target_entity)

        candidate_terms = []
        
        all_optional_terms = optional_terms_before_orginal_entity + optional_terms_after_original_entity
        candidate_terms.append(f"+({' '.join(all_optional_terms)})") if len(all_optional_terms) > 0 else None
        candidate_terms.append(' +'.join(target_entity_repeated))

        return "(" + ' +'.join(candidate_terms) + ")" 

    def adjacent_related_query_disease(self, tokenized_text, relevant_entities, disease_name):
        """The similar disease with have this priority:
        P1: child class of the specified disease
        P2: parrent class of the specified disease

        Args:
            tokenized_text: The tolenized version of the original search query.
            relevant_entities: The relevant entities to the original entities in search text.

            Example:
            relevant_entities = {
                ["A", "B", "C"],
                ["E", "F", "G"]
            }

            The priority of the similar plants is inherited by the order.
            In the above example, ["A", "B", "C"] has high priority than ["E", "F", "G"].
            So, the rewrittrn query for ["A", "B", "C"] take priority to that for ["E", "F", "G"].
        Returns:
            The rewritten query in string.

        """
        
        logger.debug(f"Original disease name: {disease_name}")

        assert len(relevant_entities) > 0

        
        similar_diseases = relevant_entities
        length = len(similar_diseases)
        repeat = length

        query_strs = []
        for disease_list in similar_diseases:
            for disease in disease_list:
                # Add double quote to make sure they appear in the result
                disease_quoted = f"\"{disease}\""

                sub_query = self.construct_sub_query(tokenized_text, disease_name, disease_quoted, repeat)
                query_strs.append(sub_query)
            # decrease the repeating number to lower the keywork match score in ACS
            repeat -= 1
        
        
        rewritten_query = " ".join(query_strs)

        logger.debug(f"Expanded query for disease only: {rewritten_query}")
        return rewritten_query

    def adjacent_related_query(self, tokenized_text, relevant_entities, disease_name):
        """Return the query for adjacent relatability. 

        Args:
            tokenized_text: The tolenized version of the original search query.
            ner_result: The list of original entities detected in the search text.
            relevant_entities: The relevant entities to the original entities in search text.
            disease_name: The disease name identified in the search text.
        Returns:
            The rewritten query in string.
        """

        # Only expand in the disease level
        
        if disease_name is not None:
            rewritten_query = self.adjacent_related_query_disease(tokenized_text, relevant_entities, disease_name)
        
        else:
            original_query = " ".join([term[1] for term in tokenized_text])
            logger.warn(f"We dont support expansion on this kind of query: {original_query}")
            rewritten_query = "" 

        return rewritten_query

    def direct_relatated_query(self, tokenized_text, repeat=1):
        """Return the query for direct relatability, namely, query for the exact disease.

        Args:
            tokenized_text: The tolenized version of the original search query.
            repeat: the number of repeation to the original entity

        Returns:
            The rewritten query in string.

        """
        
        original_disease = None
        rewritten_query = None

        for term in tokenized_text:
            # Compulsory term
            if term[0]:
                assert len(term) == 3
                if term[2] == 'Disease':
                    # Equipment take priority to plant when doing expansion
                    original_disease = term[1]
                    break

        if original_disease is not None:
            target_disease = self.process_disease_name(original_disease)
            rewritten_query = self.construct_sub_query(tokenized_text, original_disease, target_disease, repeat)
        else:
            pass
        

        logger.debug(f"Rewrittnen query for direct relatability: {rewritten_query}")
        return rewritten_query


    def tokenizing_search_text(self, search_text, ner_result):
        """Tokenize the search text such that we can seperate out the optional terms and 
        the compulsory terms.

        Args:
            search_text: The original search query.
            ner_result: The list of original entities detected in the search text

        Returns:
            The tokenization result in list[(True/False, term, entity_class)].
            The first value indicates if a term is compulsory.
            The last value indicates the entity class if any.
        """        

        #TODO: need to handle specical charaters like ", +, - 
         
        tokenized_text = []

        start = 0
        end = 0

        compulsory_pos = []

        # Identify the position of the entity
        for tag in ner_result['tags']:
            start = re.search(tag['text'], search_text).start()
            end = re.search(tag['text'], search_text).end()
            compulsory_pos.append((start, end, tag['class']))

        # Sorted by the start position
        compulsory_pos = sorted(compulsory_pos, key=lambda x: x[0])

        logger.debug(f"Compulsory pos: {compulsory_pos}")

        # Start to chunk the search text
        current_pos = 0

        for pos in compulsory_pos:
            compulsory_term_start = pos[0]
            compulsory_term_end= pos[1]

            if current_pos < compulsory_term_start:
                # Concate all string up to the next compulsory term
                # Trim the space if any
                tokenized_text.append((False, search_text[current_pos: 
                                                    compulsory_term_start-1].strip()))
                # Move to the next tokens

                # Add the next compulsory term
                # Trim the space if any
                tokenized_text.append((True, search_text[compulsory_term_start: 
                                                    compulsory_term_end].strip(),
                                                    pos[2]))


            elif current_pos == compulsory_term_start:
                # Trim the space if any
                tokenized_text.append((True, search_text[compulsory_term_start: 
                                    compulsory_term_end].strip(), pos[2]))

            # Move to the next tokens
            current_pos = compulsory_term_end + 1

        # add the remaning terms as optional
        if current_pos < len(search_text) - 1:
            tokenized_text.append((False, search_text[current_pos: 
                                                len(search_text)].strip()))

        logger.debug(f"Tokenized result: {tokenized_text}")

        return tokenized_text
         

    def rewrite(self, search_text, ner_result, relevant_entities):
        """Entry function to perform query rewriting. 

        Args:
            search_text: The search query.
            ner_result: The ner result of the search query
            relevant_entities: The relevant entities to the original entities in search text.

        Returns:
            The rewritten query in string.

        """
        
        if relevant_entities is None:
            logger.debug("No entity to expand. Dont rewrite.")
            return search_text                  

        # Start rewriting
        else:

            return ("(\"WDM_CH21\"  \"WDM_CH21\") | (\"Service Bulletin 2015-05\" \"Service Bulletin 2015-05\") | "
                "(\"MLOG_298607\" \"MLOG_298607\"  \"MLOG_298607\") | +(VH-ACX air conditioning cockpit blower on and off)")

            tokenized_text = self.tokenizing_search_text(search_text, ner_result)

            repeat_for_direct = len(relevant_entities) + 1

            disease_instance, disease_name = util.count_entities(ner_result)
            
            direct_relatated_query = self.direct_relatated_query(tokenized_text, repeat_for_direct)
            adjacent_related_query = self.adjacent_related_query(tokenized_text, 
                                                                relevant_entities, 
                                                                disease_name)

            # Simply combine all the queries
            rewritten_query = direct_relatated_query + " | " + adjacent_related_query
                
            logger.debug(f"Rewritten query: {rewritten_query}")
            return rewritten_query