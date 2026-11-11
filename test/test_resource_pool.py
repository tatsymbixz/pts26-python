from power_grid.resource_pool import ResourcePool
from power_grid.simple_types import Resource


def test_resource_pool_can_take_and_put() -> None:
    pool = ResourcePool([Resource.COAL, Resource.COAL, Resource.OIL])
    
    # Check if it can take resources
    assert pool.canTakeResourcesFromStorageSpace([Resource.COAL, Resource.OIL]) is True
    assert pool.canTakeResourcesFromStorageSpace([Resource.URANIUM]) is False
    
    # Take resources
    pool.takeResources([Resource.COAL])
    assert pool.canTakeResourcesFromStorageSpace([Resource.COAL, Resource.COAL]) is False


def test_resource_pool_to_string() -> None:
    pool = ResourcePool([Resource.OIL])
    assert "Resource.OIL" in pool.toString()