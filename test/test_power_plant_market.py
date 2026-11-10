import unittest
from power_grid.power_plant_market import PowerPlantMarket
from power_grid.simple_types import PowerPlant, Resource


class TestPowerPlantMarket(unittest.TestCase):
    """Unit tests for the PowerPlantMarket class."""

    def _make_plant(self, number: int) -> PowerPlant:
        """Helper function to create a dummy power plant for testing."""
        return PowerPlant(number=number, resource=Resource.COAL, cities=1, required_resources=1)

    def test_start_phase_fills_markets(self) -> None:
        """Test that start_phase correctly fills 4 current and 4 future cards."""
        # Create a deck of 10 valid plants (numbers 3 to 12)
        deck = [self._make_plant(i) for i in range(3, 13)]
        market = PowerPlantMarket(deck)
        
        market.start_phase()

        # Check that the current market has 4 cards
        self.assertEqual(len(market.get_current_market()), 4)
        # Check that the future market has 4 cards
        self.assertEqual(len(market.get_future_market()), 4)
        
        # The cheapest card should be number 3 (since they are sorted)
        cheapest = market.get_cheapest_power_plant()
        self.assertIsNotNone(cheapest)
        if cheapest is not None:
            self.assertEqual(cheapest.number, 3)

    def test_take_power_plant_replenishes_from_future(self) -> None:
        """Test that buying a plant removes it and brings a new one from the future market."""
        deck = [self._make_plant(i) for i in range(3, 13)]
        market = PowerPlantMarket(deck)
        market.start_phase()

        # Player buys the cheapest plant (number 3)
        cheapest = market.get_cheapest_power_plant()
        self.assertIsNotNone(cheapest)
        if cheapest is not None:
            market.take_power_plant(cheapest)

            # The bought plant should no longer be in the current market
            self.assertNotIn(cheapest, market.get_current_market())
            
            # The current market should still have 4 cards
            self.assertEqual(len(market.get_current_market()), 4)
            
            # The new cheapest plant should be number 4
            new_cheapest = market.get_cheapest_power_plant()
            self.assertIsNotNone(new_cheapest)
            if new_cheapest is not None:
                self.assertEqual(new_cheapest.number, 4)

    def test_take_plant_not_in_market_raises_error(self) -> None:
        """Test that trying to buy a plant not on the market raises an error."""
        deck = [self._make_plant(i) for i in range(3, 13)]
        market = PowerPlantMarket(deck)
        market.start_phase()

        # Plant number 50 is not in the market
        not_in_market = self._make_plant(50)
        
        with self.assertRaisesRegex(ValueError, "Plant not found"):
            market.take_power_plant(not_in_market)

    def test_empty_deck_works(self) -> None:
        """Test that the market handles an empty deck gracefully (for testing)."""
        market = PowerPlantMarket([])
        market.start_phase()
        
        self.assertEqual(len(market.get_current_market()), 0)
        self.assertIsNone(market.get_cheapest_power_plant())


if __name__ == '__main__':
    unittest.main()