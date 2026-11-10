from itertools import combinations
from typing import Optional, Sequence, Union

from power_grid.simple_types import (
    PowerPlant, PowerPlantNumber, RequestError, Resource)

MAX_POWER_PLANTS = 3
STORAGE_FACTOR = 2  # a plant can store up to 2x the resources it needs per run


class PlayerPowerPlants:
    """Stores the power plants a player owns (implements UsePowerPlants)."""

    def __init__(self, plants: Sequence[PowerPlant] = ()) -> None:
        self._plants: list[PowerPlant] = []
        for plant in plants:
            self.add_power_plant(plant)

    def can_add_power_plant(self) -> bool:
        """Returns True if the player is still below the power plant limit."""
        return len(self._plants) < MAX_POWER_PLANTS

    def add_power_plant(self, plant: PowerPlant) -> None:
        """
        Adds a power plant to the player's collection.

        Raises ValueError if the limit is reached or the plant is already owned.
        """
        if not self.can_add_power_plant():
            raise ValueError("Player already owns the maximum number of power plants")
        if any(owned.number == plant.number for owned in self._plants):
            raise ValueError(f"Power plant {plant.number} is already owned")
        self._plants.append(plant)

    def remove_power_plant(self, number: PowerPlantNumber) -> Optional[RequestError]:
        """Removes the plant with the given number, or returns an error if not owned."""
        for plant in self._plants:
            if plant.number == number.number:
                self._plants.remove(plant)
                return None
        return RequestError(f"Power plant {number.number} is not owned")

    def get_power_plants(self) -> Sequence[PowerPlant]:
        """Returns the power plants owned by the player."""
        return list(self._plants)

    def best_power_plant(self) -> Optional[PowerPlantNumber]:
        """Returns the number of the plant with the highest number (None if no plants)."""
        if not self._plants:
            return None
        return PowerPlantNumber(max(plant.number for plant in self._plants))

    def can_store_resources(self, resources: Sequence[Resource]) -> bool:
        """Checks whether the given resources fit into the storage of the owned plants."""
        capacity: dict[Resource, int] = {resource: 0 for resource in Resource}
        for plant in self._plants:
            if plant.resource is not None:
                capacity[plant.resource] += STORAGE_FACTOR * plant.required_resources
        needed: dict[Resource, int] = {resource: 0 for resource in Resource}
        for resource in resources:
            needed[resource] += 1
        return all(needed[resource] <= capacity[resource] for resource in Resource)

    def number_of_connectable_cities(self, resources: Sequence[Resource]) -> int:
        """Returns the maximum number of cities the owned plants can power with the resources."""
        best = 0
        for size in range(len(self._plants) + 1):
            for chosen in combinations(self._plants, size):
                if self._needs_fit(chosen, resources):
                    best = max(best, sum(plant.cities for plant in chosen))
        return best

    def cities_powered_by(self, numbers: Sequence[PowerPlantNumber],
                          resources: Sequence[Resource]) -> Union[int, RequestError]:
        """
        Returns how many cities the chosen plants power with the given resources.

        Returns a RequestError if a plant is not owned, is listed twice, or the
        resources are not enough. Does not change any state: the caller removes the
        burned resources (PlayerResources.remove_resources).
        """
        chosen: list[PowerPlant] = []
        for number in numbers:
            owned = [plant for plant in self._plants if plant.number == number.number]
            if not owned:
                return RequestError(f"Power plant {number.number} is not owned")
            if owned[0] in chosen:
                return RequestError(f"Power plant {number.number} listed twice")
            chosen.append(owned[0])
        if not self._needs_fit(chosen, resources):
            return RequestError("Not enough resources to run the chosen power plants")
        return sum(plant.cities for plant in chosen)

    @staticmethod
    def _needs_fit(plants: Sequence[PowerPlant], resources: Sequence[Resource]) -> bool:
        """Checks whether the available resources cover what the plants need."""
        needed: dict[Resource, int] = {resource: 0 for resource in Resource}
        for plant in plants:
            if plant.resource is not None:
                needed[plant.resource] += plant.required_resources
        available: dict[Resource, int] = {resource: 0 for resource in Resource}
        for resource in resources:
            available[resource] += 1
        return all(needed[resource] <= available[resource] for resource in Resource)
