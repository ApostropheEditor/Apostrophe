# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

from __future__ import absolute_import, unicode_literals

import pressagio.predictor
import pressagio.combiner

class TestMeritocracyCombiner:

    def setup(self):
        self.combiner = pressagio.combiner.MeritocracyCombiner()

    def _create_prediction(self):
        prediction = pressagio.predictor.Prediction()
        prediction.add_suggestion(pressagio.predictor.Suggestion(
            "Test", 0.3))
        prediction.add_suggestion(pressagio.predictor.Suggestion(
            "Test2", 0.3))
        prediction.add_suggestion(pressagio.predictor.Suggestion(
            "Test", 0.1))
        prediction.add_suggestion(pressagio.predictor.Suggestion(
            "Test3", 0.2))
        return prediction

    def _create_prediction2(self):
        prediction = pressagio.predictor.Prediction()
        prediction.add_suggestion(pressagio.predictor.Suggestion(
            "Test2", 0.3))
        prediction.add_suggestion(pressagio.predictor.Suggestion(
            "Test", 0.1))
        prediction.add_suggestion(pressagio.predictor.Suggestion(
            "Test3", 0.2))
        return prediction

    def test_filter(self):
        result = self.combiner.filter(
            self._create_prediction())

        correct = pressagio.predictor.Prediction()
        correct.add_suggestion(pressagio.predictor.Suggestion(
            "Test3", 0.2))
        correct.add_suggestion(pressagio.predictor.Suggestion(
            "Test2", 0.3))
        correct.add_suggestion(pressagio.predictor.Suggestion(
            "Test", 0.4))

        assert result == correct

    def test_combine(self):
        predictions = [ self._create_prediction2() ]
        prediction2 = self._create_prediction2()
        prediction2.add_suggestion(pressagio.predictor.Suggestion(
            "Test4", 0.1))
        predictions.append(prediction2)
        result = self.combiner.combine(predictions)

        correct = pressagio.predictor.Prediction()
        correct.add_suggestion(pressagio.predictor.Suggestion(
            "Test3", 0.4))
        correct.add_suggestion(pressagio.predictor.Suggestion(
            "Test2", 0.6))
        correct.add_suggestion(pressagio.predictor.Suggestion(
            "Test4", 0.1))
        correct.add_suggestion(pressagio.predictor.Suggestion(
            "Test", 0.2))

        assert result == correct
