POSITION_NAMES = {
    "P": "投手",
    "C": "捕手",
    "1B": "一塁手",
    "2B": "二塁手",
    "3B": "三塁手",
    "SS": "遊撃手",
    "LF": "左翼手",
    "CF": "中堅手",
    "RF": "右翼手"
}


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

    # チームの総選手数
    def get_player_count(self):
        return len(self.players)

    # 投手数
    def get_pitcher_count(self):
        return len(
            self.get_players_by_position("P")
        )

    # 野手数
    def get_fielder_count(self):
        return (
            self.get_player_count()
            - self.get_pitcher_count()
        )
    def get_player_by_name(self, name):
        for player in self.players:
            if player.name == name:
                return player

        return None
    def get_player_by_id(self, player_id):
        for player in self.players:
            if player.player_id == player_id:
                return player
    
        return None
    def show_info(self):

        print(f"チーム名: {self.name}")

        # 選手数
        print(f"選手数: {self.get_player_count()}")
        print(f"投手: {self.get_pitcher_count()}")
        print(f"野手: {self.get_fielder_count()}")

        # 投手
        print("\n【投手】")

        pitchers = self.get_players_by_position("P")

        for player in pitchers:
            print(
                f"- {player.name}（{POSITION_NAMES[player.position]}）"
            )

        # 捕手
        print("\n【捕手】")

        catchers = self.get_players_by_position("C")

        for player in catchers:
            print(
                f"- {player.name}（{POSITION_NAMES[player.position]}）"
            )

        # 内野手
        print("\n【内野手】")

        infield_positions = ["1B", "2B", "3B", "SS"]

        for player in self.players:
            if player.position in infield_positions:
                print(
                    f"- {player.name}（{POSITION_NAMES[player.position]}）"
                )

        # 外野手
        print("\n【外野手】")

        outfield_positions = ["LF", "CF", "RF"]

        for player in self.players:
            if player.position in outfield_positions:
                print(
                    f"- {player.name}（{POSITION_NAMES[player.position]}）"
                )