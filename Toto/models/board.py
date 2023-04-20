from dataclasses import dataclass

@dataclass
class Board():
    """
    Class for the 'boards' collection
    """
    collection_name: str
    name: str
    abbreviation: str

    @staticmethod
    def from_json(json_dict):
        return Board(json_dict["collection_name"], json_dict["name"], json_dict["abbreviation"])