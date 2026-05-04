import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

test_width = 120
test_height = 40

# Lines 11-18 were borrowed and altered from test_deck.py written by Candace.
os.environ["COLUMNS"] = f"{test_width}"
os.environ["LINES"] = f"{test_height}"

with patch("os.get_terminal_size", return_value=(test_width, test_height)):
    from pokete.__main__ import Figure
    from pokete import release
    from pokete.classes.save import save
    from pokete.classes.settings import settings


# Dummy classes used to populate test data without creating entire game instance
class DummyLabel:
    def rechar(self, _):
        pass


class DummyMoveMap:
    code_label = DummyLabel()


class DummyMap:
    def __init__(self, name="testmap"):
        self.name = name
        self.pretty_name = name
        self.movemap = DummyMoveMap()


session_info_dict = {
    "user": "TestUser",
    "represent_char": "a",
    "map": "testmap",
    "oldmap": "testmap",
    "last_center_map": "testmap",
    "x": 0,
    "y": 0,
    "achievements": [],
    "pokes": {},
    "inv": {},
    "money": 0,
    "settings": {},
    "caught_poketes": [],
    "visited_maps": [],
    "hotkeys": {},
    "used_npcs": [],
    "pokete_care": {},
    "time": 0,
}


def make_figure():
    fig = Figure(session_info_dict)
    # Attach minimal map objects so set_args() doesn't crash
    fig.map = DummyMap()  # type: ignore
    fig.oldmap = DummyMap()  # type: ignore
    fig.last_center_map = DummyMap()  # type: ignore
    fig.set_args({"dummy": True})
    return fig


# Test suite created using course approved AI tool MS Copilot
class TestAutosaveFix(unittest.TestCase):
    """Test suite for Autosave Fix"""

    def setUp(self):
        """Creates a temporary save file for testing save function"""
        self.temp_directory = tempfile.TemporaryDirectory()
        self.old_savepath = release.SAVEPATH
        release.SAVEPATH = Path(self.temp_directory.name)

    def tearDown(self):
        """Restores original savepath following testing"""
        release.SAVEPATH = self.old_savepath
        self.temp_directory.cleanup()

    def test_save_raises_before_set_args(self):
        """Saving before figure.set_args() should fail (old crash behavior)."""
        fig = Figure(session_info_dict)
        settings("autosave").val = True

        with self.assertRaises(Exception):
            save(fig)

    def test_save_succeeds_after_set_args(self):
        """Saving after initialization should succeed (fixed behavior)."""
        fig = make_figure()
        settings("autosave").val = True

        save(fig)

        # Verify save file exists
        savefile = os.path.join(self.temp_directory.name, "pokete.json")
        self.assertTrue(os.path.exists(savefile))

    def test_save_ignores_autosave_setting(self):
        """save() should always write a file; autosave setting only affects
        autosave thread."""
        fig = make_figure()
        settings("autosave").val = False  # autosave disabled

        save(fig)

        savefile = os.path.join(self.temp_directory.name, "pokete.json")
        self.assertTrue(os.path.exists(savefile))

    def test_save_creates_valid_json(self):
        """Saved file should contain valid JSON."""
        import json

        fig = make_figure()
        settings("autosave").val = True

        save(fig)

        savefile = os.path.join(self.temp_directory.name, "pokete.json")
        with open(savefile) as f:
            data = json.load(f)

        self.assertIn("user", data)
        self.assertEqual(data["user"], "TestUser")
