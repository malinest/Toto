from dataclasses import dataclass

@dataclass
class Counter():
    """
    Class for the counters
    """
    collection: str
    sequence: int

    @staticmethod
    def from_json(json_dict):
        return Counter(json_dict["collection"], json_dict["sequence"])