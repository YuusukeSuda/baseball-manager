class Team:
    def __init__(self, name):
        self.name = name
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def show_info(self):
        print(f"チーム名: {self.name}")
        print("所属選手:")

        for player in self.players:
            print(f"- {player.name}")