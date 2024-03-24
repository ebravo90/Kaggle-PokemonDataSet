import logging
from dataclasses import dataclass, field
from pathlib import Path

import coloredlogs
import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
coloredlogs.install(level="INFO")

DATAFRAME_COLUMNS = [
    "#",  # 0
    "Name",  # 1
    "Type 1",  # 2
    "Type 2",  # 3
    "HP",  # 4
    "Attack",  # 5
    "Defense",  # 6
    "Sp. Atk",  # 7
    "Sp. Def",  # 8
    "Speed",  # 9
    "Generation",  # 10
    "Legendary",  # 11
]
ID_COLUMN = DATAFRAME_COLUMNS[0]

@dataclass(kw_only=True)
class Profile:
    identifier: int
    name: str
    type: str
    subtype: str
    generation: int
    legendary: bool
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int
    total_stats: int = field(init=False)

    def __post_init__(self):
        self.calculate_total_stats()
        self.fix_subtype()

    def calculate_total_stats(self) -> None:
        stats_list = [
            self.hp,
            self.attack,
            self.defense,
            self.special_attack,
            self.special_defense,
            self.speed,
        ]
        self.total_stats = sum(stats_list)

    def fix_subtype(self) -> None:
        if isinstance(self.subtype, float):
            self.subtype = ""


class Factory:

    def __init__(self, dataset_path: str):
        self.dataset = dataset_path
        self.dataframe = pd.DataFrame()
        self.collection = []


    def _validate_dataset_path(self) -> bool:
        if not Path(self.dataset).exists():
            logging.error("Path doesn't exists.")
            return False
        logging.info("Dataset path is correct.")
        return True


    def _validate_dataframe_format(self, columns: list) -> bool:
        try:
            for column in columns:
                self.dataframe[column]
        except KeyError:
            logging.exception("Column '%s' is not part of the data frame.")
            return False
        return


    def _load_data_frame(self) -> bool:
        if not self._validate_dataset_path():
            return False

        self.dataframe = pd.read_csv(self.dataset)

        if self._validate_dataframe_format(DATAFRAME_COLUMNS):
            return False
        return True


    def _factory(self) -> bool:
        for pokemon_id in range(1, self.dataframe["#"].max() + 1):
            pokemon_dict = (
                self.dataframe[
                    self.dataframe[ID_COLUMN] == pokemon_id
                ]
                .to_dict(orient="records")[0]
            )
            if not pokemon_dict:
                return False

            pokemon = Profile(
                identifier=pokemon_dict[ID_COLUMN],
                name=pokemon_dict[DATAFRAME_COLUMNS[1]],
                type=pokemon_dict[DATAFRAME_COLUMNS[2]],
                subtype=pokemon_dict[DATAFRAME_COLUMNS[3]],
                generation=pokemon_dict[DATAFRAME_COLUMNS[10]],
                legendary=pokemon_dict[DATAFRAME_COLUMNS[11]],
                hp=pokemon_dict[DATAFRAME_COLUMNS[4]],
                attack=pokemon_dict[DATAFRAME_COLUMNS[5]],
                defense=pokemon_dict[DATAFRAME_COLUMNS[6]],
                special_attack=pokemon_dict[DATAFRAME_COLUMNS[7]],
                special_defense=pokemon_dict[DATAFRAME_COLUMNS[8]],
                speed=pokemon_dict[DATAFRAME_COLUMNS[9]],
            )
            self.collection.append(pokemon)

        if not self.collection:
            return False
        return True


    def _load_data(self) -> bool:
        if not self._load_data_frame():
            return False

        if not self._factory():
            return False
        return True

    def get_collection(self) -> list:
        self._load_data()
        return self.collection
