from __future__ import annotations
from typing import Dict, Tuple


class Connections:
    """
    Stores the graph of connections between cities and the cost of each line.
    
    The graph is undirected: a connection between A and B is the same as B and A.
    We store the keys as sorted tuples to avoid duplicates.
    """

    def __init__(self) -> None:
        # Key: (city1, city2) sorted alphabetically. Value: cost (int).
        self._distances: Dict[Tuple[str, str], int] = {}

    def _get_key(self, city1: str, city2: str) -> Tuple[str, str]:
        """
        Helper method to create a sorted tuple key for the dictionary.
        This ensures that (A, B) and (B, A) map to the same key.
        """
        if city1 < city2:
            return (city1, city2)
        return (city2, city1)

    def add_connection(self, city1: str, city2: str, cost: int) -> None:
        """
        Adds a connection between two cities with the specified cost.
        
        Args:
            city1: The name of the first city.
            city2: The name of the second city.
            cost: The cost to build a line between them.
            
        Raises:
            ValueError: If the cost is negative.
        """
        if cost < 0:
            raise ValueError("Connection cost cannot be negative")
            
        key = self._get_key(city1, city2)
        self._distances[key] = cost

    def calculate_connecting_cost(self, from_city: str, to_city: str) -> int:
        """
        Returns the cost of the direct line between the two cities.
        
        Args:
            from_city: The starting city.
            to_city: The destination city.
            
        Returns:
            The cost of the connection.
            
        Raises:
            ValueError: If there is no direct connection between the cities.
        """
        key = self._get_key(from_city, to_city)
        if key not in self._distances:
            raise ValueError(f"No connection between {from_city} and {to_city}")
        return self._distances[key]

    def has_connection(self, city1: str, city2: str) -> bool:
        """Checks if a direct connection exists between the two cities."""
        key = self._get_key(city1, city2)
        return key in self._distances