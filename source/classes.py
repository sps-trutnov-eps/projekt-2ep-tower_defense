import random
import pygame
import math


class Hra:
    def __init__(self, mapa, obtiznost):
        self.mapa = mapa
        self.obtiznost = obtiznost
        self.wave_count = 0
        self.seznam_entit = []
        self.enemies_list = []
        self.enemies_to_spawn_count = [0, 0, 0]      # normal enemy | fast enemy | tank
        self.seznam_cest = []
        self.aktualni_vlna_dokoncena = True

        # textury       TODO: přidat více textur
        self.nepritel_normal_textura = pygame.image.load("obrazky/nepritel_normal.png")
        self.nepritel_fast_textura = None
        self.nepritel_tank_textura = None

        self.background_textura = None
        self.spawner_textura = None
        self.dul_textura = None
        self.vesnice_textura = None

        self.vez_1_textura = None
        self.vez_2_textura = None

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
        self.wave_count += 1
        self.aktualni_vlna_dokoncena = False

    class Nepritel:
        def __init__(self, typ_nepritele, spawner_location, spawner_side):
            self.typ_nepritele = typ_nepritele
            self.location = [spawner_location[0] + 30, spawner_location[1] + 30]
            self.otocen_na_stranu = spawner_side
            self.rect = pygame.Rect(self.location[0] - (21/2), self.location[1] - (21/2), 27, 27)

            match self.typ_nepritele:
                case "normal":
                    self.hp = 4
                    self.speed = 2
                    self.rect_color = (255, 0, 0)
                case "fast":
                    self.hp = 1
                    self.speed = 3
                    self.rect_color = (255, 255, 0)
                case "tank":
                    self.hp = 10
                    self.speed = 1
                    self.rect_color = (0, 0, 0)
                case _:
                    self.hp = 4
                    self.speed = 2
                    self.rect_color = (255, 0, 0)

        def move(self):
            match self.otocen_na_stranu:
                case "dolu":
                    self.location[1] += self.speed
                case "nahoru":
                    self.location[1] -= self.speed
                case "doprava":
                    self.location[0] += self.speed
                case "doleva":
                    self.location[0] -= self.speed

        def check_for_turn(self, path_list, log):   # TODO: špatná detekce otáčení (přechod z jedné cesty na druhou?)
            for path in path_list:
                if self.rect.colliderect(path.cesta):
                    if self.otocen_na_stranu != path.turn_to:
                        match path.turn_to:
                            case "doleva":
                                self.otocen_na_stranu = "doleva"
                                log.write_to_log("collision detected: doleva")
                            case "doprava":
                                self.otocen_na_stranu = "doprava"
                                log.write_to_log("collision detected: doprava")
                            case "dolu":
                                self.otocen_na_stranu = "dolu"
                                log.write_to_log("collision detected: dolu")
                            case "nahoru":
                                self.otocen_na_stranu = "nahoru"
                                log.write_to_log("collision detected: nahoru")

        def outofbounds_check(self, log):
            if self.location[0] < 0 or self.location[0] > 1200 or self.location[1] < 0 or self.location[1] > 800:
                log.write_to_log("Nepřítel zjištěn mimo mapu")
                log.write_to_log(f"Jeho souřadnice: {self.location}")
                return True
            else:
                return False

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
            self.kapacita_streliva = 200

    class Spawner:
        def __init__(self, hra_instance, location, rotace_spawneru):

            self.location = location
            self.rotace_spawneru = rotace_spawneru      # strany jako do leva, do prava, dolu, nahoru

            self.obtiznost = hra_instance.obtiznost
            self.obtiznost_multiplier = self.obtiznost * 0.5

            self.rect = pygame.Rect(self.location[0], self.location[1], 60, 60)

            self.special_moznosti = ("fast", "tank")

        def make_wave(self, hra):
            seznam_entit = self.generate_wave(hra)
            for enemy in seznam_entit:
                hra.seznam_entit["nepratele"].append(enemy)

        # vygeneruje seznam nepřátel (třída Nepratele)
        def generate_wave(self, hra_instance):
            special_enemies = False
            list_of_enemies = []

            if hra_instance.wave_count >= 5:
                special_enemies = True

            total_enemy_number = hra_instance.base_enemy_number + (hra_instance.wave_count * 5)

            max_special = 0
            if special_enemies:
                if hra_instance.wave_count < 20:
                    max_special = math.ceil(total_enemy_number / 5)
                else:
                    max_special = math.ceil(total_enemy_number / 2)

            normal_enemy_count = total_enemy_number - max_special

            # Generate normal enemies
            for _ in range(normal_enemy_count):
                enemy = hra_instance.Nepritel("normal", self.location, self.rotace_spawneru)
                list_of_enemies.append(enemy)

            # Generate special enemies
            for _ in range(max_special):
                special_enemy = hra_instance.Nepritel(random.choice(self.special_moznosti))
                list_of_enemies.append(special_enemy)

            return list_of_enemies

        def placeholder_draw(self, window):
            pygame.draw.rect(window, (255, 255, 0), self.rect)

        def spawn_wave(self, hra_instance):
            hra_instance.enemies_list.append(self.generate_wave())
            return hra_instance

        def spawn_enemy(self, enemy_type, hra_instance):
            enemy = hra_instance.Nepritel(enemy_type)
            hra_instance.enemies_list.append(enemy)
            return hra_instance

    class Cesta:
        def __init__(self, hra_instance, x, y, sirka, vyska, otocit_se_na):
            self.cesta = pygame.Rect(x, y, sirka, vyska)
            self.turn_to = otocit_se_na

    class Vez:
        def __init__(self, typ, location):
            self.type = typ
            self.location = location

            self.damage = 0
            self.attack_cooldown = 0
            self.radius = 0
            self.list_of_shots = []

            self.testing_rect = None
            self.blittable = None

            self.define_rest_of_stats()

        def define_rest_of_stats(self):
            match self.type:
                case "test_tower":
                    self.damage = 1
                    self.attack_cooldown = 1000     # v milisekundách
                    self.radius = 15
                    self.testing_rect = pygame.Rect(self.location[0], self.location[1], 35, 35)

                case _:     # v případě chyby
                    self.damage = 1
                    self.attack_cooldown = 1000
                    self.radius = 15

        def placement_check(self, hra_instance, location: list):      # will require a check when used, whether it can be placed
            location_rectangle = pygame.Rect(location[0], location[1], 1, 1)
            collides = False

            for cesta in hra_instance.seznam_cest:
                if location_rectangle.collidepoint(cesta):
                    collides = True

            return collides

        def shoot(self):
            pass

    class Doly:     # těžba suroviny, která by byla transportována do základny pro munici
        def __init__(self, hra_instance, location: list):
            self.location = location
            self.ownership = True
            self.rect = pygame.Rect(location[0], location[1], 50, 50)
            self.color = (30, 30, 30)

    class Vesnice:
        def __init__(self, hra_instance, location: list):     # usedliště civilistů, kteří by transportovali suroviny do základen
            self.location = location
            self.ownership = True
            self.rect = pygame.Rect(location[0], location[1], 50, 50)
            self.color = (255, 255, 0)      # pro případy, kdy není žádná textura

        def check_closest_path_point(self, hra_instance):
            check = False
            if check:
                self.ownership = False

    class Logging:
        def __init__(self):
            self.logging = True
            self.log_connection = self.try_open_log()

            self.init_log_session()

        def init_log_session(self):
            log = open("game.log", "a")
            log.write(f"\n\n\n[{self.get_current_time()}] Spouštím hru")
            log.close()

        def get_current_time(self):
            from datetime import datetime
            current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            return current_time

        def try_open_log(self):
            if self.logging:
                try:
                    open("game.log", "r")
                    return True
                except:
                    try:
                        open("game.log", "w")
                        return True
                    except:
                        return False

        def write_to_log(self, message):
            if self.log_connection and self.logging:
                log = open("game.log", "a")
                log.write(f"\n[{str(self.get_current_time())}] {message}")
                log.close()
