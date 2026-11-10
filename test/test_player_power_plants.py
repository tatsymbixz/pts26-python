import unittest

from power_grid.player_power_plants import PlayerPowerPlants
from power_grid.simple_types import (
    PowerPlant, PowerPlantNumber, RequestError, Resource)

COAL_PLANT = PowerPlant(number=4, resource=Resource.COAL, cities=1, required_resources=2)
OIL_PLANT = PowerPlant(number=10, resource=Resource.OIL, cities=2, required_resources=1)
ECO_PLANT = PowerPlant(number=13, resource=None, cities=1)
URANIUM_PLANT = PowerPlant(number=20, resource=Resource.URANIUM, cities=3, required_resources=1)


class TestPlayerPowerPlants(unittest.TestCase):
    def test_add_and_get(self) -> None:
        plants = PlayerPowerPlants()
        plants.add_power_plant(COAL_PLANT)
        self.assertEqual(list(plants.get_power_plants()), [COAL_PLANT])

    def test_limit_is_three(self) -> None:
        plants = PlayerPowerPlants([COAL_PLANT, OIL_PLANT, ECO_PLANT])
        self.assertFalse(plants.can_add_power_plant())
        with self.assertRaises(ValueError):
            plants.add_power_plant(URANIUM_PLANT)

    def test_duplicate_plant_rejected(self) -> None:
        plants = PlayerPowerPlants([COAL_PLANT])
        with self.assertRaises(ValueError):
            plants.add_power_plant(COAL_PLANT)

    def test_remove_power_plant(self) -> None:
        plants = PlayerPowerPlants([COAL_PLANT, OIL_PLANT])
        self.assertIsNone(plants.remove_power_plant(PowerPlantNumber(4)))
        self.assertEqual(list(plants.get_power_plants()), [OIL_PLANT])
        self.assertIsInstance(plants.remove_power_plant(PowerPlantNumber(99)), RequestError)

    def test_best_power_plant(self) -> None:
        self.assertIsNone(PlayerPowerPlants().best_power_plant())
        plants = PlayerPowerPlants([COAL_PLANT, OIL_PLANT])
        self.assertEqual(plants.best_power_plant(), PowerPlantNumber(10))

    def test_can_store_resources(self) -> None:
        plants = PlayerPowerPlants([COAL_PLANT, ECO_PLANT])
        self.assertTrue(plants.can_store_resources([Resource.COAL] * 4))
        self.assertFalse(plants.can_store_resources([Resource.COAL] * 5))
        self.assertFalse(plants.can_store_resources([Resource.OIL]))

    def test_number_of_connectable_cities(self) -> None:
        plants = PlayerPowerPlants([COAL_PLANT, OIL_PLANT, ECO_PLANT])
        self.assertEqual(plants.number_of_connectable_cities([]), 1)
        self.assertEqual(plants.number_of_connectable_cities([Resource.OIL]), 3)
        self.assertEqual(
            plants.number_of_connectable_cities(
                [Resource.COAL, Resource.COAL, Resource.OIL]), 4)

    def test_cities_powered_by(self) -> None:
        plants = PlayerPowerPlants([COAL_PLANT, OIL_PLANT])
        result = plants.cities_powered_by(
            [PowerPlantNumber(10)], [Resource.OIL])
        self.assertEqual(result, 2)

    def test_cities_powered_by_errors(self) -> None:
        plants = PlayerPowerPlants([COAL_PLANT])
        self.assertIsInstance(
            plants.cities_powered_by([PowerPlantNumber(99)], []), RequestError)
        self.assertIsInstance(
            plants.cities_powered_by([PowerPlantNumber(4)], [Resource.COAL]), RequestError)
        self.assertIsInstance(
            plants.cities_powered_by(
                [PowerPlantNumber(4), PowerPlantNumber(4)], [Resource.COAL] * 4),
            RequestError)


if __name__ == "__main__":
    unittest.main()
