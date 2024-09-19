class Zakladna:
    def __init__(self, obtiznost, x, y):
        match obtiznost:
            case 1:
                self.hp = 20
            case 2:
                self.hp = 15
            case 3:
                self.hp = 10

        self.x = x
        self.y = y


class Spawner:
    def __init__(self, obtiznost, x, y):
        self.x = x
        self.y = y
        self.obtiznost = obtiznost


class Doly:     # těžba suroviny, která by byla transportována do základny pro munici
    def __init__(self):
        pass


class Vesnice:
    def __init__(self):     # usedliště civilistů, kteří by transportovali suroviny do základen
        pass