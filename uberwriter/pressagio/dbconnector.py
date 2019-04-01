# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2001-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE

"""
Classes to connect to databases.

"""

from __future__ import absolute_import, unicode_literals

import abc
import sqlite3
import time
import re
import regex

try:
    import psycopg2
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
except ImportError:
    pass

re_escape_singlequote = re.compile("'")


def _sqlite3_regex(expr, item):
    return (not (not regex.search(expr, item)))


class DatabaseConnector(object):
    """
    Base class for all database connectors.

    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, dbname, cardinality = 1):
        """
        Constructor of the base class DababaseConnector.

        Parameters
        ----------
        dbname : str
            path to the database file or database name
        cardinality : int
            default cardinality for n-grams

        """
        print("asjdas jdlkasj ljsa kdj lsakdj lk")
        self.cardinality = cardinality
        self.dbname = dbname
        self.lowercase = False
        self.normalize = False

    def create_ngram_table(self, cardinality):
        """
        Creates a table for n-gram of a give cardinality. The table name is
        constructed from this parameter, for example for cardinality `2` there
        will be a table `_2_gram` created.

        Parameters
        ----------
        cardinality : int
            The cardinality to create a table for.

        """
        query = "CREATE TABLE IF NOT EXISTS _{0}_gram (".format(cardinality)
        unique = ""
        for i in reversed(range(cardinality)):
            if i != 0:
                unique += "word_{0}, ".format(i)
                query += "word_{0} TEXT, ".format(i)
            else:
                unique += "word"
                query += "word TEXT, count INTEGER, UNIQUE({0}) );".format(
                    unique)

        self.execute_sql(query)

    def delete_ngram_table(self, cardinality):
        """
        Deletes the table for n-gram of a give cardinality. The table name is
        constructed from this parameter, for example for cardinality `2` there
        will be a table `_2_gram` deleted.

        Parameters
        ----------
        cardinality : int
            The cardinality of the table to delete.

        """

        query = "DROP TABLE IF EXISTS _{0}_gram;".format(cardinality)
        self.execute_sql(query)

    def create_index(self, cardinality):
        """
        Create an index for the table with the given cardinality.

        Parameters
        ----------
        cardinality : int
            The cardinality to create a index for.

        """
        for i in reversed(range(cardinality)):
            if i != 0:
                query = "CREATE INDEX idx_{0}_gram_{1} ON _{0}_gram(word_{1});".format(cardinality, i)
                self.execute_sql(query)

    def delete_index(self, cardinality):
        """
        Delete index for the table with the given cardinality.

        Parameters
        ----------
        cardinality : int
            The cardinality of the index to delete.

        """
        for i in reversed(range(cardinality)):
            if i != 0:
                query = "DROP INDEX IF EXISTS idx_{0}_gram_{1};".format(
                    cardinality, i)
                self.execute_sql(query)

    def create_unigram_table(self):
        """
        Creates a table for n-grams of cardinality 1.

        """
        self.create_ngram_table(1)

    def create_bigram_table(self):
        """
        Creates a table for n-grams of cardinality 2.

        """
        self.create_ngram_table(2)

    def create_trigram_table(self):
        """
        Creates a table for n-grams of cardinality 3.

        """
        self.create_ngram_table(3)


    def ngrams(self, with_counts=False):
        """
        Returns all ngrams that are in the table.

        Parameters
        ----------
        None

        Returns
        -------
        ngrams : generator
            A generator for ngram tuples.

        """
        query = "SELECT "
        for i in reversed(range(self.cardinality)):
            if i != 0:
                query += "word_{0}, ".format(i)
            elif i == 0:
                query += "word"

        if with_counts:
            query += ", count"

        query += " FROM _{0}_gram;".format(self.cardinality)
        print(query)
        result = self.execute_sql(query)
        for row in result:
            yield tuple(row)

    def unigram_counts_sum(self):
        query = "SELECT SUM(count) from _1_gram;"
        result = self.execute_sql(query)
        print(result, query)
        return self._extract_first_integer(result)

    def ngram_count(self, ngram):
        """
        Gets the count for a given ngram from the database.

        Parameters
        ----------
        ngram : iterable of str
            A list, set or tuple of strings.

        Returns
        -------
        count : int
            The count of the ngram.

        """
        query = "SELECT count FROM _{0}_gram".format(len(ngram))
        query += self._build_where_clause(ngram)
        query += ";"

        result = self.execute_sql(query)

        return self._extract_first_integer(result)

    def ngram_like_table(self, ngram, limit = -1):
        print("NGRAM LIKE TABLE!\n\n\n")
        query = "SELECT {0} FROM _{1}_gram {2} ORDER BY count DESC".format(
            self._build_select_like_clause(len(ngram)), len(ngram),
            self._build_where_like_clause(ngram))
        print(query)
        if limit < 0:
            query += ";"
        else:
            query += " LIMIT {0};".format(limit)

        return self.execute_sql(query)

    def ngram_like_table_filtered(self, ngram, filter, limit = -1):
        pass

    def increment_ngram_count(self, ngram):
        pass

    def insert_ngram(self, ngram, count):
        """
        Inserts a given n-gram with count into the database.

        Parameters
        ----------
        ngram : iterable of str
            A list, set or tuple of strings.
        count : int
            The count for the given n-gram.

        """
        query = "INSERT INTO _{0}_gram {1};".format(len(ngram),
            self._build_values_clause(ngram, count))
        self.execute_sql(query)

    def update_ngram(self, ngram, count):
        """
        Updates a given ngram in the database. The ngram has to be in the
        database, otherwise this method will stop with an error.

        Parameters
        ----------
        ngram : iterable of str
            A list, set or tuple of strings.
        count : int
            The count for the given n-gram.

        """
        query = "UPDATE _{0}_gram SET count = {1}".format(len(ngram), count)
        query += self._build_where_clause(ngram)
        query += ";"
        self.execute_sql(query)

    def remove_ngram(self, ngram):
        """
        Removes a given ngram from the databae. The ngram has to be in the
        database, otherwise this method will stop with an error.

        Parameters
        ----------
        ngram : iterable of str
            A list, set or tuple of strings.

        """
        query = "DELETE FROM _{0}_gram".format(len(ngram))
        query += self._build_where_clause(ngram)
        query += ";"
        self.execute_sql(query)

    def open_database(self):
        raise NotImplementedError("Method must be implemented")

    def close_database(self):
        raise NotImplementedError("Method must be implemented")

    def execute_sql(self):
        raise NotImplementedError("Method must be implemented")

    ############################################### Private methods

    def _build_values_clause(self, ngram, count):
        ngram_escaped = []
        for n in ngram:
            ngram_escaped.append(re_escape_singlequote.sub("''", n))

        values_clause = "VALUES('"
        values_clause += "', '".join(ngram_escaped)
        values_clause += "', {0})".format(count)
        return values_clause



    def _build_where_clause(self, ngram):
        where_clause = " WHERE"
        for i in range(len(ngram)):
            n = re_escape_singlequote.sub("''", ngram[i])
            if i < (len(ngram) - 1):
                where_clause += " word_{0} = '{1}' AND".format(
                    len(ngram) - i - 1, n)
            else:
                pattern = '(?:^%s){e<=%d}' % (n, 2)
                where_clause += " word = '{0}'".format(n)
                print(where_clause)
        return where_clause

    def _build_select_like_clause(self, cardinality):
        result = ""
        for i in reversed(range(cardinality)):
            if i != 0:
                result += "word_{0}, ". format(i)
            else:
                result += "word, count"
        return result

    def _build_where_like_clause(self, ngram):
        where_clause = " WHERE"
        for i in range(len(ngram)):
            if i < (len(ngram) - 1):
                where_clause += " word_{0} = '{1}' AND".format(
                    len(ngram) - i - 1, ngram[i])
            else:
                pattern = '(?:%s){e<=%d}' % (ngram[-1], 0)
                where_clause += " (word regexp '%s')" % pattern
        return where_clause

    def _extract_first_integer(self, table):
        count = 0
        if len(table) > 0:
            if len(table[0]) > 0:
                count = int(table[0][0])

        if not count > 0:
            count = 0
        return count


class SqliteDatabaseConnector(DatabaseConnector):
    """
    Database connector for sqlite databases.

    """

    def __init__(self, dbname, cardinality = 1):
        """
        Constructor for the sqlite database connector.

        Parameters
        ----------
        dbname : str
            path to the database file
        cardinality : int
            default cardinality for n-grams

        """
        DatabaseConnector.__init__(self, dbname, cardinality)
        self.con = None
        self.open_database()

    def commit(self):
        """
        Sends a commit to the database.

        """
        self.con.commit()
        
    def open_database(self):
        """
        Opens the sqlite database.

        """
        self.con = sqlite3.connect(self.dbname)
        self.con.create_function("regexp", 2, _sqlite3_regex)


    def close_database(self):
        """
        Closes the sqlite database.

        """
        if self.con:
            self.con.close()

    def execute_sql(self, query):
        """
        Executes a given query string on an open sqlite database.

        """
        c = self.con.cursor()
        c.execute(query)
        result = c.fetchall()
        return result


class PostgresDatabaseConnector(DatabaseConnector):
    """
    Database connector for postgres databases.

    """

    def __init__(self, dbname, cardinality = 1, host = "localhost", port = 5432,
            user = "postgres", password = None, connection = None):
        """
        Constructor for the postgres database connector.

        Parameters
        ----------
        dbname : str
            the database name
        cardinality : int
            default cardinality for n-grams
        host : str
            hostname of the postgres database
        port : int
            port number of the postgres database
        user : str
            user name for the postgres database
        password: str
            user password for the postgres database
        connection : connection
            an open database connection

        """
        DatabaseConnector.__init__(self, dbname, cardinality)
        self.con = connection
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def create_database(self):
        """
        Creates an empty database if not exists.
        
        """
        if not self._database_exists():
            con = psycopg2.connect(host=self.host, database="postgres",
                user=self.user, password=self.password, port=self.port)
            con.set_isolation_level(
                psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            query = "CREATE DATABASE {0};".format(self.dbname)
            c = con.cursor()
            c.execute(query)            
            con.close()


            if self.normalize:
                self.open_database()
                query = "CREATE EXTENSION IF NOT EXISTS \"plperlu\";"
                self.execute_sql(query)
    #            query = """CREATE OR REPLACE FUNCTION normalize(str text)
    #RETURNS text
    #AS $$
    #import unicodedata
    #return ''.join(c for c in unicodedata.normalize('NFKD', str)
    #if unicodedata.category(c) != 'Mn')
    #$$ LANGUAGE plpython3u IMMUTABLE;"""
    #             query = """CREATE OR REPLACE FUNCTION normalize(mystr text)
    #   RETURNS text
    # AS $$
    #     from unidecode import unidecode
    #     return unidecode(mystr.decode("utf-8"))
    # $$ LANGUAGE plpythonu IMMUTABLE;"""
                query = """CREATE OR REPLACE FUNCTION normalize(text)
      RETURNS text
    AS $$
        use Text::Unidecode;
        return unidecode(shift);
    $$ LANGUAGE plperlu IMMUTABLE;"""
                self.execute_sql(query)
                self.commit()
                self.close_database()


    def reset_database(self):
        """
        Re-create an empty database.

        """
        if self._database_exists():
            con = psycopg2.connect(host=self.host, database="postgres",
                user=self.user, password=self.password, port=self.port)
            con.set_isolation_level(
                psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            query = "DROP DATABASE {0};".format(self.dbname)
            c = con.cursor()
            c.execute(query)
            con.close()
        self.create_database()

    def create_index(self, cardinality):
        """
        Create an index for the table with the given cardinality.

        Parameters
        ----------
        cardinality : int
            The cardinality to create a index for.

        """
        DatabaseConnector.create_index(self, cardinality)
        query = "CREATE INDEX idx_{0}_gram_varchar ON _{0}_gram(word varchar_pattern_ops);".format(cardinality)
        self.execute_sql(query)

        if self.lowercase:

            for i in reversed(range(cardinality)):
                if i != 0:
                    query = "CREATE INDEX idx_{0}_gram_{1}_lower ON _{0}_gram(LOWER(word_{1}));".format(cardinality, i)
                    self.execute_sql(query)

            if self.normalize:

                query = "CREATE INDEX idx_{0}_gram_lower_normalized_varchar ON _{0}_gram(NORMALIZE(LOWER(word)) varchar_pattern_ops);".format(cardinality)
                self.execute_sql(query)

            else:

                query = "CREATE INDEX idx_{0}_gram_lower_varchar ON _{0}_gram(LOWER(word) varchar_pattern_ops);".format(cardinality)
                self.execute_sql(query)

        elif self.normalize:

            query = "CREATE INDEX idx_{0}_gram_normalized_varchar ON _{0}_gram(NORMALIZE(word) varchar_pattern_ops);".format(cardinality)
            self.execute_sql(query)

    def delete_index(self, cardinality):
        """
        Delete index for the table with the given cardinality.

        Parameters
        ----------
        cardinality : int
            The cardinality of the index to delete.

        """
        DatabaseConnector.delete_index(self, cardinality)

        query = "DROP INDEX IF EXISTS idx_{0}_gram_varchar;".format(cardinality)
        self.execute_sql(query)
        query = "DROP INDEX IF EXISTS idx_{0}_gram_normalized_varchar;".format(
            cardinality)
        self.execute_sql(query)
        query = "DROP INDEX IF EXISTS idx_{0}_gram_lower_varchar;".format(
            cardinality)
        self.execute_sql(query)
        query = "DROP INDEX IF EXISTS idx_{0}_gram_lower_normalized_varchar;".\
            format(cardinality)
        self.execute_sql(query)
        for i in reversed(range(cardinality)):
            if i != 0:
                query = "DROP INDEX IF EXISTS idx_{0}_gram_{1}_lower;".format(
                    cardinality, i)
                self.execute_sql(query)

    def commit(self):
        """
        Sends a commit to the database.

        """
        self.con.commit()
        
    def open_database(self):
        """
        Opens the sqlite database.

        """
        if not self.con:
            try:
                self.con = psycopg2.connect(host=self.host,
                    database=self.dbname, user=self.user,
                    password=self.password, port=self.port)
            except psycopg2.Error as e:
                print("Error while opening database:")
                print(e.pgerror)

    def close_database(self):
        """
        Closes the sqlite database.

        """
        if self.con:
            self.con.close()
            self.con = None

    def execute_sql(self, query):
        """
        Executes a given query string on an open postgres database.

        """
        c = self.con.cursor()
        c.execute(query)
        result = []
        if c.rowcount > 0:
            try:
                result = c.fetchall()
            except psycopg2.ProgrammingError:
                pass
        return result


    ############################################### Private methods

    def _database_exists(self):
        """
        Check if the database exists.

        """
        con = psycopg2.connect(host=self.host, database="postgres",
            user=self.user, password=self.password, port=self.port)
        query_check = "select datname from pg_catalog.pg_database"
        query_check += " where datname = '{0}';".format(self.dbname)
        c = con.cursor()
        c.execute(query_check)
        result = c.fetchall()
        if len(result) > 0:
            return True
        return False

    def _build_where_like_clause(self, ngram):
        where_clause = " WHERE"
        for i in range(len(ngram)):
            if i < (len(ngram) - 1):
                if self.lowercase:
                    where_clause += " LOWER(word_{0}) = LOWER('{1}') AND".format(
                            len(ngram) - i - 1, ngram[i])
                else:
                    where_clause += " word_{0} = '{1}' AND".format(
                        len(ngram) - i - 1, ngram[i])
            else:
                if ngram[-1] != "":
                    if self.lowercase:
                        if self. normalize:
                            where_clause += " NORMALIZE(LOWER(word)) LIKE NORMALIZE(LOWER('{0}%'))".format(ngram[-1])
                        else:
                            where_clause += " LOWER(word) LIKE LOWER('{0}%')".format(ngram[-1])
                    elif self.normalize:
                        where_clause += " NORMALIZE(word) LIKE NORMALIZE('{0}%')".format(ngram[-1])
                    else:
                        where_clause += " word LIKE '{0}%'".format(ngram[-1])
                else:
                    # remove the " AND"
                    where_clause = where_clause[:-4]
        
        return where_clause


#################################################### Functions

def insert_ngram_map_sqlite(ngram_map, ngram_size, outfile, append=False,
    create_index=False):
    sql = SqliteDatabaseConnector(outfile, ngram_size)
    sql.create_ngram_table(ngram_size)

    for ngram, count in ngram_map.items():
        if append:
            old_count = sql.ngram_count(ngram)
            if old_count > 0:
                sql.update_ngram(ngram, old_count + count)
            else:
                sql.insert_ngram(ngram, count)
        else:
            sql.insert_ngram(ngram, count)

    sql.commit()

    if create_index and not append:
        sql.create_index(ngram_size)

    sql.close_database()


def insert_ngram_map_postgres(ngram_map, ngram_size, dbname, append=False,
    create_index=False, host = "localhost", port = 5432, user = "postgres",
    password = None, lowercase = False, normalize = False):
    sql = PostgresDatabaseConnector(dbname, ngram_size, host, port, user,
        password)
    sql.lowercase = lowercase
    sql.normalize = normalize
    sql.create_database()
    sql.open_database()
    if not append:
        sql.delete_index(ngram_size)
        sql.delete_ngram_table(ngram_size)
    sql.create_ngram_table(ngram_size)

    for ngram, count in ngram_map.items():
        if append:
            old_count = sql.ngram_count(ngram)
            if old_count > 0:
                sql.update_ngram(ngram, old_count + count)
            else:
                sql.insert_ngram(ngram, count)
        else:
            sql.insert_ngram(ngram, count)

    sql.commit()

    if create_index and not append:
        sql.create_index(ngram_size)

    sql.commit()

    sql.close_database()

def _filter_ngrams(sql, dictionary):
    for ngram in sql.ngrams():
        delete_ngram = False
        for word in ngram:
            if not word in dictionary:
                delete_ngram = True
        if delete_ngram:
            sql.remove_ngram(ngram)


def filter_ngrams_sqlite(dictionary, ngram_size, outfile):
    sql = SqliteDatabaseConnector(outfile, ngram_size)
    _filter_ngrams(sql, dictionary)
    sql.commit()
    sql.close_database()

def filter_ngrams_postgres(dictionary, ngram_size, dbname, host = "localhost",
        port = 5432, user = "postgres", password = None):
    sql = PostgresDatabaseConnector(dbname, ngram_size, host, port, user,
        password)
    sql.open_database()

    _filter_ngrams(sql, dictionary)

    sql.commit()
    sql.close_database()