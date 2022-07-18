import unittest
import os
import search_expansion.util as util
from search_expansion.rewriting.query_rewriter import UMLSQueryRewriter

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

class RewriterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Method called to prepare the test fixture.
        """
        cls.query_rewriter = UMLSQueryRewriter()

    @classmethod
    def tearDownClass(cls):
        """Method called after all the test method have been called 
        and the result recorded.
        """
        pass

    def test_tokenizing_search_text(self):
        """Test the search text tokenizing function.
        """
        search_text = "keratoconus treatment"

        ner_result = {
                "tags": [
                    {
                        "category": "Disease",
                        "class": "Disease",
                        "length": 11,
                        "offset": 0,
                        "text": "keratoconus"
                    }
                ]
            }

        tokenized_text = RewriterTest.query_rewriter.tokenizing_search_text(search_text, ner_result)

        assert tokenized_text[0] == (True, "keratoconus", "Disease")
        assert tokenized_text[1] == (False, "treatment")

    def test_direct_relatated_query(self):
        """Test the rewriting function for direct relatability.
        """
        
        search_text = "keratoconus treatment"

        ner_result = {
                "tags": [
                    {
                        "category": "Disease",
                        "class": "Disease",
                        "length": 11,
                        "offset": 0,
                        "text": "keratoconus"
                    }
                ]
            }

        tokenized_text = RewriterTest.query_rewriter.tokenizing_search_text(search_text, ner_result)
        rewritten_query = RewriterTest.query_rewriter.direct_relatated_query(tokenized_text, 2)

        assert rewritten_query == "(+(treatment) +\"keratoconus\" +\"keratoconus\")"

    def test_adjacent_related_query_disease(self):
        """Test the rewriting function for adjacent relatability (Expanding on disease only).
        """        

        search_text = "keratoconus treatment"

        ner_result = {
                "tags": [
                    {
                        "category": "Disease",
                        "class": "Disease",
                        "length": 11,
                        "offset": 0,
                        "text": "keratoconus"
                    }
                ]
            }

        relevant_entities = [
            ['stable condition keratoconus', 'acute hydrops keratoconus'],
            ['corneal disease', 'corneal ectasia']
        ]

        disease_name = "keratoconus"

        tokenized_text = RewriterTest.query_rewriter.tokenizing_search_text(search_text, ner_result)
        rewritten_query = RewriterTest.query_rewriter.adjacent_related_query_disease(tokenized_text, relevant_entities, disease_name)

        assert rewritten_query == ("(+(treatment) +\"stable condition keratoconus\" +\"stable condition keratoconus\") "
                                   "(+(treatment) +\"acute hydrops keratoconus\" +\"acute hydrops keratoconus\") "
                                   "(+(treatment) +\"corneal disease\") "
                                   "(+(treatment) +\"corneal ectasia\")")

    def test_rewrite(self):
        """Test the rewrite function.
        """

        search_text = "keratoconus treatment"

        ner_result = {
                "tags": [
                    {
                        "category": "Disease",
                        "class": "Disease",
                        "length": 11,
                        "offset": 0,
                        "text": "keratoconus"
                    }
                ]
            }

        relevant_entities = [
            ['stable condition keratoconus', 'acute hydrops keratoconus'],
            ['corneal disease', 'corneal ectasia']
        ]

        rewritten_query = RewriterTest.query_rewriter.rewrite(search_text, ner_result, relevant_entities)

        assert rewritten_query == ("(+(treatment) +\"keratoconus\" +\"keratoconus\" +\"keratoconus\") | "
                                   "(+(treatment) +\"stable condition keratoconus\" +\"stable condition keratoconus\") "
                                   "(+(treatment) +\"acute hydrops keratoconus\" +\"acute hydrops keratoconus\") "
                                   "(+(treatment) +\"corneal disease\") "
                                   "(+(treatment) +\"corneal ectasia\")")
