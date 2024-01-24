import fnmatch
import glob
import logging
import os
from typing import List

import toml
import yaml
from watchfiles import awatch


class Model:
    name: str
    backend: str

    def __init__(self, name: str, backend: str, capabilities: List[str] | None = None):
        self.name = name
        self.backend = backend

class RagModel:
    hub: str
    model: str

    def __init__(self, hub: str, model: str):
        self.hub = hub
        self.model = model

class Rag:
    vector_stores: List[str]
    file_extensions: List[str]
    llm: RagModel
    embed_model: RagModel

    def __init__(self, vector_stores: List[str], file_extensions: List[str], llm: RagModel,  embed_model: RagModel):
        self.vector_stores = vector_stores
        self.file_extensions = file_extensions
        self.llm = llm
        self.embed_model = embed_model


class Config:
    models: dict[str, Model] = {}
    rag: Rag = Rag(vector_stores=[], file_extensions=[], llm={}, embed_model={})

    def __init__(self, models: dict[str, Model] = {}):
        self.models = models

    def __str__(self):
        return f"Models: {self.models}"

    async def watch_and_load_configs(self, directory=".", filename="config.yaml"):
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

    def get_model_backend(self, model: str) -> Model | None:
        if model in self.models:
            return self.models[model]
        else:
            return None

    def get_rag_vector_stores(self):
        return self.rag.vector_stores

    def get_rag_file_extensions(self):
        return self.rag.file_extensions

    def get_rag_llm(self):
        return self.rag.llm

    def get_rag_embed_model(self):
        return self.rag.embed_model

    def parse_models(self, loaded_artifact):
        for m in loaded_artifact["models"]:
            model_config = Model(name=m["name"], backend=m["backend"])

            self.models[m["name"]] = model_config

        if "rag" in loaded_artifact:

            if "llm" in loaded_artifact["rag"]:
                llm = RagModel(hub=loaded_artifact["rag"]["llm"]["hub"], model=loaded_artifact["rag"]["llm"]["model"])
            else:
                llm = RagModel(hub='none', model='none')

            if "embed_model" in loaded_artifact["rag"]:
                embed_model = RagModel(hub=loaded_artifact["rag"]["embed_model"]["hub"], model=loaded_artifact["rag"]["embed_model"]["model"])
            else:
                embed_model = RagModel(hub='none', model='none')

            rag_config = Rag(vector_stores=loaded_artifact["rag"]["vector_stores"], file_extensions=loaded_artifact["rag"]["file_extensions"], llm=llm, embed_model=embed_model)
            self.rag = rag_config
