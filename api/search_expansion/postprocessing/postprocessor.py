# -*- coding: utf-8 -*-
"""
This module provides functions to post-process the search result.

"""


class PostProcessor:
    
    __config = dict()

    def __init__(self, config):
        pass

    def postprocess(self, initial_results, expanded):
        """Extract similar the similar diseases of the user specified one.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            initial_results: the initial result of rewritten query.
            expanded: indicate if the query is expanded.

        Returns:
            The postprocessed result.

        """
        return initial_results


class UMLSPostProcessor(PostProcessor):

    pass