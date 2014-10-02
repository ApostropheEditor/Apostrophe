# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

"""
Combiner classes to merge results from several predictors.

"""

from __future__ import absolute_import, unicode_literals

import abc

from . import predictor

class Combiner(object):
    """
    Base class for all combiners
    """
    
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    def filter(self, prediction):
        seen_tokens = set()
        result = predictor.Prediction()
        for i, suggestion in enumerate(prediction):
            token = suggestion.word
            if token not in seen_tokens:
                for j in range(i+1, len(prediction)):
                    if token == prediction[j].word:
                        # TODO: interpolate here?
                        suggestion.probability += prediction[j].probability
                        if suggestion.probability > \
                                predictor.MAX_PROBABILITY:
                            suggestion.probability = \
                                MAX_PROBABILITY
                seen_tokens.add(token)
                result.add_suggestion(suggestion)
        return result

    @abc.abstractmethod
    def combine(self):
        raise NotImplementedError("Method must be implemented")


class MeritocracyCombiner(Combiner):

    def __init__(self):
        pass

    def combine(self, predictions):
        result = predictor.Prediction()
        for prediction in predictions:
            for suggestion in prediction:
                result.add_suggestion(suggestion)
        return(self.filter(result))
