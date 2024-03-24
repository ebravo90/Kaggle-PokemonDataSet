import logging
import re

import coloredlogs

from data_factory import Factory


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
coloredlogs.install(level="INFO")


class DataHandler:
    def __init__(self, dataset_path: str) -> None:
        # Create a composition of the Factory class.
        init_factory = Factory(dataset_path)
        self.collection = init_factory.get_collection()

    def get_by_id(self, identifier: int) -> dict:
        pick_data = None
        for data in self.collection:
            if  data._id == identifier:
                pick_data = data

        if not pick_data:
            logging.error("There is not Pokemon with the given ID.")
            return {}
        return pick_data.__dict__

    def get_by_name(self, name: str) -> dict:
        pick_data = ""
        for data in self.collection:
            if re.match(name, data.name, flags=re.IGNORECASE):
                pick_data = data

        if not pick_data:
            logging.error("There is not Pokemon with the given name.")
            return {}
        return pick_data.__dict__

    def get_by_type(self, data_type: str) -> dict:
        pick_data = {}
        found_id = 0
        for data in self.collection:
            if re.match(
                data_type, data.type, flags=re.IGNORECASE
            ) or re.match(data_type, data.subtype, flags=re.IGNORECASE):
                found_id += 1
                pick_data[f"match_{found_id}"] = data.__dict__

        if not pick_data:
            logging.error("There is not Pokemon with the given type.")
            return {}
        logging.info(
            "Pokemon with the type '%s': %s.", data_type, len(pick_data.keys())
        )
        return pick_data

    def get_legendary(self) -> dict:
        pick_data = {}
        found_id = 0
        for data in self.collection:
            if data.legendary:
                found_id += 1
                pick_data[f"match_{found_id}"] = data.__dict__

        if not pick_data:
            logging.error("There is not Pokemon with the given type.")
            return {}
        logging.info("Legendary pokemon found: %s.", len(pick_data.keys()))
        return pick_data

    def get_whole_collection(self) -> list:
        """
        Get whole collection as list of dictionaries.

        :return: List of dictionaries.
        :rtype: list
        """
        pick_data = []
        for data in self.collection:
            pick_data.append(data.__dict__)

        if not pick_data:
            logging.error("Something went wrong while retrieving collection.")
            return []
        logging.info("Retrieve collection with: %s pokemon.", len(pick_data))
        return pick_data


if __name__ == "__main__":
    pokemon_data = DataHandler("src/Pokemon.csv")
    print(pokemon_data.get_by_type("grass"))