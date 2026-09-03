from player import Player
from team import Team


player1 = Player(
    name="田中 太郎",
    age=22,
    position="P"
)

player2 = Player(
    name="佐藤 次郎",
    age=25,
    position="C"
)

player3 = Player(
    name="鈴木 三郎",
    age=20,
    position="CF"
)


team = Team("東京ファルコンズ")

team.add_player(player1)
team.add_player(player2)
team.add_player(player3)


team.show_info()