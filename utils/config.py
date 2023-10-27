import logging
import os
from typing import List
import toml
import yaml
import glob
import fnmatch

from watchfiles import awatch


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

    async def watch_and_load_configs(self, directory="", filename="config.yaml"):
        # Get the config directory and filename from the environment variables if provided
        env_directory = os.environ.get("LFAI_CONFIG_PATH", directory)
        if env_directory != None and env_directory != "":
            directory = env_directory
        env_filename = os.environ.get("LFAI_CONFIG_FILENAME", filename)
        if env_filename != None and env_filename != "":
            filename = env_filename

        # Process all the configs that were already in the directory
        self.load_all_configs(directory, filename)

        # Watch the directory for changes until the end of time
        while True:
            async for changes in awatch(directory, recursive=False, step=150):
                # get a unique list of files that have been updated 
                # (awatch can return duplicates depending on the type of updates that happen)
                unique_files = set()
                for change in changes:
                    unique_files.add(os.path.basename(change[1]))

                # filter the files to those that match the filename or glob pattern
                filtered_matches = fnmatch.filter(unique_files, filename)

                # load all the updated config files
                for match in filtered_matches:
                    self.load_config_file(os.path.join(directory, match))





    def load_config_file(self, config_path: str):
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
                return

            # parse the object into our config
            self.parse_models(loaded_artifact)

        return


    def load_all_configs(self, directory="", filename="config.yaml"):
        if not os.path.exists(directory):
            return "THE CONFIG DIRECTORY DOES NOT EXIST"

        # Get all config files
        config_files = glob.glob(os.path.join(directory, filename))

        # load all the found config files into the config object
        for config_path in config_files:
            self.load_config_file(config_path)

        return


    def get_model_backend(self, model: str) -> str | None:
        if model in self.models:
            return self.models[model].backend
        else:
            return None


    def parse_models(self, loaded_artifact):
        for m in loaded_artifact["models"]:
            model_config = Model(name=m["name"],
                                 backend=m["backend"])

            self.models[m["name"]] = model_config