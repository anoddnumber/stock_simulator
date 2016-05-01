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
        path = value
        print "setting the path to value of environment variable env_key: " + str(env_key)
        print "path: " + str(path)

    if not os.path.exists(log_dir):
        print "path of log directory does not exist, automatically creating the directories"
        print "path created: " + str(log_dir)
        os.makedirs(log_dir)

    if os.path.exists(path):
        print "path to logging config exists"
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        print "path does not exist"
        logging.basicConfig(level=level) #prints to standard out