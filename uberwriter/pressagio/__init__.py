# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

from . import predictor
from . import context_tracker

class Pressagio:

    def __init__(self, callback, config, dbconnection = None):
        self.config = config
        self.callback = callback

        self.predictor_registry = pressagio.predictor.PredictorRegistry(
            self.config, dbconnection)
        self.context_tracker = pressagio.context_tracker.ContextTracker(
            self.config, self.predictor_registry, callback)

        self.predictor_activator = pressagio.predictor.PredictorActivator(
            self.config, self.predictor_registry, self.context_tracker)
        self.predictor_activator.combination_policy = "meritocracy"

    def predict(self):
        multiplier = 1
        predictions = self.predictor_activator.predict(multiplier)
        return [p.word for p in predictions]

    def close_database(self):
        self.predictor_registry.close_database()