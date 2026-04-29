import unittest
from unittest.mock import patch
import os

test_width = 120
test_height = 40

# Lines 9-13 were borrowed from test_deck.py written by Candace.
os.environ["COLUMNS"] = f"{test_width}"
os.environ["LINES"] = f"{test_height}"

with patch("os.get_terminal_size", return_value=(test_width, test_height)):
    from pokete.classes.fight.fightmap import FightMap


def render_test_fightmap_chars(map_width, map_height):
    """Collects all the characters rendered to the screen in Fightmap into a single
    list of characters"""
    test_fightmap = FightMap(map_width, map_height).map
    list_all_map_chars = []
    for line in test_fightmap:
        for char in line:
            list_all_map_chars.append(char)
    return list_all_map_chars


class TestFightMap(unittest.TestCase):
    """Test suite for fightmap UI"""

    def test_box_chars_in_output(self):
        """Checks to make sure that the fightmap UI is using box drawing characters."""
        rendered_map_chars = render_test_fightmap_chars(test_width, test_height)
        self.assertIn("┌", rendered_map_chars)
        self.assertIn("┐", rendered_map_chars)
        self.assertIn("└", rendered_map_chars)
        self.assertIn("┘", rendered_map_chars)
        self.assertIn("│", rendered_map_chars)
        self.assertIn("─", rendered_map_chars)
