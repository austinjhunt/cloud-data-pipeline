
# Created: Sept 11, 2021
#
# Purpose:
#
#    Demonstrate the use of Kafka Python streaming APIs.
#    In this example, we use the "top" command and use it as producer of events for
#    Kafka. The consumer can be another Python program that reads and dumps the
#    information into a database OR just keeps displaying the incoming events on the
#    command line consumer (or consumers)
#

import json
import time
import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError
import yfinance
import logging

# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs


class Producer:
    def __init__(self, bootstrap_server="localhost", producer_alias="Producer1",
        stock_symbol="AMZN", sleep_interval=1, verbose=False):
        # Host to contact to bootstrap initial cluster metadata.
        # Needs to have at least one broker that will respond to a Metadata API Request.
        self.producer_alias = producer_alias
        self.stock_symbol = stock_symbol
        self.sleep_interval = sleep_interval
        self.setup_logging(verbose=verbose)
        self.info(
            f'Creating producer with bootstrap_server={bootstrap_server}, '
            f'producer_alias={producer_alias},sleep_interval={sleep_interval}, '
            f'stock_symbol={stock_symbol}')
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=f'{bootstrap_server}', # IP_ADDRESS:PORT
            api_version=(0,10,1),
            request_timeout_ms=5000,
            # wait for leader to write to log; this controls the durability of records that are sent.
            acks=1)

    def setup_logging(self, verbose):
        """ set up self.logger for producer logging """
        self.logger = logging.getLogger('producer')
        formatter = logging.Formatter('%(prefix)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.prefix = {'prefix': self.producer_alias}
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

    def produce(self, num_messages=100, topic='stock-market-data'):
        """ Produce data / send data into pipeline <count> times
        Args:
        - count (int): number of times to send data """
        self.info(f'Beginning to produce data')
        for i in range(num_messages):
            self.debug(f'Producing message {i}, stock_symbol={self.stock_symbol}')
            message = {
                'timestamp': datetime.datetime.now().isoformat(),
                'stock_symbol': self.stock_symbol,
                'current_share_price': yfinance.Ticker(self.stock_symbol).info['currentPrice'],
                'producer_alias': self.producer_alias,
                'message_index': i
            }
            message = bytes(json.dumps(message), 'ascii')
            try:
                self.kafka_producer.send(topic=topic, value=message)
                self.kafka_producer.flush() # try to empty sending buffer
            except KafkaTimeoutError as e:
                self.error(f'Timeout error when sending message: {str(e)}')
            except Exception as e:
                self.error(f'Exception when sending message: {str(e)}')
            time.sleep(self.sleep_interval)
        self.kafka_producer.close ()
