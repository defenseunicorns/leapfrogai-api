import logging
import os
from typing import List

import toml
import yaml
import glob


class Model:
    name: str
    backend: str

    def __init__(self, name: str, backend: str, capabilities: List[str] | None = None):
        self.name = name
        self.backend = backend


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
        env_filename = os.environ.get("LFAI_CONFIG_FILENAME", filename)
 
        if env_filename != None and env_filename != "":
            filename = env_filename

        if not os.path.exists(directory):
            return "THE CONFIG DIRECTORY DOES NOT EXIST"

        config_files = glob.glob(os.path.join(directory, filename))

        for config_path in config_files:
            # ensure the config file exists
            if not os.path.exists(config_path):
                logging.warn(f"Config file not found at %s", config_path)
                return "TODO: Return an error?"

            # load the config file into the config object
            with open(config_path) as c:
                # Load the file into a python object
                loaded_artifact = {}
                if config_path.endswith(".toml"):
                    loaded_artifact = toml.load(c)
                elif config_path.endswith(".yaml"):
                    loaded_artifact = yaml.safe_load(c)
                else:
                    # TODO: Return an error ???
                    print(f"Unsupported file type: {config_path}")
                    continue

                # parse the object into our config
                self.parse_models(loaded_artifact)

        return self


    def parse_models(self, loaded_artifact):
        for m in loaded_artifact["models"]:
            model_config = Model(name=m["name"],
                                 backend=m["backend"])

            self.models[m["name"]] = model_config