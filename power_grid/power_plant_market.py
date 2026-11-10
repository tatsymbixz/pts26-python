from __future__ import annotations
from typing import List, Optional
from power_grid.simple_types import PowerPlant


class PowerPlantMarket:
    """
    Manages the power plant market.
    It consists of a 'current' market (4 cards) and a 'future' market (4 cards).
    When a card is bought, it's removed, and a new one is drawn from the deck.
    """

    def __init__(self, deck: List[PowerPlant]) -> None:
        # We use a list for the deck to allow passing incomplete decks for testing
        self._deck: List[PowerPlant] = list(deck)
        self._current_market: List[PowerPlant] = []
        self._future_market: List[PowerPlant] = []

    def start_phase(self) -> None:
        """
        Initializes the market at the start of the game.
        Fills 4 cards for the current market and 4 for the future market.
        """
        self._current_market.clear()
        self._future_market.clear()

        # Draw 4 cards for the current market
        for _ in range(4):
            if self._deck:
                self._current_market.append(self._deck.pop(0))
                
        # Draw 4 cards for the future market
        for _ in range(4):
            if self._deck:
                self._future_market.append(self._deck.pop(0))

        self._sort_markets()

    def _sort_markets(self) -> None:
        """Sorts both markets by the power plant number."""
        self._current_market.sort(key=lambda p: p.number)
        self._future_market.sort(key=lambda p: p.number)

    def get_cheapest_power_plant(self) -> Optional[PowerPlant]:
        """Returns the cheapest power plant currently available for auction."""
        if not self._current_market:
            return None
        return self._current_market[0]

    def take_power_plant(self, plant: PowerPlant) -> None:
        """
        Removes a plant from the market after it's bought.
        Replenishes the current market from the future market.
        """
        if plant in self._current_market:
            self._current_market.remove(plant)
            self._replenish_market()
        elif plant in self._future_market:
            self._future_market.remove(plant)
            if self._deck:
                self._future_market.append(self._deck.pop(0))
        else:
            raise ValueError("Plant not found in market")
            
        self._sort_markets()

    def _replenish_market(self) -> None:
        """
        Moves the cheapest card from the future market to the current market
        to maintain 4 cards in the current market.
        """
        while self._future_market and len(self._current_market) < 4:
            cheapest_future = min(self._future_market, key=lambda p: p.number)
            self._future_market.remove(cheapest_future)
            self._current_market.append(cheapest_future)

        # If future market is empty, draw from deck
        while self._deck and len(self._current_market) < 4:
            self._current_market.append(self._deck.pop(0))

    def get_current_market(self) -> List[PowerPlant]:
        """Returns a copy of the current market (useful for testing and UI)."""
        return list(self._current_market)

    def get_future_market(self) -> List[PowerPlant]:
        """Returns a copy of the future market."""
        return list(self._future_market)