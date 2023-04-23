import unittest
from jeu import *

"""auteur: Chloé"""

class TestJeu(unittest.TestCase):
    def setUp(self):
        self.plateau = Plateau(10, 10)

    def test_add_element(self):
        player = Player(0, 0)
        self.plateau.add_element(player)
        self.assertEqual(self.plateau.grid[0][0], player)
        self.assertEqual(self.plateau.player, player)

    def test_remove_element(self):
        player = Player(0, 0)
        self.plateau.add_element(player)
        self.plateau.remove_element(player)
        self.assertIsNone(self.plateau.grid[0][0])
        self.assertIsNone(self.plateau.player)

    def test_is_element(self):
        player = Player(0, 0)
        self.plateau.add_element(player)
        self.assertTrue(self.plateau.is_element(Player))
        self.assertFalse(self.plateau.is_element(Brique))

    def test_is_used(self):
        player = Player(0, 0)
        self.plateau.add_element(player)
        self.assertTrue(self.plateau.is_used(0, 0))
        self.assertFalse(self.plateau.is_used(1, 1))

    def test_is_valid_position(self):
        self.assertTrue(self.plateau.is_valid_position(0, 0))
        self.assertFalse(self.plateau.is_valid_position(-1, -1))
        self.assertFalse(self.plateau.is_valid_position(10, 10))

    def test_move_element(self):
        player = Player(0, 0)
        self.plateau.add_element(player)
        self.plateau.move_element(player, 1, 1)
        self.assertIsNone(self.plateau.grid[0][0])
        self.assertEqual(self.plateau.grid[1][1], player)

    def test_get_falling_elements(self):
        diamant = Diamant(0, 0)
        pierre = Pierre(1, 0)
        self.plateau.add_element(diamant)
        self.plateau.add_element(pierre)
        falling_elements = self.plateau.get_falling_elements()
        self.assertTrue(diamant in falling_elements)
        self.assertTrue(pierre in falling_elements)

    def test_move_player(self):
        player = Player(0, 0)
        sortie = Sortie(1, 0)
        self.plateau.add_element(player)
        self.plateau.add_element(sortie)
        score = self.plateau.move_player(1, 0)
        self.assertEqual(score, True)
        self.assertIsNone(self.plateau.player)

    def test_apply_gravity(self):
        diamant = Diamant(0, 0)
        self.plateau.add_element(diamant)
        self.plateau.apply_gravity(diamant)
        self.assertEqual(self.plateau.grid[0][1], diamant)