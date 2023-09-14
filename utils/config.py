import os
from typing import List
import yaml
import logging

class Model:
    name: str
    backend: str
    capabilities: List[str] | None
    
    def __init__(self, name: str, backend: str, capabilities: List[str] | None = None):
        self.name = name
        self.backend = backend
        self.capabilities = capabilities


class Config:
    models: dict[str, Model] = {}
    
    def __init__(self, models: dict[str, Model] = {}):
        self.models = models

    def __str__(self):
        return f"Models: {self.models}"
    
    def model_backend(self, model: str) -> str | None:
        if model in self.models:
            return self.models[model].backend
        else:
            return None
        
    def load(self, directory="", filename="config.yaml"):
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

            self.parse_models(loaded_artifact)
        
    
    def parse_models(self, loaded_artifact):
        for m in loaded_artifact["models"]:
            self.models[m["name"]] = m