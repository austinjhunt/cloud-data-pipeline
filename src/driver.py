""" Driver Module, Controls Execution of Project """
import argparse
import os
import json
import logging
from lib.producer import Producer
from lib.consumer import Consumer

class Driver:

    def __init__(self,verbose=False, cloud_platform='', bootstrap_server=''):
        self.setup_logging(verbose)
        self.consumer_host = None
        self.cloud_platform = cloud_platform
        ## PUBLIC_IP_ADDRESS:PORT_NUMBER
        self.bootstrap_server = bootstrap_server
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
        )
        if save_data:
            self.consumer.connect_couchdb()
        self.consumer.consume(save_data=save_data)

    def run_producer(self,topic='stock-market-data', producer_alias="Producer 1", read_data_from_file=None,
        batch_size=None, stock_symbol="AMZN", sleep_interval=1, verbose=False,num_messages=100):
        """ Method to drive a Kafka Producer process (run this from a local VM in VirtualBox) """
        self.info("Running Kafka Producer...")
        if read_data_from_file:
            # use file (already validated), not in memory custom data
            self.producer = Producer(
                bootstrap_server=self.bootstrap_server,
                producer_alias=producer_alias,
                sleep_interval=sleep_interval,
                verbose=verbose,
                read_data_from_file=read_data_from_file,
                batch_size=batch_size
            )
        else:
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
                    # Need to get bootstrap server from json config
                    self.bootstrap_server = cloud_hosts[0]['public']

            except Exception as e:
                self.error(e)


parser = argparse.ArgumentParser(
    description='pass arguments to run the driver for the project'
)
parser.add_argument('--cloud_platform', default='', choices=['chameleon','aws','gcp'], help='indicate which cloud platform to use')

# Pass these two if not using --cloud_platform
parser.add_argument('-b','--bootstrap_server', type=str, default='', help=(
'provide the PUBLIC_IP:PORT_NUMBER of the Kafka bootstrap server '
'(alternative to --cloud_platform, which pulls bootstrap '
'address from static config file)')
)

parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
parser.add_argument('-t', '--topic',
    help='topic to produce (if running producer with -p) or consume (if running consumer with -c)',
    type=str,required=True)

parser.add_argument('-p', '--run_producer', help='whether to run producer', action='store_true')
parser.add_argument('-pa', '--producer_alias', default='Producer 1',
    help='WHEN RUNNING PRODUCER WITH -p|--producer, friendly alias/name of producer', type=str)
parser.add_argument('-n', '--num_messages', type=int, default=100, help='number of messages to produce')
parser.add_argument('-s', '--sleep_interval', default=1, type=int,
    help='WHEN RUNNING PRODUCER WITH -p|--producer, number of seconds to sleep between each message sent')
parser.add_argument('-ss', '--stock_symbol', default='AMZN', help=(
    'WHEN RUNNING PRODUCER WITH -p|--producer, stock symbol to produce data for'), type=str)
parser.add_argument('-r', '--read_data_from_file', help=(
    'WHEN RUNNING PRODUCER WITH -p|--producer, use -r CSV_FILENAME to tell the producer '
    'to read data from a CSV file instead of producing its '
    'own custom data; must be a valid .csv file path on your machine'
    ), type=str)
parser.add_argument('-b', '--batch_size', help=(
    'WHEN RUNNING PRODUCER WITH -p|--producer AND -r|--read_data_from_file CSV_FILENAME, use --batch_size '
    'to tell producer how many records of the CSV to include in each message; REQUIRED'
    ), type=int)

parser.add_argument('-c', '--run_consumer', help='whether to run consumer', action='store_true')
parser.add_argument('-d', '--dump', help='whether consumer should dump data/save to couchdb, only run with -c', action='store_true')



args = parser.parse_args()
if args.cloud_platform == '' and args.bootstrap_server == '':
    # If not providing
    raise Exception('You need to pass one of --cloud_platform PLATFORM or --bootstrap_server PUBLIC_IP')

elif args.cloud_platform != '':
    driver = Driver(
        verbose=args.verbose,
        cloud_platform=args.cloud_platform
        )

elif args.bootstrap_server != '':
    driver = Driver(
        verbose=args.verbose,
        bootstrap_server=args.bootstrap_server
        )

import sys
# Print the full command that was used to invoke driver:
driver.debug(
    f'Command used: {" ".join(sys.argv[:])}'
)

if args.run_producer:
    if args.read_data_from_file:
        if not args.batch_size:
            raise Exception(
                'when using -r|--read_data_from_file, you MUST include '
                '-b|--batch_size to tell producer how many records of '
                'the CSV to include in each message')
        # Try to read the file provided ; throw error if it fails
        try:
            driver.info('Using provided data file instead of custom producer data in memory')
            f = open(args.read_data_from_file,'r')
            driver.debug(f'File {args.read_data_from_file} has {len(f.readlines)} lines')
            f.close()
            driver.run_producer(
                topic=args.topic,
                producer_alias=args.producer_alias ,
                read_data_from_file=args.read_data_from_file,
                batch_size=args.batch_size,
                sleep_interval=args.sleep_interval,
                verbose=args.verbose
            )
        except Exception as e:
            driver.error(e)
            sys.exit(1)
    else:
        driver.info('Using custom producer data (in memory), not a data file')
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
