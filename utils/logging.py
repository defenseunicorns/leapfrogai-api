import logging
from datetime import datetime
import sys

def logging_init():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

def log(msg):
    print(msg)

def now():
    return datetime.now()

def get_elapsed(start_time):
    return datetime.now() - start_time        