from power_grid.game_adapter import PowerGridGameAdapter
from power_grid.simple_types import SerializedGameState


def test_game_adapter_conversion() -> None:
    adapter = PowerGridGameAdapter()
    
    # Test conversion to external
    external = adapter.to_external("test_state")
    assert isinstance(external, SerializedGameState)
    assert external.state == "test_state"
    
    # Test conversion back to internal
    internal = adapter.to_internal(external)
    assert internal == "test_state"