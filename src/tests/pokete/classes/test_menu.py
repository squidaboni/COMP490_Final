import unittest
from unittest.mock import patch, MagicMock, Mock
import os
import sys

os.environ["COLUMNS"] = "80"
os.environ["LINES"] = "24"

sys.modules['pokete.base.input_loops'] = MagicMock()
sys.modules['pokete.base.input_loops.ask'] = MagicMock()
sys.modules['pokete.base.input_loops.new_text_input'] = MagicMock()

with patch("os.get_terminal_size", return_value=(80, 24)):
    import pokete.base.tss
    from pokete.classes.menu import Menu
    from pokete.classes.game import ReturnToMenuException


class MyTestCase(unittest.TestCase):
    def test_return_to_menu_exception_is_exception(self):
        with self.assertRaises(ReturnToMenuException):
            raise ReturnToMenuException()# add assertion here

    def test_choose_raises_return_to_menu_on_return_label(self):
        menu = Menu()
        menu.c_obs = [menu.return_label]
        menu.index = Mock()
        menu.index.index = 0
        ctx = Mock()
        with patch("pokete.classes.menu.save"):
            with self.assertRaises(ReturnToMenuException):
                menu.choose(ctx, 0)

    def test_return_label_in_elems(self):
        menu = Menu()
        self.assertIn(menu.return_label, menu.elems)

    def test_return_label_order(self):
        menu = Menu()
        elems = menu.elems
        save_idx = elems.index(menu.save_label)
        return_idx = elems.index(menu.return_label)
        exit_idx = elems.index(menu.exit_label)
        self.assertLess(save_idx, return_idx)
        self.assertLess(return_idx, exit_idx)

    def test_return_label_text(self):
        import scrap_engine as se
        menu = Menu()
        self.assertIsInstance(menu.return_label, se.Text)
        self.assertEqual(menu.return_label.text, "Return to main menu")

    def test_exit_label_does_not_raise_return_to_menu(self):
        menu = Menu()
        menu.c_obs = [menu.exit_label]
        menu.index = Mock()
        menu.index.index = 0
        ctx = Mock()
        with patch("pokete.classes.menu.save"):
            with self.assertRaises(SystemExit):
                menu.choose(ctx, 0)

    def test_return_to_menu_exception_inherits_exception(self):
        self.assertTrue(issubclass(ReturnToMenuException, Exception))

if __name__ == '__main__':
    unittest.main()
