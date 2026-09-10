import json
import os
import shutil
import random

from player import Player, Pitch
from team import Team, POSITION_NAMES


def main():

    with open("players.json", encoding="utf-8") as file:
        players_data = json.load(file)
    with open("teams.json", encoding="utf-8") as file:
        teams_data = json.load(file)

    players = []
    players_by_id = {}
    # 元の JSON データ辞書を id で参照できるようにする
    players_data_by_id = {p["id"]: p for p in players_data}

    for player_data in players_data:

        pitches = []

        for pitch_data in player_data.get("pitches", []):
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

            velocity=player_data.get("velocity"),
            control=player_data.get("control"),
            stamina=player_data.get("stamina"),

            pitches=pitches,
            plate_appearances=player_data.get("plate_appearances", player_data.get("ab", 0)),
            at_bats=player_data.get("at_bats", player_data.get("ab", 0)),
            hits=player_data.get("hits", player_data.get("h", 0)),
            runs_batted_in=player_data.get("runs_batted_in", 0)
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

    # チーム選択
    print("\n====================")
    print("チーム選択")
    print("====================")

    for index, team in enumerate(teams, start=1):
        print(f"{index}: {team.name}")

    while True:

        team_choice = input(
            "\nチーム番号を入力してください: "
        )

        try:
            team_number = int(team_choice)

            if 1 <= team_number <= len(teams):
                break

            print(
                f"1〜{len(teams)} の番号を入力してください"
            )

        except ValueError:
            print("数字を入力してください")

    selected_team = teams[team_number - 1]

    print(f"\n選択したチーム: {selected_team.name}")

    # 選手検索を繰り返す
    while True:

        print("\n====================")
        print("選手検索")
        print("====================")

        print("\n検索方法を選択してください")
        print("1: 名前で検索")
        print("2: IDで検索")
        print("3: チームを変更")
        print("4: ポジションで検索")
        print("5: 能力値ランキング")
        print("6: 選手データ編集")
        print("7: 新しい選手を追加")
        print("8: 選手を移籍/削除")
        print("9: スターティングメンバー設定")
        print("10: 投手ローテーション設定")
        print("11: 試合シミュレーション")
        print("0: 終了")

        choice = input("\n> ")

        # 終了
        if choice == "0":
            print("\n検索を終了します")
            break

        # 名前検索
        elif choice == "1":

            search_name = input(
                "選手名を入力してください: "
            )

            player = selected_team.get_player_by_name(
                search_name
            )

            if player is not None:
                player.show_detail()
            else:
                print("選手が見つかりませんでした")

        # ID検索
        elif choice == "2":

            while True:

                search_id_input = input(
                    "選手IDを入力してください: "
                )

                try:
                    search_id = int(search_id_input)
                    break

                except ValueError:
                    print("数字を入力してください")

            player = selected_team.get_player_by_id(
                search_id
            )

            if player is not None:
                player.show_detail()
            else:
                print("選手が見つかりませんでした")

        # チーム変更
        elif choice == "3":

            print("\n====================")
            print("チーム変更")
            print("====================")

            for index, team in enumerate(teams, start=1):
                print(f"{index}: {team.name}")

            while True:

                team_choice = input(
                    "\nチーム番号を入力してください: "
                )

                try:
                    team_number = int(team_choice)

                    if 1 <= team_number <= len(teams):
                        break

                    print(
                        f"1〜{len(teams)} の番号を入力してください"
                    )

                except ValueError:
                    print("数字を入力してください")

            selected_team = teams[team_number - 1]

            print(f"\n選択したチーム: {selected_team.name}")

        # ポジション検索
        elif choice == "4":

            print("\n====================")
            print("ポジション検索")
            print("====================")

            pos_items = list(POSITION_NAMES.items())

            for index, (code, jp_name) in enumerate(pos_items, start=1):
                print(f"{index}: {jp_name} ({code})")

            while True:

                pos_choice = input(
                    "\n検索するポジションの番号を入力してください: "
                )

                try:
                    pos_number = int(pos_choice)

                    if 1 <= pos_number <= len(pos_items):
                        break

                    print(f"1〜{len(pos_items)} の番号を入力してください")

                except ValueError:
                    print("数字を入力してください")

            position_code = pos_items[pos_number - 1][0]

            players = selected_team.get_players_by_position(position_code)

            print(f"\n{selected_team.name} の {POSITION_NAMES[position_code]} 一覧")

            if players:
                for p in players:
                    print(f"- {p.name} (ID: {p.player_id})")
            else:
                print("該当する選手はいませんでした")

        # 能力値ランキング
        elif choice == "5":

            print("\n====================")
            print("能力値ランキング")
            print("====================")

            stats = [
                ("contact", "ミート"),
                ("power", "パワー"),
                ("speed", "走力"),
                ("fielding", "守備"),
                ("velocity", "球速 (投手のみ)"),
                ("control", "制球 (投手のみ)")
            ]

            for index, (_, label) in enumerate(stats, start=1):
                print(f"{index}: {label}")
            print("0: 戻る")

            while True:
                stat_choice = input("\n> ")
                try:
                    stat_number = int(stat_choice)
                except ValueError:
                    print("数字を入力してください")
                    continue

                if stat_number == 0:
                    break

                if 1 <= stat_number <= len(stats):
                    key, label = stats[stat_number - 1]

                    # チーム内の選手を並べ替え
                    ranked = [
                        p for p in selected_team.players
                        if getattr(p, key, None) is not None
                    ]

                    ranked.sort(key=lambda x: getattr(x, key, 0), reverse=True)

                    print(f"\n{selected_team.name} の {label} ランキング")

                    for i, p in enumerate(ranked[:10], start=1):
                        value = getattr(p, key, "-")
                        suffix = "km/h" if key == "velocity" else ""
                        print(f"{i}位 {p.name} {value}{suffix}")

                    break
                else:
                    print(f"1〜{len(stats)} の番号を入力してください")

        # 選手データ編集
        elif choice == "6":

            print("\n====================")
            print("選手データ編集")
            print("====================")

            print("検索方法を選択してください")
            print("1: 名前で検索")
            print("2: IDで検索")

            sub_choice = input("\n> ")

            target = None

            if sub_choice == "1":
                name = input("選手名を入力してください: ")
                target = selected_team.get_player_by_name(name)
            elif sub_choice == "2":
                while True:
                    sid = input("選手IDを入力してください: ")
                    try:
                        sid_i = int(sid)
                        break
                    except ValueError:
                        print("数字を入力してください")
                target = selected_team.get_player_by_id(sid_i)
            else:
                print("1 または 2 を入力してください")
                continue

            if target is None:
                print("選手が見つかりませんでした")
                continue

            target.show_detail()

            editable = [
                ("name", "名前"),
                ("age", "年齢"),
                ("position", "ポジション"),
                ("throw_hand", "投球利き腕"),
                ("bat_hand", "打席"),
                ("contact", "ミート"),
                ("power", "パワー"),
                ("eye", "選球眼"),
                ("speed", "走力"),
                ("baserunning", "走塁"),
                ("fielding", "守備"),
                ("arm_strength", "肩力"),
                ("throwing", "送球"),
                ("velocity", "球速"),
                ("control", "制球"),
                ("stamina", "スタミナ")
            ]

            for i, (_, label) in enumerate(editable, start=1):
                print(f"{i}: {label}")
            print("0: キャンセル")

            while True:
                f_choice = input("変更する項目番号を入力してください: ")
                try:
                    f_num = int(f_choice)
                except ValueError:
                    print("数字を入力してください")
                    continue

                if f_num == 0:
                    break

                if 1 <= f_num <= len(editable):
                    attr, label = editable[f_num - 1]
                    new_val = input(f"新しい {label} を入力してください: ")

                    try:
                        # 型変換とバリデーション
                        if attr in ("age",):
                            new_val_cast = int(new_val)
                            setattr(target, attr, new_val_cast)
                        elif attr in ("throw_hand",):
                            target.throw_hand = target.validate_throw_hand(new_val)
                        elif attr in ("bat_hand",):
                            target.bat_hand = target.validate_bat_hand(new_val)
                        elif attr == "position":
                            if new_val not in POSITION_NAMES:
                                raise ValueError("無効なポジションコードです")
                            target.position = new_val
                        elif attr in ("name",):
                            target.name = new_val
                        else:
                            # それ以外は能力値として整数で validate_stat を使う
                            new_int = int(new_val)
                            # velocity は投手特有で validate_stat 用外
                            if attr == "velocity":
                                target.velocity = new_int
                            else:
                                target.validate_stat(new_int, label)
                                setattr(target, attr, new_int)

                        # JSON 側の更新
                        pdata = players_data_by_id.get(target.player_id)
                        if pdata is not None:
                            # 特別扱い: attribute 名は players.json と一致
                            pdata[attr] = getattr(target, attr)

                        # バックアップを作成して保存
                        try:
                            if os.path.exists("players.json"):
                                shutil.copyfile("players.json", "players.json.bak")
                        except Exception:
                            pass

                        with open("players.json", "w", encoding="utf-8") as f:
                            json.dump(players_data, f, ensure_ascii=False, indent=4)

                        print("保存しました")

                        # 編集後に選択チームとチーム一覧を再表示
                        print("\n=== 更新後の選手・チーム情報 ===")
                        try:
                            selected_team.show_info()
                        except Exception:
                            pass

                        print("\nチーム一覧")
                        for t in teams:
                            print(f"- {t.name}: {t.get_player_count()} 選手")

                        break

                    except ValueError as e:
                        print(f"入力エラー: {e}")
                        continue

                else:
                    print(f"1〜{len(editable)} の番号を入力してください")

        # 新しい選手の追加
        elif choice == "7":

            print("\n====================")
            print("新しい選手を追加")
            print("====================")

            # 新しいIDは既存の最大ID + 1
            max_id = max((p["id"] for p in players_data), default=0)
            new_id = max_id + 1

            name = input("名前: ")

            while True:
                age_in = input("年齢: ")
                try:
                    age = int(age_in)
                    break
                except ValueError:
                    print("数字を入力してください")

            # ポジション選択
            pos_items = list(POSITION_NAMES.items())
            for index, (code, jp_name) in enumerate(pos_items, start=1):
                print(f"{index}: {jp_name} ({code})")

            while True:
                pos_choice = input("ポジション番号: ")
                try:
                    pos_num = int(pos_choice)
                    if 1 <= pos_num <= len(pos_items):
                        position = pos_items[pos_num - 1][0]
                        break
                    print(f"1〜{len(pos_items)} の番号を入力してください")
                except ValueError:
                    print("数字を入力してください")

            # 利き手
            while True:
                throw_hand = input("投球利き腕 (R/L): ").upper()
                if throw_hand in ("R", "L"):
                    break
                print("R または L を入力してください")

            while True:
                bat_hand = input("打席 (R/L/S): ").upper()
                if bat_hand in ("R", "L", "S"):
                    break
                print("R、L、S のいずれかを入力してください")

            def ask_stat(label, allow_none=False):
                while True:
                    v = input(f"{label} (20-100){' または空で未設定' if allow_none else ''}: ")
                    if allow_none and v.strip() == "":
                        return None
                    try:
                        vi = int(v)
                        if 20 <= vi <= 100:
                            return vi
                        print("20〜100の範囲で入力してください")
                    except ValueError:
                        print("数字を入力してください")

            contact = ask_stat("ミート")
            power = ask_stat("パワー")
            eye = ask_stat("選球眼")

            speed = ask_stat("走力")
            baserunning = ask_stat("走塁")

            fielding = ask_stat("守備")
            arm_strength = ask_stat("肩力")
            throwing = ask_stat("送球")

            velocity = None
            control = None
            stamina = None
            pitches = []

            if position == "P":
                while True:
                    v_in = input("球速 (km/h)、または空で未設定: ")
                    if v_in.strip() == "":
                        velocity = None
                        break
                    try:
                        velocity = int(v_in)
                        break
                    except ValueError:
                        print("数字を入力してください")

                control = ask_stat("制球", allow_none=True)
                stamina = ask_stat("スタミナ", allow_none=True)

                # 変化球追加
                add_p = input("変化球を追加しますか？ (y/n): ").lower()
                while add_p == "y":
                    pname = input("変化球名: ")
                    while True:
                        try:
                            pm = int(input("変化量 (1-10): "))
                            if 1 <= pm <= 10:
                                break
                            print("1〜10を入力してください")
                        except ValueError:
                            print("数字を入力してください")
                    while True:
                        try:
                            pp = int(input("球威 (20-100): "))
                            if 20 <= pp <= 100:
                                break
                            print("20〜100を入力してください")
                        except ValueError:
                            print("数字を入力してください")

                    pitches.append({"name": pname, "movement": pm, "power": pp})
                    add_p = input("さらに追加しますか？ (y/n): ").lower()

            # 新規 player dict
            new_player_data = {
                "id": new_id,
                "name": name,
                "age": age,
                "position": position,
                "throw_hand": throw_hand,
                "bat_hand": bat_hand,
                "contact": contact,
                "power": power,
                "eye": eye,
                "speed": speed,
                "baserunning": baserunning,
                "fielding": fielding,
                "arm_strength": arm_strength,
                "throwing": throwing,
                "plate_appearances": 0,
                "at_bats": 0,
                "hits": 0,
                "runs_batted_in": 0,
            }

            if velocity is not None:
                new_player_data["velocity"] = velocity
            if control is not None:
                new_player_data["control"] = control
            if stamina is not None:
                new_player_data["stamina"] = stamina
            if pitches:
                new_player_data["pitches"] = pitches

            # メモリに追加
            players_data.append(new_player_data)
            players_data_by_id[new_id] = new_player_data

            # Player オブジェクトを作成して追加
            player_obj = Player(
                player_id=new_player_data["id"],
                name=new_player_data["name"],
                age=new_player_data["age"],
                position=new_player_data["position"],
                throw_hand=new_player_data["throw_hand"],
                bat_hand=new_player_data["bat_hand"],
                contact=new_player_data["contact"],
                power=new_player_data["power"],
                eye=new_player_data["eye"],
                speed=new_player_data["speed"],
                baserunning=new_player_data["baserunning"],
                fielding=new_player_data["fielding"],
                arm_strength=new_player_data["arm_strength"],
                throwing=new_player_data["throwing"],
                velocity=new_player_data.get("velocity"),
                control=new_player_data.get("control"),
                stamina=new_player_data.get("stamina"),
                pitches=[Pitch(p["name"], p["movement"], p["power"]) for p in new_player_data.get("pitches", [])],
                plate_appearances=new_player_data.get("plate_appearances", 0),
                at_bats=new_player_data.get("at_bats", 0),
                hits=new_player_data.get("hits", 0),
                runs_batted_in=new_player_data.get("runs_batted_in", 0)
            )

            players.append(player_obj)
            players_by_id[player_obj.player_id] = player_obj

            # どのチームに追加するか
            print("チームに追加しますか？")
            for idx, t in enumerate(teams, start=1):
                print(f"{idx}: {t.name}")
            print("0: 追加しない")

            while True:
                t_choice = input("> ")
                try:
                    t_num = int(t_choice)
                except ValueError:
                    print("数字を入力してください")
                    continue
                if t_num == 0:
                    chosen_team = None
                    break
                if 1 <= t_num <= len(teams):
                    chosen_team = teams[t_num - 1]
                    break
                print(f"1〜{len(teams)} の番号を入力してください")

            if chosen_team is not None:
                chosen_team.add_player(player_obj)
                # teams_data 側にも追加
                for td in teams_data:
                    if td["name"] == chosen_team.name:
                        td.setdefault("player_ids", []).append(new_id)
                        break

            # 保存: players.json と teams.json
            try:
                if os.path.exists("players.json"):
                    shutil.copyfile("players.json", "players.json.bak")
            except Exception:
                pass

            with open("players.json", "w", encoding="utf-8") as f:
                json.dump(players_data, f, ensure_ascii=False, indent=4)

            try:
                if os.path.exists("teams.json"):
                    shutil.copyfile("teams.json", "teams.json.bak")
            except Exception:
                pass

            with open("teams.json", "w", encoding="utf-8") as f:
                json.dump(teams_data, f, ensure_ascii=False, indent=4)

            print("選手を追加しました")

            # 追加後に表示更新
            print("\n=== 更新後の選手・チーム情報 ===")
            try:
                selected_team.show_info()
            except Exception:
                pass
            print("\nチーム一覧")
            for t in teams:
                print(f"- {t.name}: {t.get_player_count()} 選手")

        # 試合シミュレーション
        elif choice == "11":

            print("\n====================")
            print("試合シミュレーション")
            print("====================")

            # 対戦相手を選択
            print("対戦相手を選んでください")
            for idx, t in enumerate(teams, start=1):
                print(f"{idx}: {t.name}")
            while True:
                opp_in = input("> ")
                try:
                    opp_num = int(opp_in)
                    if 1 <= opp_num <= len(teams):
                        opponent = teams[opp_num - 1]
                        break
                    print(f"1〜{len(teams)} の番号を入力してください")
                except ValueError:
                    print("数字を入力してください")

            # 両チームのスタメンを用意
            def ensure_lineup(team):
                if not hasattr(team, 'starting_lineup') or not team.starting_lineup:
                    # teams_data にあれば反映
                    for td in teams_data:
                        if td["name"] == team.name and "starting_lineup" in td:
                            team.starting_lineup = td["starting_lineup"]
                            break
                if not hasattr(team, 'starting_lineup') or not team.starting_lineup:
                    # 自動で上位9人を選ぶ
                    team.starting_lineup = [p.player_id for p in team.players[:9]]

            ensure_lineup(selected_team)
            ensure_lineup(opponent)

            # ローテの先発を用意
            def get_starter(team, inning):
                # rotation attribute expected
                rot = getattr(team, 'rotation', None)
                if not rot:
                    for td in teams_data:
                        if td["name"] == team.name and "rotation" in td:
                            team.rotation = td["rotation"]
                            rot = team.rotation
                            break
                if rot:
                    return players_by_id.get(rot[(inning-1) % len(rot)])
                # それ以外はチームの先頭投手
                for p in team.players:
                    if p.position == 'P':
                        return p
                return None

            innings = 9
            score_a = 0
            score_b = 0

            for inning in range(1, innings+1):
                # selected_team攻撃、opponent投手
                a_pitcher = get_starter(opponent, inning)
                b_pitcher = get_starter(selected_team, inning)

                def team_offense_score(team):
                    ids = getattr(team, 'starting_lineup', [])
                    bats = [players_by_id.get(pid) for pid in ids if players_by_id.get(pid) is not None]
                    if not bats:
                        bats = team.players
                    s = 0
                    for b in bats:
                        s += (b.contact or 0) + (b.power or 0) * 0.5
                    return s / max(1, len(bats))

                a_off = team_offense_score(selected_team)
                b_off = team_offense_score(opponent)
                # 打席単位で処理する簡易シミュレーション関数群
                def simulate_at_bat(batter, pitcher):
                    # 打者スコア
                    batter_score = (
                        (batter.contact or 50) * 0.6 +
                        (batter.power or 50) * 0.2 +
                        (batter.eye or 50) * 0.2
                    )

                    pitcher_score = 0
                    if pitcher is not None:
                        pitcher_score = (
                            (pitcher.control or 50) * 0.5 +
                            (pitcher.velocity or 140) * 0.3
                        )

                    # 簡易確率: 四球と三振を含めた判定
                    # 四球確率（低め）
                    walk_prob = max(0.01, ((batter.eye or 50) - (pitcher.control or 50)) / 500.0 + 0.02)
                    # 三振確率（バッターのミートが低いほど高くなる）
                    strikeout_prob = max(0.02, (70 - (batter.contact or 50)) / 300.0)

                    # ヒット期待値
                    if batter_score + pitcher_score <= 0:
                        hit_probability = 0.0
                    else:
                        hit_probability = batter_score / (batter_score + pitcher_score)

                    r = random.random()
                    if r < walk_prob:
                        return "walk"
                    # 判定: ヒットかアウト
                    if r < walk_prob + hit_probability:
                        # ヒットが出た場合、長打の確率を簡易計算
                        hr_thresh = 0.03
                        double_thresh = 0.12
                        rr = random.random()
                        if rr < hr_thresh:
                            return "home_run"
                        if rr < double_thresh:
                            return "double"
                        return "single"
                    # 三振判定
                    if r < walk_prob + hit_probability + strikeout_prob:
                        return "strikeout"
                    return "out"

                def update_batting_stats(p_obj, pdata, result, rbi=0):
                    # plate appearance は常に増える
                    p_obj.plate_appearances = getattr(p_obj, 'plate_appearances', 0) + 1
                    pdata['plate_appearances'] = pdata.get('plate_appearances', 0) + 1

                    # 四球は打数に含めない
                    if result != "walk":
                        p_obj.at_bats = getattr(p_obj, 'at_bats', 0) + 1
                        pdata['at_bats'] = pdata.get('at_bats', 0) + 1

                    if result in ("single", "double", "home_run"):
                        p_obj.hits = getattr(p_obj, 'hits', 0) + 1
                        pdata['hits'] = pdata.get('hits', 0) + 1

                    if rbi:
                        p_obj.runs_batted_in = getattr(p_obj, 'runs_batted_in', 0) + rbi
                        pdata['runs_batted_in'] = pdata.get('runs_batted_in', 0) + rbi

                def init_game_batting_stats(team):
                    stats = {}
                    for p in team.players:
                        stats[p.player_id] = {
                            'name': p.name,
                            'plate_appearances': 0,
                            'at_bats': 0,
                            'hits': 0,
                            'runs_batted_in': 0,
                        }
                    return stats

                def update_game_batting_stats(stats, p_obj, result, rbi=0):
                    if stats is None:
                        return

                    pid = p_obj.player_id
                    entry = stats.setdefault(pid, {
                        'name': p_obj.name,
                        'plate_appearances': 0,
                        'at_bats': 0,
                        'hits': 0,
                        'runs_batted_in': 0,
                    })

                    entry['plate_appearances'] += 1
                    if result != 'walk':
                        entry['at_bats'] += 1
                    if result in ('single', 'double', 'home_run'):
                        entry['hits'] += 1
                    if rbi:
                        entry['runs_batted_in'] += rbi

                def print_game_batting_summary(title, stats):
                    print(f"\n=== {title} ===")
                    found = False
                    for pid, entry in sorted(stats.items(), key=lambda kv: kv[0]):
                        if entry['plate_appearances'] == 0 and entry['at_bats'] == 0 and entry['hits'] == 0 and entry['runs_batted_in'] == 0:
                            continue

                        found = True
                        print(
                            f"{entry['name']}: "
                            f"打数 {entry['at_bats']} "
                            f"安打 {entry['hits']} "
                            f"打点 {entry['runs_batted_in']}"
                        )

                    if not found:
                        print("本試合で打席はありません")

                def advance_runners(result, batter_id, bases, defense_team):
                    """
                    打席結果に応じてランナーを進塁させる。

                    bases:
                        [1塁, 2塁, 3塁]
                        各要素は player_id または None

                    戻り値:
                        new_bases: 進塁後の塁状況
                        runs_scored: 今回の打席で入った得点
                    """

                    def runner_home_chance(runner_id, result, defense_team):
                        runner = players_by_id.get(runner_id)

                        if runner is None:
                            return 0.0

                        # =========================
                        # 走者側の能力
                        # =========================
                        runner_score = (
                            (runner.speed or 50) * 0.5
                            + (runner.baserunning or 50) * 0.5
                        )

                        # 50を平均値として基本進塁率を設定
                        chance = 0.20 + (runner_score - 50) * 0.01

                        # =========================
                        # 打球結果による補正
                        # =========================
                        if result == "double":
                            chance += 0.15

                        # =========================
                        # 守備側の肩・送球能力
                        # =========================
                        if defense_team is not None:
                            defenders = [
                                p for p in defense_team.players
                                if p.position != "P"
                            ]

                            defensive_scores = []
                            for defender in defenders:
                                arm = defender.arm_strength or 50
                                throwing = defender.throwing or 50

                                defensive_score = (
                                    arm * 0.5
                                    + throwing * 0.5
                                )

                                defensive_scores.append(defensive_score)

                            # 守備側の上位3人を基準にする
                            if defensive_scores:
                                defensive_scores.sort(reverse=True)
                                top_defenders = defensive_scores[:3]
                                defense_score = sum(top_defenders) / len(top_defenders)
                            else:
                                defense_score = 50
                        else:
                            defense_score = 50

                        # =========================
                        # 守備力による補正
                        # =========================
                        # 守備力50を基準
                        # 守備力が高いほど進塁成功率を下げる
                        defense_penalty = (defense_score - 50) * 0.005
                        chance -= defense_penalty

                        # 最低5%、最高70%
                        return max(0.05, min(0.70, chance))

                    first, second, third = bases
                    runs_scored = 0

                    if result == "single":
                        if third is not None:
                            runs_scored += 1

                        next_first = batter_id
                        next_second = first
                        next_third = None

                        if second is not None:
                            if random.random() < runner_home_chance(
                                second,
                                result,
                                defense_team
                            ):
                                runs_scored += 1
                            else:
                                next_third = second

                        new_bases = [
                            next_first,
                            next_second,
                            next_third
                        ]

                    elif result == "double":
                        if third is not None:
                            runs_scored += 1

                        if second is not None:
                            runs_scored += 1

                        next_first = None
                        next_second = batter_id
                        next_third = None

                        if first is not None:
                            if random.random() < runner_home_chance(
                                first,
                                result,
                                defense_team
                            ):
                                runs_scored += 1
                            else:
                                next_third = first

                        new_bases = [
                            next_first,
                            next_second,
                            next_third
                        ]

                    elif result == "home_run":
                        runs_scored = sum(
                            1 for base in bases
                            if base is not None
                        ) + 1

                        new_bases = [
                            None,
                            None,
                            None
                        ]

                    elif result == "walk":
                        if (
                            first is not None
                            and second is not None
                            and third is not None
                        ):
                            runs_scored = 1

                        new_bases = [
                            batter_id,
                            first,
                            second
                        ]

                    else:
                        new_bases = bases.copy()

                    return new_bases, runs_scored

                def simulate_half(batting_team, pitcher, defense_team, game_stats=None):
                    # returns runs scored this half
                    outs = 0
                    runs = 0
                    # bases[0]=1st, [1]=2nd, [2]=3rd store player_id or None
                    bases = [None, None, None]

                    lineup = getattr(batting_team, 'starting_lineup', [])
                    if not lineup:
                        lineup = [p.player_id for p in batting_team.players]

                    # maintain batting order across innings
                    idx = getattr(batting_team, 'bat_index', 0)
                    while outs < 3:
                        pid = lineup[idx % len(lineup)]
                        idx += 1
                        p_obj = players_by_id.get(pid)
                        pdata = players_data_by_id.get(pid)
                        if p_obj is None or pdata is None:
                            # skip invalid
                            continue

                        result = simulate_at_bat(p_obj, pitcher)

                        if result in ("single", "double", "home_run", "walk"):
                            bases, scored = advance_runners(
                                result,
                                pid,
                                bases,
                                defense_team
                            )

                            runs += scored

                            update_batting_stats(
                                p_obj,
                                pdata,
                                result,
                                rbi=scored
                            )
                            update_game_batting_stats(
                                game_stats,
                                p_obj,
                                result,
                                rbi=scored
                            )

                        elif result == "strikeout":
                            update_batting_stats(
                                p_obj,
                                pdata,
                                "strikeout"
                            )
                            update_game_batting_stats(
                                game_stats,
                                p_obj,
                                "strikeout"
                            )
                            outs += 1

                        else:
                            update_batting_stats(
                                p_obj,
                                pdata,
                                "out"
                            )
                            update_game_batting_stats(
                                game_stats,
                                p_obj,
                                "out"
                            )
                            outs += 1

                    batting_team.bat_index = idx % len(lineup)
                    return runs

                game_stats_a = init_game_batting_stats(selected_team)
                game_stats_b = init_game_batting_stats(opponent)

                ra = simulate_half(
                    selected_team,
                    a_pitcher,
                    opponent,
                    game_stats_a
                )

                rb = simulate_half(
                    opponent,
                    b_pitcher,
                    selected_team,
                    game_stats_b
                )

                score_a += ra
                score_b += rb

                print(f"{inning}回表 {selected_team.name} 得点: {ra}  ／  {opponent.name} 得点: {rb}")

            print("\n=== 試合終了 ===")
            print(f"{selected_team.name} {score_a} - {score_b} {opponent.name}")

            print_game_batting_summary(f"{selected_team.name} 今回の打撃成績", game_stats_a)
            print_game_batting_summary(f"{opponent.name} 今回の打撃成績", game_stats_b)

            # 進塁ロジックの簡易テスト
            print("\n=== 進塁ロジック確認（簡易テスト） ===")
            test_bases = [10, None, None]
            test_result = "single"
            test_new_bases, test_runs = advance_runners(
                test_result,
                99,
                test_bases,
                opponent
            )
            print(f"単打テスト: bases={test_bases} -> {test_new_bases}, 得点={test_runs}")

            test_bases_2 = [None, 10, None]
            test_new_bases_2, test_runs_2 = advance_runners(
                "double",
                77,
                test_bases_2,
                opponent
            )
            print(f"二塁打テスト: bases={test_bases_2} -> {test_new_bases_2}, 得点={test_runs_2}")

            # 試合結果を players.json に反映して保存（バックアップを作成）
            # updated は直前のイニングで変更された選手を保持している可能性がある
            try:
                if os.path.exists("players.json"):
                    shutil.copyfile("players.json", "players.json.bak")
            except Exception:
                pass

            with open("players.json", "w", encoding="utf-8") as f:
                json.dump(players_data, f, ensure_ascii=False, indent=4)

            # 通算成績を表示
            print("\n=== 通算成績 ===")
            print(f"【{selected_team.name}】")
            for pid, pdata in players_data_by_id.items():
                if pdata.get('at_bats', 0) > 0 or pdata.get('hits', 0) > 0:
                    if pid in [p.player_id for p in selected_team.players]:
                        name = pdata.get('name')
                        rbi = pdata.get('runs_batted_in', 0)
                        print(f"{name}: 打数 {pdata.get('at_bats',0)} 安打 {pdata.get('hits',0)} 打点 {rbi}")

            print(f"\n【{opponent.name}】")
            for pid, pdata in players_data_by_id.items():
                if pdata.get('at_bats', 0) > 0 or pdata.get('hits', 0) > 0:
                    if pid in [p.player_id for p in opponent.players]:
                        name = pdata.get('name')
                        rbi = pdata.get('runs_batted_in', 0)
                        print(f"{name}: 打数 {pdata.get('at_bats',0)} 安打 {pdata.get('hits',0)} 打点 {rbi}")

        # スターティングメンバー設定
        elif choice == "9":

            print("\n====================")
            print("スターティングメンバー設定")
            print("====================")

            # チームは selected_team を使う
            print(f"設定対象チーム: {selected_team.name}")

            # 表示
            for p in selected_team.players:
                print(f"ID:{p.player_id} - {p.name} ({p.position})")

            lineup = []
            print("1番から9番まで選手IDを順に入力してください (空で終了):")
            for slot in range(1, 10):
                while True:
                    entry = input(f"{slot}番: ")
                    if entry.strip() == "":
                        break
                    try:
                        pid = int(entry)
                    except ValueError:
                        print("数字を入力してください")
                        continue
                    if pid in [p.player_id for p in selected_team.players]:
                        if pid in lineup:
                            print("すでに選択されています")
                            continue
                        lineup.append(pid)
                        break
                    else:
                        print("そのIDの選手はチームにいません")
                if entry.strip() == "":
                    break

            # teams_data に保存
            for td in teams_data:
                if td["name"] == selected_team.name:
                    td["starting_lineup"] = lineup
                    break

            try:
                if os.path.exists("teams.json"):
                    shutil.copyfile("teams.json", "teams.json.bak")
            except Exception:
                pass
            with open("teams.json", "w", encoding="utf-8") as f:
                json.dump(teams_data, f, ensure_ascii=False, indent=4)

            # 反映: team オブジェクトに属性をセット
            selected_team.starting_lineup = lineup

            print("スターティングメンバーを保存しました")

        # 投手ローテーション設定
        elif choice == "10":

            print("\n====================")
            print("投手ローテーション設定")
            print("====================")

            print(f"設定対象チーム: {selected_team.name}")
            pitchers = [p for p in selected_team.players if p.position == "P"]
            if not pitchers:
                print("このチームに投手がいません")
                continue

            for p in pitchers:
                print(f"ID:{p.player_id} - {p.name} (球速:{p.velocity})")

            rotation = []
            print("ローテーションに入れる投手のIDを順に入力してください (空で終了):")
            while True:
                entry = input("次の投手ID: ")
                if entry.strip() == "":
                    break
                try:
                    pid = int(entry)
                except ValueError:
                    print("数字を入力してください")
                    continue
                if pid in [p.player_id for p in pitchers]:
                    if pid in rotation:
                        print("すでに選択されています")
                        continue
                    rotation.append(pid)
                else:
                    print("そのIDの投手はチームにいません")

            for td in teams_data:
                if td["name"] == selected_team.name:
                    td["rotation"] = rotation
                    break

            try:
                if os.path.exists("teams.json"):
                    shutil.copyfile("teams.json", "teams.json.bak")
            except Exception:
                pass
            with open("teams.json", "w", encoding="utf-8") as f:
                json.dump(teams_data, f, ensure_ascii=False, indent=4)

            selected_team.rotation = rotation
            print("投手ローテーションを保存しました")

        # 選手移籍／削除
        elif choice == "8":

            print("\n====================")
            print("選手移籍・削除")
            print("====================")

            # 選手IDを指定
            while True:
                pid_in = input("処理する選手IDを入力してください: ")
                try:
                    pid = int(pid_in)
                    break
                except ValueError:
                    print("数字を入力してください")

            # 所属チーム検索
            cur_team = None
            for t in teams:
                for p in t.players:
                    if p.player_id == pid:
                        cur_team = t
                        player_obj = p
                        break
                if cur_team:
                    break

            if cur_team is None:
                print("その選手はどのチームにも所属していません")
                # それでも players_data に存在するか確認
                if pid in players_data_by_id:
                    player_obj = players_by_id.get(pid)
                else:
                    print("選手データが見つかりません")
                    continue

            print(f"対象選手: {getattr(player_obj, 'name', '不明')} (現在の所属: {getattr(cur_team, 'name', 'なし')})")
            print("1: 移籍する")
            print("2: チームから削除(フリーエージェント)")
            print("3: データから完全削除")
            sub = input("> ")

            if sub == "1":
                print("移籍先チームを選んでください")
                for idx, t in enumerate(teams, start=1):
                    print(f"{idx}: {t.name}")
                while True:
                    tc = input("> ")
                    try:
                        tnum = int(tc)
                        if 1 <= tnum <= len(teams):
                            new_team = teams[tnum - 1]
                            break
                        print(f"1〜{len(teams)} の番号を入力してください")
                    except ValueError:
                        print("数字を入力してください")

                # 所属チームがあれば削除
                if cur_team is not None:
                    cur_team.players = [p for p in cur_team.players if p.player_id != pid]
                    # teams_data 更新
                    for td in teams_data:
                        if td["name"] == cur_team.name:
                            if "player_ids" in td and pid in td["player_ids"]:
                                td["player_ids"].remove(pid)
                            break

                new_team.add_player(player_obj)
                # teams_data 更新
                for td in teams_data:
                    if td["name"] == new_team.name:
                        td.setdefault("player_ids", []).append(pid)
                        break

                # 保存 teams.json
                try:
                    if os.path.exists("teams.json"):
                        shutil.copyfile("teams.json", "teams.json.bak")
                except Exception:
                    pass
                with open("teams.json", "w", encoding="utf-8") as f:
                    json.dump(teams_data, f, ensure_ascii=False, indent=4)

                print("移籍を完了しました")

            elif sub == "2":
                # チームから削除(フリー化)
                if cur_team is not None:
                    cur_team.players = [p for p in cur_team.players if p.player_id != pid]
                    for td in teams_data:
                        if td["name"] == cur_team.name:
                            if "player_ids" in td and pid in td["player_ids"]:
                                td["player_ids"].remove(pid)
                            break

                    try:
                        if os.path.exists("teams.json"):
                            shutil.copyfile("teams.json", "teams.json.bak")
                    except Exception:
                        pass
                    with open("teams.json", "w", encoding="utf-8") as f:
                        json.dump(teams_data, f, ensure_ascii=False, indent=4)

                    print("チームから削除しました (FA) ")
                else:
                    print("選手はどのチームにも所属していません")

            elif sub == "3":
                # 完全削除: players_data から消す
                # teams_data からも削除
                players_data = [pd for pd in players_data if pd["id"] != pid]
                players_data_by_id.pop(pid, None)
                players = [p for p in players if p.player_id != pid]
                players_by_id.pop(pid, None)

                for td in teams_data:
                    if "player_ids" in td and pid in td["player_ids"]:
                        td["player_ids"].remove(pid)

                # 保存両方
                try:
                    if os.path.exists("players.json"):
                        shutil.copyfile("players.json", "players.json.bak")
                except Exception:
                    pass
                with open("players.json", "w", encoding="utf-8") as f:
                    json.dump(players_data, f, ensure_ascii=False, indent=4)

                try:
                    if os.path.exists("teams.json"):
                        shutil.copyfile("teams.json", "teams.json.bak")
                except Exception:
                    pass
                with open("teams.json", "w", encoding="utf-8") as f:
                    json.dump(teams_data, f, ensure_ascii=False, indent=4)

                print("選手データを完全に削除しました")
            else:
                print("1、2、3 のいずれかを入力してください")


        # その他
        else:
            print("0〜11 のいずれかを入力してください")
    

if __name__ == "__main__":
    main()