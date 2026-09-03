class Player:
    def __init__(self, name, age, position):
        self.name = name
        self.age = age
        self.position = position

    def show_info(self):
        print(f"名前: {self.name}")
        print(f"年齢: {self.age}")
        print(f"ポジション: {self.position}")