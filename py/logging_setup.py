import os
import json
import logging.config

def setup(path='./config/logging.json', level=logging.INFO, env_key='LOG_CFG',
          log_dir='./logs'):
    """
        Setup logging configuration
    """
    value = os.getenv(env_key, None)
    if value:
        print "value"
        path = value

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if os.path.exists(path):
        print "path to logging config exists"
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        print "path does not exist"
        logging.basicConfig(level=level) #prints to standard out