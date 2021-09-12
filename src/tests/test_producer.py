from src.lib.producer import Producer
from unittest import TestCase
import os
import json

class TestProducer(TestCase):
    def setUp(self):
        ## Set up the bootstrap server using config.json
        config_file = open(os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)), 'config.json'))
        config = json.load(config_file)
        self.bootstrap_server = config['cloud_hosts'][0]['public']
        config_file.close()

    def test_connection(self):
        success = False
        try:
            consumer = Producer(
                bootstrap_server=self.bootstrap_server,
                producer_alias='Producer Test',
                stock_symbol='AMZN',
                sleep_interval=1,
                verbose=True
            )
            success = True
        except Exception as e:
            print(e)
        assert success