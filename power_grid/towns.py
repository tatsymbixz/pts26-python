from __future__ import annotations
from typing import Dict, List, Optional
from power_grid.simple_types import PlayerColor


class Towns:
    """
    Stores information about the houses players have built in cities.
    Key: city name (str). Value: list of players (in the order they built).
    
    This class handles the logic for building houses, checking ownership,
    and counting how many cities a player has built in.
    """

    def __init__(self, max_slots_per_town: int = 3) -> None:
        """
        Initializes the Towns storage.
        
        Args:
            max_slots_per_town: The maximum number of houses allowed in a single town.
                                (Normally 1 for Step 1, 2 for Step 2, 3 for Step 3).
        """
        self._houses: Dict[str, List[PlayerColor]] = {}
        self._max_slots: int = max_slots_per_town

    def buy_houses(self, player: PlayerColor, town_names: List[str]) -> None:
        """
        Adds a player's house to the specified cities.
        
        Raises:
            ValueError: If the town is full or if the player already has a house there.
        """
        for town in town_names:
            # If the town is not in our dictionary yet, initialize it with an empty list
            if town not in self._houses:
                self._houses[town] = []

            # A player cannot build more than one house in the same town
            if player in self._houses[town]:
                raise ValueError(f"Player {player} already has a house in {town}")

            # Check if the town has reached its maximum capacity for the current step
            if len(self._houses[town]) >= self._max_slots:
                raise ValueError(f"Town {town} is full (max {self._max_slots} slots)")

            # Add the player's house to the town
            self._houses[town].append(player)

    def get_number_of_houses(self, player: PlayerColor) -> int:
        """
        Returns the number of cities where the player has a house.
        This is used for determining player order and winning conditions.
        """
        return sum(1 for houses in self._houses.values() if player in houses)

    def get_owner_of_house(self, town: str, slot: int) -> Optional[PlayerColor]:
        """
        Returns the owner of the house in a specific slot (0, 1, or 2).
        
        Args:
            town: The name of the city.
            slot: The index of the house (0 is the first one built, 1 is the second, etc.).
            
        Returns:
            The PlayerColor of the owner, or None if the slot is empty or invalid.
        """
        if town in self._houses and 0 <= slot < len(self._houses[town]):
            return self._houses[town][slot]
        return None

    def start_phase(self) -> None:
        """
        Clears the state before a new phase (if needed).
        Currently does nothing, but is required by the interface.
        """
        pass