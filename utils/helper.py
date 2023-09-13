import os
from typing import List
import yaml
import logging


def helperFunction():
    return "this is the helper"


class Model:
    name: str
    backend: str
    capabilities: List[str]


class Config:
    models: dict[str, Model] = {}

    def __str__(self):
        return f"Models: {self.models}"
        


"""
load_configs loads the config.yaml so that the api knows what endpoints should return. 
TODO: Put more meaningful words here...
"""
def load_configs(directory="", filename="config.yaml"):
    # ENV Variables take precedence over the provided directory for now..
    directory = os.environ.get("LFAI_CONFIG_PATH", directory)
    config_path = os.path.join(directory, filename)
    logging.info(f"Loading config from {config_path}")

    # ensure the config file exists
    if not os.path.exists(config_path):
        logging.warn(f"Config file not found at %s", config_path)
        return "TODO: Return an error?"

    # load the config file into the config object
    with open(config_path) as c:
        loaded_artifact = yaml.safe_load(c)

        parsed_configs = parse_configs(loaded_artifact)
        return parsed_configs 
    


def parse_configs(config):
    c = Config()
    for m in config["models"]:
        c.models[m["name"]] = m
    return c

def url_for_model(model_name: str):
    pass