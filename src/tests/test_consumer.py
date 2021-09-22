from src.lib.consumer import Consumer
from unittest import TestCase
import os
import json

# Test runs against chameleon cloud platform hosts. Change dictionary key
# to aws or gcp to test against another platform.
class TestConsumer(TestCase):
    def setUp(self):
        ## Set up the bootstrap server using config.json
        config_file = open(os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)), 'config.json'))
        config = json.load(config_file)
        self.bootstrap_server = config['cloud_hosts']['chameleon'][0]['public']
        config_file.close()

    def test_connection(self):
        success = False
        try:
            consumer = Consumer(
                verbose=True,
                bootstrap_server=self.bootstrap_server,
                topics=['stock-market-data'])
            success = True
        except Exception as e:
            print(e)
            success = False
        assert success