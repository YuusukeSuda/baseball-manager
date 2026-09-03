class Team:

    def __init__(self, name):
        self.name = name
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def get_players_by_position(self, position):
        return [
            player
            for player in self.players
            if player.position == position
        ]

    def show_info(self):

        print(f"チーム名: {self.name}")

        print("\n【投手】")

        pitchers = self.get_players_by_position("P")

        for player in pitchers:
            print(f"- {player.name}")

        print("\n【野手】")

        for player in self.players:

            if player.position != "P":
                print(f"- {player.name}")