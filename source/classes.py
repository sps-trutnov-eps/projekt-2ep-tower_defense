import pygame
import math


class Hra:
    def __init__(self, mapa, obtiznost):
        self.mapa = mapa
        self.obtiznost = obtiznost
        self.wave_count = 1
        self.enemies_list = []

        match self.obtiznost:
            case 1:
                self.base_enemy_number = 10
            case 2:
                self.base_enemy_number = 15
            case 3:
                self.base_enemy_number = 20
            case _:
                self.base_enemy_number = 15

    def update_wave_count(self):
        self.wave += 1

    class Nepritel:
        def __init__(self, type):
            self.enemy_type = type

            match self.enemy_type:
                case "normal":
                    self.hp = 4
                    self.speed = 2
                case "fast":
                    self.hp = 1
                    self.speed = 3
                case "tank":
                    self.hp = 10
                    self.speed = 1
                case _:
                    self.hp = 4
                    self.speed = 2

    class Zakladna:
        def __init__(self, obtiznost, x, y):
            match obtiznost:
                case 1:
                    self.hp = 150
                case 2:
                    self.hp = 125
                case 3:
                    self.hp = 100

            self.x = x
            self.y = y

            # kapacita pro střelivo
            self.capacity = 200

    class Spawner:
        def __init__(self, hra_instance, obtiznost, x, y):
            self.hra_instance = hra_instance

            self.x = x
            self.y = y

            self.obtiznost = self.hra_instance.obtiznost
            self.obtiznost_multiplier = self.obtiznost * 0.5

            self.rect = pygame.Rect(self.x, self.y, 25, 25)

        # vygeneruje seznam nepřátel (třída Nepratele)
        def generate_wave(self):
            special_enemies = False
            list_of_enemies = []

            if self.hra_instance.wave_count >= 5:
                special_enemies = True

            total_enemy_number = self.hra_instance.base_enemy_number + self.hra_instance.wave_count * 5

            max_special = 0
            if special_enemies:
                if self.hra_instance.wave_count < 20:
                    max_special = math.ceil(total_enemy_number / 5)
                else:
                    max_special = math.ceil(total_enemy_number / 2)

            normal_enemy_count = total_enemy_number - max_special

            # Generate normal enemies
            for _ in range(normal_enemy_count):
                enemy = self.hra_instance.Nepritel(self.obtiznost, "normal")
                list_of_enemies.append(enemy)

            # Generate special enemies
            for _ in range(max_special):
                special_enemy = self.hra_instance.Nepritel(self.obtiznost, "special")
                list_of_enemies.append(special_enemy)

            return list_of_enemies

        def placeholder_draw(self, window):
            pygame.draw.rect(window, (255, 255, 0), self.rect)

        def spawn_wave(self):
            self.hra_instance.enemies_list.append(self.generate_wave())

    class Doly:     # těžba suroviny, která by byla transportována do základny pro munici
        def __init__(self):
            pass

    class Vesnice:
        def __init__(self):     # usedliště civilistů, kteří by transportovali suroviny do základen
            pass