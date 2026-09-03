import json

from player import Player, Pitch
from team import Team


def main():

    with open("players.json", encoding="utf-8") as file:
        players_data = json.load(file)
    with open("teams.json", encoding="utf-8") as file:
        teams_data = json.load(file)

    players = []
    players_by_id = {}

    for player_data in players_data:

        pitches = []

        for pitch_data in player_data["pitches"]:
            pitch = Pitch(
                name=pitch_data["name"],
                movement=pitch_data["movement"],
                power=pitch_data["power"]
            )

            pitches.append(pitch)

        player = Player(
            player_id=player_data["id"],
            name=player_data["name"],
            age=player_data["age"],
            position=player_data["position"],
            throw_hand=player_data["throw_hand"],
            bat_hand=player_data["bat_hand"],

            contact=player_data["contact"],
            power=player_data["power"],
            eye=player_data["eye"],

            speed=player_data["speed"],
            baserunning=player_data["baserunning"],

            fielding=player_data["fielding"],
            arm_strength=player_data["arm_strength"],
            throwing=player_data["throwing"],

            velocity=player_data["velocity"],
            control=player_data["control"],
            stamina=player_data["stamina"],

            pitches=pitches
        )

        players.append(player)
        players_by_id[player.player_id] = player

    # チーム作成
    teams = []

    for team_data in teams_data:

        team = Team(
            team_data["name"]
        )

        for player_id in team_data["player_ids"]:

            player = players_by_id[player_id]

            team.add_player(player)

        teams.append(team)

    # チーム情報表示
    for team in teams:
        team.show_info()

if __name__ == "__main__":
    main()