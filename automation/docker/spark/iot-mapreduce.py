import couchdb
import argparse
import logging
import time
import json
import couchdb
import os
from pyspark.sql import SparkSession, Row


class IOTSparkMapReducer:
    def __init__(self, verbose=False):
        # Use environment
        self.couchdb_server = os.environ.get(
            'COUCHDB_SERVER', 'localhost:5984')
        self.couchdb_user = os.environ.get('COUCHDB_USER', 'admin')
        self.couchdb_password = os.environ.get('COUCHDB_PASSWORD', '123456')
        self.couchdb_database = os.environ.get('COUCHDB_DATABASE', 'couchie')
        self.setup_logging(verbose=verbose)
        self.debug(
            f"Using DB Info:"
            f"SERVER:{self.couchdb_server}, "
            f"USER: {self.couchdb_user}, "
            f"Password: {self.couchdb_password}, "
            f"DB: {self.couchdb_database}")

        self.connect_couchdb()

    def database_exists(self, database):
        return database in self.couch

    def get_all_data_chunks(self):
        """ Each document in Couchdb stores, under the 'chunk' key, a value that
        is a list of 1000 (or more) recrods from the energy data CSV. This returns a full
        list that aggregates the 'chunk' value of each couchdb record """
        chunks = []
        for doc_id in self.db:
            chunk = self.db.get(doc_id).get('chunk')
            # This chunk contains many sub dicts, each of which represent an energy record from CSV
            for energy_record in chunk:
                chunks.append(energy_record)
        return chunks

    def compute_property_avg_from_chunks(self, chunks=[], property='work'):
        # property can be 'work' or 'load' -> determines whether to
        # filter by property = 0 (work) or 1 (load)
        # id,timestamp,value,property,plug_id,household_id,house_id
        # type of the measurement: 0 for work or 1 for load [boolean]; interested
        # in work for this function
        # Reference: https://stackoverflow.com/questions/29930110/calculating-the-averages-for-each-key-in-a-pairwise-k-v-rdd-in-spark-with-pyth
        filters = {
            'work': '0',
            'load': '1'
        }
        mapped = SparkSession\
            .builder\
            .appName("SmartPlugAvgWorkCalculator")\
            .getOrCreate()\
            .createDataFrame(
                Row(
                    id=int(x[0]),
                    timestamp=x[1],
                    value=float(x[2]),
                    property=int(x[3]),
                    plug_id=int(x[4]),
                    household_id=int(x[5]),
                    house_id=int(x[6])
                ) for x in chunks if x[3] == filters[property]).rdd.map(
                lambda row: (
                    (row.plug_id, row.household_id, row.house_id), row.value
                )
            )
        reduced = mapped.aggregateByKey(
            zeroValue=(0, 0),
            # simultaneously calculate the SUM (the numerator for the
            # average that we want to compute), and COUNT (the
            # denominator for the average that we want to compute):
            seqFunc=lambda a, b: (a[0] + b,    a[1] + 1),
            combFunc=lambda a, b: (a[0] + b[0], a[1] + b[1]))\
            .mapValues(lambda v: v[0]/v[1]).collect()  # divide sum by count
        return reduced

    def connect_couchdb(self):
        # couchdb connection
        self.debug(
            f'Connecting to CouchDB server at: http://{self.couchdb_user}:{self.couchdb_password}@{self.couchdb_server}/"')
        self.couch = couchdb.Server(
            f"http://{self.couchdb_user}:{self.couchdb_password}@{self.couchdb_server}/")
        # create the database if not existing, get the database if already existing
        try:
            self.db = self.couch.create(self.couchdb_database)
            self.debug(
                f"Successfully created new CouchDB database {self.couchdb_database}")
        except:
            self.db = self.couch[self.couchdb_database]
            self.debug(
                f"Successfully connected to existing CouchDB database {self.couchdb_database}")

    def setup_logging(self, verbose):
        """ set up self.logger for producer logging """
        self.logger = logging.getLogger('IOTSparkMapReducer')
        formatter = logging.Formatter('%(prefix)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.prefix = {'prefix': 'IOTSparkMapReducer'}
        self.logger.addHandler(handler)
        self.logger = logging.LoggerAdapter(self.logger, self.prefix)
        if verbose:
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug('Debug mode enabled', extra=self.prefix)
        else:
            self.logger.setLevel(logging.INFO)

    def debug(self, msg):
        self.logger.debug(msg, extra=self.prefix)

    def info(self, msg):
        self.logger.info(msg, extra=self.prefix)

    def error(self, msg):
        self.logger.error(msg, extra=self.prefix)

    def get_all_docs(self):
        return [row for row in self.db]

    def get_db(self):
        return self.db

    def save_list_to_database(self, db_name, lst):
        """ Write a list to CouchDB database """
        try:
            db = self.couch.create(db_name)
            self.debug(
                f"Successfully created new CouchDB database {db_name}")
        except:
            db = self.couch[db_name]
            self.debug(
                f"Successfully connected to existing CouchDB database {db_name}")
        self.debug(f'Preparing to save {len(lst)} items to database')
        fails = 0
        for msg in lst:
            try:
                jsonified_msg = {
                    'plug_id': msg[0][0],
                    'household_id': msg[0][1],
                    'house_id': msg[0][2],
                    'value': msg[1]
                }
                db.save(jsonified_msg)
            except Exception as e:
                self.error(e)
                fails += 1
        self.debug("Saving completed")
        self.debug(f"Failed to save {fails} items")

    def validate(self):
        """ used only for testing/development; Count number of unique (row.plug_id, row.household_id, row.house_id) tuples """
        d = {}
        num_chunks = 0
        potential = 0
        count_11_0_0 = 0
        total_11_0_0 = 0
        for doc_id in self.db:
            chunk = self.db.get(doc_id).get('chunk')
            num_chunks += 1
            for record in chunk:
                potential += 1
                # id, timestamp, value, property plug_id,household_id,house_id
                _tuple = (record[-3], record[-2], record[-1])
                if _tuple == ("11", "0", "0") and record[3] == "0":
                    print(f'Adding {record[2]}')
                    total_11_0_0 += float(record[2])
                    count_11_0_0 += 1
                if _tuple not in d:
                    d[_tuple] = record[2]
                else:
                    d[_tuple] += record[2]
        print(f"Avg for 11 0 0 = {total_11_0_0 / count_11_0_0}")
        print(f'Keys: {len(d.keys())}')
        print(f'Num chunks: {num_chunks}')
        print(f'Potential Number of Tuples: {potential} ')
        return d


if __name__ == "__main__":
    master = IOTSparkMapReducer(verbose=True)
    # wait for the signal that the database is ready to be read from
    # the signal comes in the form of a database called "complete" added to the couchdb server.
    # add this manually once all data is added
    while not master.database_exists("complete"):
        master.debug("waiting on 'complete' database creation to signal Spark Analysis")
        time.sleep(3)

    master.info("CouchDB Server is now ready, beginning Spark Analysis")
    # Use mapreduce to get the average values for both properties 'work' and 'load'
    avg_work = master.compute_property_avg_from_chunks(
        chunks=master.get_all_data_chunks(),
        property='work'
    )
    avg_load = master.compute_property_avg_from_chunks(
        chunks=master.get_all_data_chunks(),
        property='load'
    )
    # Save results to couchdb
    master.save_list_to_database('avg_work', avg_work)
    master.save_list_to_database('avg_load', avg_load)
