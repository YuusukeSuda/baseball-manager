class Pitch:
    def __init__(self, name, movement, power):

        if not 1 <= movement <= 10:
            raise ValueError(
                "変化量は1〜10の範囲で設定してください"
            )

        if not 20 <= power <= 100:
            raise ValueError(
                "球威は20〜100の範囲で設定してください"
            )

        self.name = name
        self.movement = movement
        self.power = power

    def __str__(self):
        return (
            f"{self.name} "
            f"(変化量: {self.movement}/10, 球威: {self.power})"
        )


class Player:

    def validate_stat(self, value, stat_name):
        if not 20 <= value <= 100:
            raise ValueError(
                f"{stat_name} は20〜100の範囲で設定してください"
            )

        return value
    def validate_throw_hand(self, throw_hand):
        if throw_hand not in ["R", "L"]:
            raise ValueError(
                "投球利き腕は R または L を設定してください"
            )

        return throw_hand


    def validate_bat_hand(self, bat_hand):
        if bat_hand not in ["R", "L", "S"]:
            raise ValueError(
                "打席は R、L、S のいずれかを設定してください"
            )

        return bat_hand

    def get_throw_hand_label(self):
        hands = {
            "R": "右",
            "L": "左"
        }

        return hands[self.throw_hand]


    def get_bat_hand_label(self):
        hands = {
            "R": "右",
            "L": "左",
            "S": "両"
        }

        return hands[self.bat_hand]
    def __init__(
        self,
        player_id,
        name,
        age,
        position,
        throw_hand,
        bat_hand,
        contact,
        power,
        eye,
        speed,
        baserunning,
        fielding,
        arm_strength,
        throwing,
        velocity,
        control,
        stamina,
        pitches=None
    ):
        self.player_id = player_id
        self.name = name
        self.age = age
        self.position = position
        self.throw_hand = self.validate_throw_hand(throw_hand)
        self.bat_hand = self.validate_bat_hand(bat_hand)
        # 打撃能力
        self.contact = self.validate_stat(contact, "ミート")
        self.power = self.validate_stat(power, "パワー")
        self.eye = self.validate_stat(eye, "選球眼")

        # 走塁能力
        self.speed = self.validate_stat(speed, "走力")
        self.baserunning = self.validate_stat(
            baserunning,
            "走塁"
        )

        # 守備能力
        self.fielding = self.validate_stat(
            fielding,
            "守備"
        )
        self.arm_strength = self.validate_stat(
            arm_strength,
            "肩力"
        )
        self.throwing = self.validate_stat(
            throwing,
            "送球"
        )

       # 投球能力
        self.velocity = velocity

        self.control = (
            self.validate_stat(control, "制球")
            if control is not None
            else None
        )

        self.stamina = (
            self.validate_stat(stamina, "スタミナ")
            if stamina is not None
            else None
        )
        # 変化球
        self.pitches = pitches if pitches is not None else []

    def add_pitch(self, pitch):
        self.pitches.append(pitch)

    def __str__(self):
        throw_hand_label = self.get_throw_hand_label()
        bat_hand_label = self.get_bat_hand_label()
        return (
            f"{self.name} "
            f"({self.age}歳 / {self.position}/"
            f"{throw_hand_label}投{bat_hand_label}打)"
        )
    def show_detail(self):

        print("\n===== 選手詳細 =====")

        print(f"名前: {self.name}")
        print(f"年齢: {self.age}歳")
        print(f"ポジション: {self.position}")
        print(
            f"投球: {self.get_throw_hand_label()}投"
        )
        print(
            f"打席: {self.get_bat_hand_label()}打"
        )

        print("\n【打撃能力】")
        print(f"ミート: {self.contact}")
        print(f"パワー: {self.power}")
        print(f"選球眼: {self.eye}")

        print("\n【走塁能力】")
        print(f"走力: {self.speed}")
        print(f"走塁: {self.baserunning}")

        print("\n【守備能力】")
        print(f"守備: {self.fielding}")
        print(f"肩力: {self.arm_strength}")
        print(f"送球: {self.throwing}")

        # 投手の場合のみ投球能力を表示
        if self.position == "P":

            print("\n【投球能力】")
            print(f"球速: {self.velocity}km/h")
            print(f"制球: {self.control}")
            print(f"スタミナ: {self.stamina}")

            print("\n【変化球】")

            for pitch in self.pitches:
                print(f"- {pitch}")