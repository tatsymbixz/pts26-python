import unittest
from power_grid.towns import Towns
from power_grid.simple_types import PlayerColor


class TestTowns(unittest.TestCase):
    """Sociable unit tests for the Towns class."""

    def test_buy_house_in_empty_town(self) -> None:
        towns = Towns(max_slots_per_town=3)
        towns.buy_houses(PlayerColor.RED, ["Berlin"])
        self.assertEqual(towns.get_number_of_houses(PlayerColor.RED), 1)
        self.assertEqual(towns.get_owner_of_house("Berlin", 0), PlayerColor.RED)

    def test_cannot_buy_house_if_already_owned(self) -> None:
        towns = Towns(max_slots_per_town=3)
        towns.buy_houses(PlayerColor.RED, ["Berlin"])
        with self.assertRaisesRegex(ValueError, "already has a house"):
            towns.buy_houses(PlayerColor.RED, ["Berlin"])

    def test_two_players_can_build_in_same_town(self) -> None:
        towns = Towns(max_slots_per_town=2)
        towns.buy_houses(PlayerColor.RED, ["Berlin"])
        towns.buy_houses(PlayerColor.BLUE, ["Berlin"])
        self.assertEqual(towns.get_owner_of_house("Berlin", 0), PlayerColor.RED)
        self.assertEqual(towns.get_owner_of_house("Berlin", 1), PlayerColor.BLUE)

    def test_town_full_raises_error(self) -> None:
        towns = Towns(max_slots_per_town=1)
        towns.buy_houses(PlayerColor.RED, ["Berlin"])
        with self.assertRaisesRegex(ValueError, "is full"):
            towns.buy_houses(PlayerColor.BLUE, ["Berlin"])

    def test_get_owner_of_invalid_slot_returns_none(self) -> None:
        towns = Towns()
        towns.buy_houses(PlayerColor.RED, ["Berlin"])
        self.assertIsNone(towns.get_owner_of_house("Berlin", 5))
        self.assertIsNone(towns.get_owner_of_house("Unknown", 0))


if __name__ == '__main__':
    unittest.main()