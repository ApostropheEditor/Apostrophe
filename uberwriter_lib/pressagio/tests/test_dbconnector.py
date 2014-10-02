# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2001-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE

from __future__ import absolute_import, unicode_literals

import os

import pressagio.dbconnector

psycopg2_installed = False
try:
    import psycopg2
    psycopg2_installed = True
except ImportError:
    pass

class TestSqliteDatabaseConnector():

    def setup(self):
        self.filename = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
            'test_data', 'test.db'))
        self.connector = pressagio.dbconnector.SqliteDatabaseConnector(self.filename)
        self.connector.open_database()

    def test_execute_sql(self):
        self.connector.execute_sql("CREATE TABLE IF NOT EXISTS test ( c1 TEXT, c2 INTEGER );")

    def test_create_ngram_table(self):
        self.connector.create_ngram_table(1)
        result = self.connector.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_1_gram';")
        assert result == [('_1_gram',)]
        self.connector.execute_sql("DROP TABLE _1_gram;")

        self.connector.create_ngram_table(2)
        result = self.connector.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_2_gram';")
        assert result == [('_2_gram',)]
        self.connector.execute_sql("DROP TABLE _2_gram;")

        self.connector.create_ngram_table(3)
        result = self.connector.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_3_gram';")
        assert result == [('_3_gram',)]
        self.connector.execute_sql("DROP TABLE _3_gram;")

    def test_create_index(self):
        self.connector.create_ngram_table(2)
        self.connector.insert_ngram(('der', 'linksdenker'), 22)
        self.connector.create_index(2)
        result = self.connector.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='index' \
            AND name='idx_2_gram_1';")
        assert result == [('idx_2_gram_1',)]

        self.connector.execute_sql("DROP TABLE _2_gram;")

    def test_create_unigram_table(self):
        self.connector.create_unigram_table()
        result = self.connector.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_1_gram';")
        assert result == [('_1_gram',)]
        self.connector.execute_sql("DROP TABLE _1_gram;")

    def test_create_bigram_table(self):
        self.connector.create_bigram_table()
        result = self.connector.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_2_gram';")
        assert result == [('_2_gram',)]
        self.connector.execute_sql("DROP TABLE _2_gram;")

    def test_create_trigram_table(self):
        self.connector.create_trigram_table()
        result = self.connector.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_3_gram';")
        assert result == [('_3_gram',)]
        self.connector.execute_sql("DROP TABLE _3_gram;")

    def test_insert_ngram(self):
        self.connector.create_bigram_table()
        self.connector.insert_ngram(('der', 'linksdenker'), 22)
        result = self.connector.execute_sql("SELECT * FROM _2_gram")
        assert result == [('der', 'linksdenker', 22)]
        self.connector.execute_sql("DROP TABLE _2_gram;")

    def test_update_ngram(self):
        self.connector.create_bigram_table()

        # Insert
        self.connector.insert_ngram(('der', 'linksdenker'), 22)
        result = self.connector.execute_sql("SELECT * FROM _2_gram")
        assert result == [('der', 'linksdenker', 22)]

        # Update
        self.connector.update_ngram(('der', 'linksdenker'), 44)
        result = self.connector.execute_sql("SELECT * FROM _2_gram")
        assert result == [('der', 'linksdenker', 44)]

        self.connector.execute_sql("DROP TABLE _2_gram;")

    def test_ngram_count(self):
        self.connector.create_bigram_table()
        self.connector.insert_ngram(('der', 'linksdenker'), 22)
        result = self.connector.ngram_count(('der', 'linksdenker'))
        assert result == 22
        self.connector.execute_sql("DROP TABLE _2_gram;")

    def test_ngram_like_table(self):
        self.connector.create_bigram_table()
        self.connector.insert_ngram(('der', 'linksdenker'), 22)
        self.connector.insert_ngram(('der', 'linksabbieger'), 32)
        result = self.connector.ngram_like_table(('der', 'links'))
        assert result == [('der', 'linksabbieger', 32), (
            'der', 'linksdenker', 22)]
        self.connector.execute_sql("DROP TABLE _2_gram;")
        
    def teardown(self):
        self.connector.close_database()
        if os.path.isfile(self.filename):
            os.remove(self.filename)

if psycopg2_installed:
    class TestPostgresDatabaseConnector():

        def setup(self):
            self.connector = pressagio.dbconnector.PostgresDatabaseConnector("test")
            self.connector.create_database()
            self.connector.open_database()

        def test_create_database(self):
            self.connector.create_database()

        def test_create_ngram_table(self):
            self.connector.create_ngram_table(1)
            result = self.connector.execute_sql(
                "SELECT * FROM information_schema.tables WHERE table_name='_1_gram';")
            assert len(result) == 1
            self.connector.execute_sql("DROP TABLE _1_gram;")

            self.connector.create_ngram_table(2)
            result = self.connector.execute_sql(
                "SELECT * FROM information_schema.tables WHERE table_name='_2_gram';")
            assert len(result) == 1
            self.connector.execute_sql("DROP TABLE _2_gram;")

            self.connector.create_ngram_table(3)
            result = self.connector.execute_sql(
                "SELECT * FROM information_schema.tables WHERE table_name='_3_gram';")
            assert len(result) == 1
            self.connector.execute_sql("DROP TABLE _3_gram;")

        def test_create_unigram_table(self):
            self.connector.create_unigram_table()
            result = self.connector.execute_sql(
                "SELECT * FROM information_schema.tables WHERE table_name='_1_gram';")
            assert len(result) == 1
            self.connector.execute_sql("DROP TABLE _1_gram;")

        def test_create_bigram_table(self):
            self.connector.create_bigram_table()
            result = self.connector.execute_sql(
                "SELECT * FROM information_schema.tables WHERE table_name='_2_gram';")
            assert len(result) == 1
            self.connector.execute_sql("DROP TABLE _2_gram;")

        def test_create_trigram_table(self):
            self.connector.create_trigram_table()
            result = self.connector.execute_sql(
                "SELECT * FROM information_schema.tables WHERE table_name='_3_gram';")
            assert len(result) == 1
            self.connector.execute_sql("DROP TABLE _3_gram;")

        def test_insert_ngram(self):
            self.connector.create_bigram_table()
            self.connector.insert_ngram(('der', 'linksdenker'), 22)
            result = self.connector.execute_sql("SELECT * FROM _2_gram")
            assert result == [('der', 'linksdenker', 22)]
            self.connector.execute_sql("DROP TABLE _2_gram;")

        def test_update_ngram(self):
            self.connector.create_bigram_table()

            # Insert
            self.connector.insert_ngram(('der', 'linksdenker'), 22)
            result = self.connector.execute_sql("SELECT * FROM _2_gram")
            assert result == [('der', 'linksdenker', 22)]

            # Update
            self.connector.update_ngram(('der', 'linksdenker'), 44)
            result = self.connector.execute_sql("SELECT * FROM _2_gram")
            assert result == [('der', 'linksdenker', 44)]

            self.connector.execute_sql("DROP TABLE _2_gram;")

        def test_ngram_count(self):
            self.connector.create_bigram_table()
            self.connector.insert_ngram(('der', 'linksdenker'), 22)
            result = self.connector.ngram_count(('der', 'linksdenker'))
            assert result == 22
            self.connector.execute_sql("DROP TABLE _2_gram;")

        def test_ngram_like_table(self):
            self.connector.create_bigram_table()
            self.connector.insert_ngram(('der', 'linksdenker'), 22)
            self.connector.insert_ngram(('der', 'linksabbieger'), 32)
            result = self.connector.ngram_like_table(('der', 'links'))
            assert result == [('der', 'linksabbieger', 32), (
                'der', 'linksdenker', 22)]
            self.connector.execute_sql("DROP TABLE _2_gram;")

            # testing lowercase mode
            self.connector.lowercase = True
            self.connector.close_database()
            self.connector.reset_database()
            self.connector.open_database()
            self.connector.create_bigram_table()
            self.connector.insert_ngram(('Der', 'Linksdenker'), 22)
            self.connector.insert_ngram(('Der', 'Linksabbieger'), 32)
            result = self.connector.ngram_like_table(('der', 'links'))
            assert result == [('Der', 'Linksabbieger', 32), (
                'Der', 'Linksdenker', 22)]
            self.connector.execute_sql("DROP TABLE _2_gram;")

            # testing normalize mode
            self.connector.normalize = True
            self.connector.close_database()
            self.connector.reset_database()
            self.connector.open_database()
            self.connector.create_bigram_table()
            self.connector.insert_ngram(('Der', 'Lünksdenker'), 22)
            self.connector.insert_ngram(('Der', 'Lünksabbieger'), 32)
            result = self.connector.ngram_like_table(('der', 'lunks'))
            assert result == [('Der', 'Lünksabbieger', 32), (
                'Der', 'Lünksdenker', 22)]
            self.connector.execute_sql("DROP TABLE _2_gram;")

            self.connector.normalize = False
            self.connector.lowercase = False

        def teardown(self):
                self.connector.close_database()
                con = psycopg2.connect(database="postgres", user="postgres")
                con.set_isolation_level(
                        psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                c = con.cursor()
                c.execute("DROP DATABASE test;")
                con.close()
