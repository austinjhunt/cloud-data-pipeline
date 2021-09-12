from kafka import KafkaConsumer
import logging
import json

class Consumer:
    def __init__(self,verbose=False, bootstrap_server='localhost', topics=['stock-market-data']):
        self.setup_logging(verbose=verbose)
        self.kafka_consumer = KafkaConsumer(
            bootstrap_servers=f'{bootstrap_server}:9092'
        )
        self.info(
            f'Creating consumer with bootstrap_server={bootstrap_server}:9092, topics={topics}')
        self.kafka_consumer.subscribe(topics=topics)

    def consume(self):
        """ Method to run consumption of messages until messages no longer arrive """
        self.info('Beginning consumption')
        for msg in self.kafka_consumer:
            self.info(
                f'Receiving message: {json.loads(str(msg.value, "ascii"))}'
            )
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




