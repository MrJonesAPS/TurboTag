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


    
    # Test case 1: Testing if a goal increases the team's score by 3 points
    def test_goal_scoring(self):
        team = Team("Test Team", 6, "blue")
        team.score_goal()
        self.assertEqual(team.score, 3, "Scoring a goal should add 3 points to the team's score.")

    # Test case 2: Testing if tagging an opponent transfers the ball correctly
    def test_tag_opponent_for_ball_possession(self):
        team1 = Team("Blue Team", 6, "blue")
        team2 = Team("Red Team", 7, "red")
        player1 = team1.players[0]
        player2 = team2.players[0]
        ball = Ball()
        ball.transfer_possession(player2)
        player1.tag(player2, 120, ball, 20)
        self.assertTrue(player1.has_ball, "After tagging, the ball should be transferred to the tagging player.")

    # Test case 3: Testing if the block-by-tag rule adds an extra point
    def test_block_by_tag_scoring(self):
        team1 = Team("Blue Team", 6, "blue")
        team2 = Team("Red Team", 7, "red")
        player1 = team1.players[0]
        player2 = team2.players[0]
        ball = Ball()
        ball.transfer_possession(player2)
        player1.tag(player2, 200, ball, 3) # within 5 meters of the goal
        self.assertEqual(team1.score, 1, "A successful block-by-tag should add 1 point.")

    #Test case 4: Confirm that a tag outside the radius doesn't give a point
    def test_non_block_by_tag_scoring(self):
        team1 = Team("Blue Team", 6, "blue")
        team2 = Team("Red Team", 7, "red")
        player1 = team1.players[0]
        player2 = team2.players[0]
        ball = Ball()
        ball.transfer_possession(player2)
        player1.tag(player2, 200, ball, 10) # within 5 meters of the goal
        self.assertEqual(team1.score, 0, "A successful block-by-tag should add 1 point.")


    # Test case 5: Testing the band stealing mechanic
    def test_band_stealing(self):
        team1 = Team("Blue Team", 6, "blue")
        team2 = Team("Red Team", 7, "red")
        player1 = team1.players[0]
        player2 = team2.players[0]
        player1.tag(player2, 1000, Ball(), 500)
        self.assertEqual(player1.bands["red"], 1, "The tagging player should steal a red band from the tagged player.")

    # Test case 5: Testing the end-game bonus calculation for captured bands
    def test_end_game_bonus_calculation(self):
        team1 = Team("Blue Team", 6, "blue")
        player1 = team1.players[0]
        # Simulating the player losing all their bands
        player1.bands["blue"] = 0
        game = Game(team1, Team("Red Team", 7, "red"))
        game.end_game()
        self.assertEqual(team1.score, 10, "The team should receive a 10-point bonus for a player with zero bands.")

    # Test case 5: Testing the end-game bonus calculation for captured bands
    def test_tags_too_close_together(self):
        team1 = Team("Blue Team", 6, "blue")
        team2 = Team("Red Team", 7, "red")
        player1 = team1.players[0]
        player2 = team2.players[0]
        ball = Ball()
        player1.tag(player2, 1000, ball, 500)
        player1.tag(player2, 1001, ball, 500)
        self.assertEqual(player1.bands["red"], 1, "If a player tags another two times within 30 seconds, only the first tag should result in a flag steal.")


if __name__ == '__main__':
    unittest.main()
