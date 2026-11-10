import unittest
from power_grid.towns import Towns
from power_grid.power_plant_market import PowerPlantMarket
from power_grid.simple_types import PlayerColor, Resource, PowerPlant


class TestIntegration(unittest.TestCase):
    """
    End-to-End integration tests.
    These tests simulate a realistic game flow, checking how different classes interact.
    """

    def _make_plant(self, number: int) -> PowerPlant:
        """Helper to create a valid power plant."""
        return PowerPlant(number=number, resource=Resource.COAL, cities=1, required_resources=1)

    def test_scenario_1_auction_and_building(self) -> None:
        """
        Scenario 1: A player buys a power plant at auction and builds a house.
        
        Flow:
        1. Set up the market with a deck of plants.
        2. Player buys the cheapest plant (auction logic).
        3. Player builds a house in a city (building logic).
        4. Verify the state (player has the plant, city has the house).
        """
        # 1. Setup
        deck = [self._make_plant(i) for i in range(3, 13)]
        market = PowerPlantMarket(deck)
        market.start_phase()
        
        towns = Towns()
        player = PlayerColor.RED
        city = "Berlin"

        # 2. Player buys the cheapest plant
        cheapest_plant = market.get_cheapest_power_plant()
        self.assertIsNotNone(cheapest_plant)
        if cheapest_plant is not None:
            market.take_power_plant(cheapest_plant)
            # The market should replenish and the cheapest plant changes
            self.assertNotEqual(market.get_cheapest_power_plant().number, cheapest_plant.number)

        # 3. Player builds a house in Berlin
        towns.buy_houses(player, [city])

        # 4. Verify state
        # Check that the player has a house in Berlin
        self.assertEqual(towns.get_number_of_houses(player), 1)
        self.assertEqual(towns.get_owner_of_house(city, 0), player)
        
        # Check that the market has 4 cards in the current market still
        self.assertEqual(len(market.get_current_market()), 4)

    def test_scenario_2_multiple_players_building(self) -> None:
        """
        Scenario 2: Two players build houses in the same city, and one buys a plant.
        
        Flow:
        1. Player RED builds a house in Munich.
        2. Player BLUE builds a house in Munich (if slots allow).
        3. Player BLUE buys a power plant.
        4. Verify that both actions are recorded correctly.
        """
        # Setup
        towns = Towns(max_slots_per_town=2) # Allow 2 houses in this test
        deck = [self._make_plant(i) for i in range(3, 10)]
        market = PowerPlantMarket(deck)
        market.start_phase()

        player_red = PlayerColor.RED
        player_blue = PlayerColor.BLUE
        city = "Munich"

        # 1. RED builds
        towns.buy_houses(player_red, [city])
        self.assertEqual(towns.get_owner_of_house(city, 0), player_red)

        # 2. BLUE builds
        towns.buy_houses(player_blue, [city])
        self.assertEqual(towns.get_owner_of_house(city, 1), player_blue)
        
        # Check that both have 1 house
        self.assertEqual(towns.get_number_of_houses(player_red), 1)
        self.assertEqual(towns.get_number_of_houses(player_blue), 1)

        # 3. BLUE buys a plant
        plant_to_buy = market.get_cheapest_power_plant()
        self.assertIsNotNone(plant_to_buy)
        if plant_to_buy is not None:
            market.take_power_plant(plant_to_buy)
            
        # 4. Verify market state
        self.assertEqual(len(market.get_current_market()), 4)


if __name__ == '__main__':
    unittest.main()