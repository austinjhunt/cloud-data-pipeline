""" Driver Module, Controls Execution of Project """
import argparse
import os
import json
import logging
from lib.producer import Producer
from lib.consumer import Consumer

class Driver:

    def __init__(self,verbose=False, cloud_platform='', bootstrap_server='', data_sink_server=''):
        self.setup_logging(verbose)
        self.consumer_host = None
        self.couchdb_server = None
        self.couchdb_user = None
        self.couchdb_password = None
        self.cloud_platform = cloud_platform
        self.bootstrap_server = bootstrap_server
        self.data_sink_server = data_sink_server
        self.configure()

    def run_consumer(self, topic='stock-market-data', verbose=False, save_data=False):
        """ Method to drive a Kafka Consumer process (run this from a Cloud VM where Apache Kafka is installed)
        If save_data, save into couchdb (run this from a Cloud VM where both Apache Kafka and Apache CouchDB are installed
        """
        self.info("Running Kafka Consumer...")
        self.consumer = Consumer(
            verbose=verbose,
            bootstrap_server=self.bootstrap_server,
            topics=[topic],
            couchdb_server = self.couchdb_server,
            couchdb_user = self.couchdb_user,
            couchdb_password = self.couchdb_password,
            couchdb_database = self.couchdb_database
        )
        if save_data:
            self.consumer.connect_couchdb()
        self.consumer.consume(save_data=save_data)

    def run_producer(self,topic='stock-market-data', producer_alias="Producer 1",stock_symbol="AMZN",
        sleep_interval=1, verbose=False,num_messages=100):
        """ Method to drive a Kafka Producer process (run this from a local VM in VirtualBox) """
        self.info("Running Kafka Producer...")
        self.producer = Producer(
            bootstrap_server=self.bootstrap_server,
            producer_alias=producer_alias,
            stock_symbol=stock_symbol,
            sleep_interval=sleep_interval,
            verbose=verbose
        )
        self.producer.produce(num_messages=num_messages, topic=topic)

    def setup_logging(self, verbose):
        """ set up self.logger for Driver logging """
        self.logger = logging.getLogger('driver')
        formatter = logging.Formatter('%(prefix)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.prefix = {'prefix': 'DRIVER'}
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

    def configure(self):
        """ Parse configuration file (config.json) """
        self.info("Configuring driver")
        config_file = os.path.join(
            os.path.dirname(__file__),
            'config.json'
        )
        with open(config_file) as f:
            try:
                config = json.load(f)
                if self.cloud_platform:
                    cloud_hosts = config['cloud_hosts'][self.cloud_platform]
                    # Should be 2 VMs.
                    # First will run Kafka Broker, Zookeeper, and Consumer.
                    self.consumer_host = cloud_hosts[0]
                    self.bootstrap_server = self.consumer_host['public']
                    # Second will Run Kafka Broker and CouchDB, functioning as sink.
                    self.data_sink_server = cloud_hosts[1]

                elif self.bootstrap_server:
                    self.consumer_host = self.data_sink_server
                    # bootstrap_server and data_sink_server are already set

                self.debug(f"Consumer host: {self.consumer_host}")
                self.debug(f"Sink Host: {self.data_sink_server}")

                # couch db admin name and password
                couchdb = config['couchdb']
                self.couchdb_server = couchdb['server']
                self.couchdb_user = couchdb['user']
                self.couchdb_password = couchdb['password']
                self.couchdb_database = couchdb['database']

            except Exception as e:
                self.error(e)


parser = argparse.ArgumentParser(
    description='pass arguments to run the driver for the project'
)
parser.add_argument('--cloud_platform', default='', choices=['chameleon','aws','gcp'], help='indicate which cloud platform to use')

# Pass these two if not using --cloud_platform
parser.add_argument('-b','--bootstrap_server', type=str, default='', help=(
'provide the public IP address of the Kafka bootstrap server '
'(alternative to --cloud_platform, which pulls bootstrap '
'address from  static config file)')
)
parser.add_argument('-sink','--data_sink_server', type=str, default='', help=(
'provide the public IP address of the server on which the data sink (CouchDB) will run '
'(alternative to --cloud_platform, which pulls address from static config file)')
)


parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
parser.add_argument('-t', '--topic',
    help='topic to produce (if running producer with -p) or consume (if running consumer with -c)',
    type=str,required=True)
parser.add_argument('-p', '--run_producer', help='whether to run producer', action='store_true')
parser.add_argument('-pa', '--producer_alias', default='Producer 1',
    help='friendly alias/name of producer', type=str)
parser.add_argument('-n', '--num_messages', type=int, default=100, help='number of messages to produce')
parser.add_argument('-s', '--sleep_interval', default=1, type=int,
    help='number of seconds to sleep between each message sent')
parser.add_argument('-ss', '--stock_symbol', default='AMZN', help='stock symbol to produce data for', type=str)

parser.add_argument('-c', '--run_consumer', help='whether to run consumer', action='store_true')
parser.add_argument('-d', '--dump', help='whether consumer should dump data/save to couchdb, only run with -c', action='store_true')


args = parser.parse_args()
if args.cloud_platform == '' and (args.bootstrap_server == '' or args.data_sink_server == ''):
    # If not providing
    raise Exception('You need to pass one of --cloud_platform PLATFORM or (BOTH --bootstrap_server PUBLIC_IP and --data_sink_server PUBLIC_IP)')

elif args.cloud_platform != '':
    driver = Driver(
        verbose=args.verbose,
        cloud_platform=args.cloud_platform
        )

elif args.bootstrap_server != '' and args.data_sink_server != '':
    driver = Driver(
        verbose=args.verbose,
        bootstrap_server=args.bootstrap_server,
        data_sink_server=args.data_sink_server
        )

if args.run_producer:
    driver.run_producer(
        topic=args.topic,
        producer_alias=args.producer_alias ,
        stock_symbol=args.stock_symbol ,
        num_messages=args.num_messages,
        sleep_interval=args.sleep_interval,
        verbose=args.verbose
    )
elif args.run_consumer:
    driver.run_consumer(
        topic=args.topic,
        verbose=args.verbose,
        save_data=args.dump
    )
elif args.run_consumer_couchdb:
    topic = args.topic
    driver.run_consumer_couchdb(
        topic=topic,
        verbose=args.verbose
    )
