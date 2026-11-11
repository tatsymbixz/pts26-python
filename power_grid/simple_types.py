from enum import Enum, auto
from dataclasses import dataclass
from typing import List


class Resource(Enum):
    """The four types of resources available in the game."""
    COAL = 1
    OIL = 2
    GARBAGE = 3
    URANIUM = 4


class PlayerColor(Enum):
    """The possible colors for players according to the UML diagram."""
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    PURPLE = auto()
    BLACK = auto()


class PhaseStatus(Enum):
    """Indicates the status of the current phase or the game itself."""
    CONTINUES = auto()
    PHASE_ENDS = auto()
    GAME_ENDS = auto()


class GamePhase(Enum):
    """The sequential phases that make up a single game round."""
    AUCTION = auto()
    BUY_RESOURCES = auto()
    BUILD_HOUSES = auto()
    BUREAUCRACY = auto()
    GAME_END = auto()


class GameStep(Enum):
    """The three steps of the game. The step affects building limits."""
    STEP_1 = auto()
    STEP_2 = auto()
    STEP_3 = auto()


@dataclass(frozen=True)
class PowerPlantNumber:
    """A simple wrapper around an integer representing a power plant's number."""
    number: int


@dataclass(frozen=True)
class RequestError:
    """Represents an error returned by a game action instead of raising an exception."""
    description: str


@dataclass(frozen=True)
class SerializedGameState:
    """Holds the serialized state of the game, typically as a JSON string."""
    state: str


@dataclass(frozen=True)
class PowerPlant:
    """
    Represents a power plant card according to the UML diagram.
    Fields are in snake_case to satisfy pylint and Python conventions.
    """
    number: PowerPlantNumber
    accepted_resources: List[Resource]
    number_of_cities: int
    resource_amount: int = 0

    # --- Backward compatibility properties ---
    # These properties allow the rest of the codebase (written by other team members)
    # to continue using the old camelCase field names without breaking.
    # They redirect read access to the new snake_case fields.

    @property
    def acceptedResources(self) -> List[Resource]:
        """Compatibility property for 'accepted_resources'."""
        return self.accepted_resources

    @property
    def numberOfCities(self) -> int:
        """Compatibility property for 'number_of_cities'."""
        return self.number_of_cities

    @property
    def resourceAmount(self) -> int:
        """Compatibility property for 'resource_amount'."""
        return self.resource_amount
