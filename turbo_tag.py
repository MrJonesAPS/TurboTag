"""
Module: Turbo Tag Game Simulation

This module simulates a game of Turbo Tag, a dynamic team sport emphasizing strategy and agility. 
It is played on a rectangular field with a goal at each end, involving two teams with a variable number of players. 
The primary objective is to score points through tagging, ball possession, and goal scoring.

Game Rules:

1. Team Composition: Teams can have 5 to 9 players. Each additional player beyond five reduces the team's total band count by 2.
2. Starting the Game: Begins with a jump ball at the center. The team that secures the ball gains initial possession.
3. Scoring Points:

   - Goal Score: Throwing the ball into the opponent's goal scores 3 points.
   - Band Capture: Tagging an opponent allows stealing a band, earning 1 point. If the tagged player holds bands of more than one color, 
     the tagging player steals a band of their own team's color. The tagger only steals a band of the opposing team's color if the tagged player 
     has only bands of that color.
   - End of game bonuses, described below.

4. Tagging Mechanism:

   - Players can tag opponents to steal their bands.
   - A player must wait at least 30 seconds before re-tagging the same opponent.
   - If a tagged player holds the ball, the ball is transferred to the nearest opponent. If this tag occurs within 5 meters of the tagging 
     player's team's goal, the tag is also worth one point (this is called a "block-by-tag").

5. Time Limit: Two 25-minute halves with a break in between.
6. Scoring System:

   - Each goal: 3 points.
   - Each band captured: 1 point.
   - Bonus for capturing all opponent bands: At the end of the game, each player that has zero bands of their own color awards their opponent 10 points.
   - Single color bonus: At the end of the game, each band that a team holds of their opposing team's color is worth an additional bonus point.
"""
#this adds future functionality for type hinting, and avoids having to import typing 
from __future__ import annotations

class Player:
    """Represents a player in the Turbo Tag game.

    Attributes:
        name (str): The name of the player.
        team (Team): The team the player belongs to.
        bands (dict): A dictionary tracking the count of blue and red bands the player has.
        last_tag_time (int or None): The last time the player tagged someone (given in seconds since the start of the game).
        has_ball (bool): Flag indicating whether the player currently has the ball.
    """

    def __init__(self, name: str, team: Team, initial_bands: int):
        """Initializes a Player with a name, team, and initial band counts.

        Args:
            name (str): The name of the player.
            team (str): The name of the team.
            initial_bands (int): The initial number of bands (of the team's color) the player starts with.
        """
        self.name = name
        self.team = team
        if team.team_color == "blue":
            self.bands = {"blue": initial_bands, "red": 0}
        else:
            self.bands = {"blue": 0, "red": initial_bands}
        self.last_tag_time = None
        self.has_ball = False

    def tag(self, opponent: Player, current_time: int, ball: Ball, distance_from_goal: int):
        """Tags an opponent, attempting to steal a band and transfer ball possession.

        Args:
            opponent (Player): The player being tagged.
            current_time (int): The current time (given in seconds since the start of the game).
            ball (Ball): The ball object in the game.
            distance_from_goal (int): used to calculate block-by-tag
        """
        # Check if 30 seconds have passed since last tag
        if current_time - self.last_tag_time >= 30:
            if opponent.team != self.team:
                # Transfer ball if opponent has it
                if opponent.has_ball:
                    ball.transfer_possession(self)
                    # Check for block-by-tag within 5 meters of the goal
                    if distance_from_goal:
                        self.team.score += 1

                # Determine which color band to steal
                #band_color = "red" if self.team == "Home" else "blue"
                band_color = self.team.team_color
                if opponent.bands[band_color] > 0:
                    opponent.bands[band_color] -= 1
                    self.bands[band_color] += 1
                else:
                    opponent.bands[band_color] -= 1
                    self.bands[band_color] += 1

                self.last_tag_time = current_time

class Ball:
    """Represents the ball used in Turbo Tag.

    Attributes:
        current_holder (Player or None): The player currently holding the ball.
    """

    def __init__(self):
        """Initializes the Ball with no current holder."""
        self.current_holder = None

    def transfer_possession(self, new_holder: Player):
        """Transfers possession of the ball to a new holder.

        Args:
            new_holder (Player): The player who is the new holder of the ball.
        """
        if self.current_holder:
            self.current_holder.has_ball = False
        new_holder.has_ball = True
        self.current_holder = new_holder

class Team:
    """Represents a team in the Turbo Tag game.

    Attributes:
        name (str): The name of the team.
        score (int): The current score of the team.
        players (list): A list of Player objects on the team.
        team_color (str): The color of the team's bands.
        opponent (Team): The opposing team
    """

    def __init__(self, name: str, player_count: int, team_color: str):
        """Initializes a Team with a name, number of players, and team color.

        Args:
            name (str): The name of the team.
            player_count (int): The number of players on the team.
            team_color (str): The color of the team's bands.
        """
        self.name = name
        self.score = 0
        self.players: list[Player] = []
        self.team_color = team_color
        self.adjust_band_count(player_count, team_color)
        self.opponent: Team = None #this is set by the game

    def adjust_band_count(self, player_count: int, team_color: str):
        """Adjusts the initial band count for each player based on the team size.

        Args:
            player_count (int): The number of players on the team.
            team_color (str): The color of the team's bands.
        """
        base_bands = 7 - (player_count - 5) * 2
        for _ in range(player_count):
            self.players.append(Player(f"Player_{len(self.players) + 1}", self, base_bands))

    def score_goal(self):
        """Updates the team's score when a goal is scored."""
        self.score += 3

    def calculate_end_game_bonus(self):
        """Calculates and adds end-game bonus points to the team's score."""
        for player in self.opponent.players:
            # Bonus for all opponent bands captured
            if player.bands[player.team.team_color] == 0:
                self.score += 10
            
        # Single color bonus
        for player in self.players:
            self.score += player.bands[self.team_color]

class Game:
    """Represents a game of Turbo Tag.

    Attributes:
        team1 (Team): The first team in the game.
        team2 (Team): The second team in the game.
        ball (Ball): The ball used in the game.
        time_left (int): The time left in the game (in minutes).
    """

    def __init__(self, team1: Team, team2: Team):
        """Initializes a Game with two teams.

        Args:
            team1 (Team): The first team.
            team2 (Team): The second team.
        """
        self.team1 = team1
        self.team1.opponent = team2
        self.team2 = team2
        self.team2.opponent = team1
        self.ball = Ball()
        self.time_left = 50  # minutes
        print(f"Starting an exciting new game of Turbo Tag, featuring {team1.name} vs. {team2.name}" )

    def end_game(self):
        """Ends the game and calculates final scores."""
        self.team1.calculate_end_game_bonus()
        self.team2.calculate_end_game_bonus()
        print("The game is over")
        print(f"Final Score: {self.team1.name} {self.team1.score} - {self.team2.name} {self.team2.score}")


if __name__ == "__main__":
    # Usage example with simplified game setup and flow
    print("""
        Welcome to the world of TurboTag!\n \
        This code includes everything you need to simulate an exciting game\n \
        ...but it includes some bugs. To get started, here's code for a very simple game\n \
        where nothing happens. Why is the score not 0-0?""")
    print
    team1 = Team("Blue", 6, "blue")
    team2 = Team("Red", 7, "red")
    game = Game(team1, team2)

    # Nothing happens the entire game

    #This code ends the game
    game.end_game()

    
    
