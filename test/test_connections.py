import unittest
from power_grid.connections import Connections


class TestConnections(unittest.TestCase):
    """Unit tests for the Connections class."""

    def test_add_and_get_connection_cost(self) -> None:
        conn = Connections()
        conn.add_connection("Berlin", "Hamburg", 10)
        self.assertEqual(conn.calculate_connecting_cost("Berlin", "Hamburg"), 10)
        # Order shouldn't matter
        self.assertEqual(conn.calculate_connecting_cost("Hamburg", "Berlin"), 10)

    def test_connection_not_found(self) -> None:
        conn = Connections()
        with self.assertRaisesRegex(ValueError, "No connection"):
            conn.calculate_connecting_cost("Berlin", "Munich")

    def test_has_connection(self) -> None:
        conn = Connections()
        conn.add_connection("Berlin", "Hamburg", 10)
        self.assertTrue(conn.has_connection("Berlin", "Hamburg"))
        self.assertFalse(conn.has_connection("Berlin", "Munich"))

    def test_negative_cost_raises_error(self) -> None:
        conn = Connections()
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            conn.add_connection("Berlin", "Hamburg", -5)


if __name__ == '__main__':
    unittest.main()