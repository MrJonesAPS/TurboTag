import unittest
from turbo_tag import Player, Team, Game, Ball

class TestTurboTag(unittest.TestCase):
    # Test case 0: This is the one from the example in the file
    def test_empty_game_scoring(self):
        team1 = Team("Blue", 6, "blue")
        team2 = Team("Red", 7, "red")
        game = Game(team1, team2)

        # Nothing happens the entire game

        #This code ends the game
        game.end_game()
        self.assertEqual(team1.score, 0, "In a game where nothing happens, both teams' scores should be 0")
        self.assertEqual(team2.score, 0, "In a game where nothing happens, both teams' scores should be 0")

    #TODO: Add more Unit Tests Here

if __name__ == '__main__':
    unittest.main()
