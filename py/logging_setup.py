import os
import json
import logging.config

def setup(
    default_path='./config/logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        print "value"
        path = value
    if os.path.exists(path):
        print "path exists"
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        print "path does not exist"
        logging.basicConfig(level=default_level)