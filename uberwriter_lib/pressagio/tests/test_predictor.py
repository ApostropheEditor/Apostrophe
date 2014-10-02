# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

from __future__ import absolute_import, unicode_literals

import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import pressagio.predictor
import pressagio.tokenizer
import pressagio.dbconnector
import pressagio.context_tracker
import pressagio.callback

class TestSuggestion():

    def setup(self):
        self.suggestion = pressagio.predictor.Suggestion("Test", 0.3)

    def test_probability(self):
        self.suggestion.probability = 0.1
        assert self.suggestion.probability == 0.1


class TestPrediction():

    def setup(self):
        self.prediction = pressagio.predictor.Prediction()

    def test_add_suggestion(self):
        self.prediction.add_suggestion(pressagio.predictor.Suggestion(
            "Test", 0.3))
        assert self.prediction[0].word == "Test"
        assert self.prediction[0].probability == 0.3

        self.prediction.add_suggestion(pressagio.predictor.Suggestion(
            "Test2", 0.2))
        assert self.prediction[0].word == "Test"
        assert self.prediction[0].probability == 0.3
        assert self.prediction[1].word == "Test2"
        assert self.prediction[1].probability == 0.2

        self.prediction.add_suggestion(pressagio.predictor.Suggestion(
            "Test3", 0.6))
        assert self.prediction[0].word == "Test3"
        assert self.prediction[0].probability == 0.6
        assert self.prediction[1].word == "Test"
        assert self.prediction[1].probability == 0.3
        assert self.prediction[2].word == "Test2"
        assert self.prediction[2].probability == 0.2

        self.prediction[:] = []

    def test_suggestion_for_token(self):
        self.prediction.add_suggestion(pressagio.predictor.Suggestion(
            "Token", 0.8))
        assert self.prediction.suggestion_for_token("Token").probability == 0.8
        self.prediction[:] = []

class StringStreamCallback(pressagio.callback.Callback):

    def __init__(self, stream):
        pressagio.callback.Callback.__init__(self)
        self.stream = stream

class TestSmoothedNgramPredictor():

    def setup(self):
        self.dbfilename = os.path.abspath(os.path.join(
            os.path.dirname( __file__ ), 'test_data', 'test.db'))
        self.infile = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
            'test_data', 'der_linksdenker.txt'))

        for ngram_size in range(3):
            ngram_map = pressagio.tokenizer.forward_tokenize_file(
                self.infile, ngram_size + 1, False)
            pressagio.dbconnector.insert_ngram_map_sqlite(ngram_map, ngram_size + 1,
                self.dbfilename, False)

        config_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
            'test_data', 'profile_smoothedngram.ini'))
        config = configparser.ConfigParser()
        config.read(config_file)
        config.set("Database", "database", self.dbfilename)

        self.predictor_registry = pressagio.predictor.PredictorRegistry(config)

        self.callback = StringStreamCallback("")
        context_tracker = pressagio.context_tracker.ContextTracker(
            config, self.predictor_registry, self.callback)

    def test_predict(self):
        predictor = self.predictor_registry[0]
        predictions = predictor.predict(6, None)
        assert len(predictions) == 6
        words = []
        for p in predictions:
            words.append(p.word)
        assert "er" in words
        assert "der" in words
        assert "die" in words
        assert "und" in words
        assert "nicht" in words

        self.callback.stream="d"
        predictions = predictor.predict(6, None)
        assert len(predictions) == 6
        words = []
        for p in predictions:
            words.append(p.word)
        assert "der" in words
        assert "die" in words
        assert "das" in words
        assert "da" in words
        assert "Der" in words

        self.callback.stream="de"
        predictions = predictor.predict(6, None)
        assert len(predictions) == 6
        words = []
        for p in predictions:
            words.append(p.word)
        assert "der" in words
        assert "Der" in words
        assert "dem" in words
        assert "den" in words
        assert "des" in words

    def teardown(self):
        if self.predictor_registry[0].db:
            self.predictor_registry[0].db.close_database()
        del(self.predictor_registry[0])
        if os.path.isfile(self.dbfilename):
            os.remove(self.dbfilename)
