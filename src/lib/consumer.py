from kafka import KafkaConsumer
import logging
import json
import couchdb
import os

class Consumer:
    def __init__(self, verbose=False, bootstrap_server='localhost', topics=['stock-market-data']):
        # Use environment
        self.couchdb_server = os.environ.get('COUCHDB_SERVER', 'localhost')
        self.couchdb_user = os.environ.get('COUCHDB_USER', 'admin')
        self.couchdb_password = os.environ.get('COUCHDB_PASSWORD', '123456')
        self.couchdb_database = os.environ.get('COUCHDB_DATABASE', 'couchie')

        self.setup_logging(verbose=verbose)
        self.kafka_consumer = KafkaConsumer(
            bootstrap_servers=f'{bootstrap_server}' # PUBLIC_IP:PORT
        )
        self.info(f'Creating consumer with bootstrap_server={bootstrap_server}, topics={topics}')
        self.kafka_consumer.subscribe(topics=topics)

    def connect_couchdb(self):
        # couchdb connection
        self.debug(f'Connecting to CouchDB server at: http://{self.couchdb_user}:{self.couchdb_password}@{self.couchdb_server}:5984/"')
        self.couch = couchdb.Server(f"http://{self.couchdb_user}:{self.couchdb_password}@{self.couchdb_server}:5984/")
        # create the database if not existing, get the database if already existing
        try:
            self.db = self.couch.create(self.couchdb_database)
            self.debug(f"Successfully created new CouchDB database {self.couchdb_database}")
        except:
            self.db = self.couch[self.couchdb_database]
            self.debug(f"Successfully connected to existing CouchDB database {self.couchdb_database}")

    def consume(self, save_data=False):
        """ Method to run consumption of messages until messages no longer arrive """
        self.info('Beginning consumption')
        for msg in self.kafka_consumer:
            self.info(
                f'Receiving message: {json.loads(str(msg.value, "ascii"))}'
            )
            if save_data:
                self.info(
                    f'Saving to database!'
                )
                msg = json.loads(str(msg.value, "ascii"))
                self.db.save(msg)
        self.kafka_consumer.close()

    def setup_logging(self, verbose):
        """ set up self.logger for producer logging """
        self.logger = logging.getLogger('consumer')
        formatter = logging.Formatter('%(prefix)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.prefix = {'prefix': 'Consumer'}
        self.logger.addHandler(handler)
        self.logger = logging.LoggerAdapter(self.logger, self.prefix )
        if verbose:
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug('Debug mode enabled', extra=self.prefix )
        else:
            self.logger.setLevel(logging.INFO)

    def debug(self, msg):
        self.logger.debug(msg, extra=self.prefix)

    def info(self, msg):
        self.logger.info(msg, extra=self.prefix)

    def error(self, msg):
        self.logger.error(msg, extra=self.prefix)
