import random
import pygame
import math


# noinspection PyTypeChecker
class Hra:
    def __init__(self, mapa, obtiznost):
        self.mapa = mapa
        self.obtiznost = obtiznost
        self.speed_up_multiplier = 1
        self.game_over = False

        self.wave_count = 0
        self.celkova_kapacita_streliva = None
        self.mnozstvi_streliva = 200
        self.penezenka = 150
        self.list_of_buttons = []

        self.seznam_entit = []
        self.enemies_list = []
        self.enemies_to_spawn_count = [0, 0, 0]  # normal enemy | fast enemy | tank
        self.enemies_killed = 0

        self.seznam_cest = []
        self.aktualni_vlna_dokoncena = True

        # textury       TODO: Doplnit texturu nepritel_fast
        self.nepritel_normal_textura = pygame.image.load("obrazky/nepritel_normal.png").convert_alpha()
        self.nepritel_fast_textura = None
        self.nepritel_tank_textura = pygame.transform.scale(pygame.image.load("obrazky/tank.png"), (45, 45)).convert_alpha()
        self.nepritel_boss_textura = pygame.transform.scale(pygame.image.load("obrazky/Boss.png"), (45, 45)).convert_alpha()

        self.background_textura = None
        self.spawner_textura = pygame.transform.scale(pygame.image.load("obrazky/base1.png"), (50, 50)).convert_alpha()
        self.vesnice_textura = pygame.transform.scale(pygame.image.load("obrazky/military-tent.png"), (50, 50)).convert_alpha()

        self.vez_1_textura = pygame.image.load("obrazky/vez_1.png").convert_alpha()
        self.vez_2_textura = pygame.image.load("obrazky/vez_2.png").convert_alpha()
        self.vez_3_textura = pygame.image.load("obrazky/mortar.png").convert_alpha()

        self.side_menu_textura = pygame.image.load("obrazky/postranni_menu.png").convert_alpha()
        self.side_menu_end_action_img = pygame.image.load("obrazky/remove_action.png").convert_alpha()

        match self.obtiznost:
            case 1:
                self.base_enemy_number = 10
            case 2:
                self.base_enemy_number = 15
            case 3:
                self.base_enemy_number = 20

            case _:
                self.base_enemy_number = 15

    def get_max_resource_count(self):
        max_count = 0
        for zakladna in self.seznam_entit["zakladny"]:
            max_count += zakladna.kapacita_streliva
        self.celkova_kapacita_streliva = max_count

        if self.mnozstvi_streliva > self.celkova_kapacita_streliva:
            self.mnozstvi_streliva = self.celkova_kapacita_streliva

    def check_for_loss(self, log):
        zakladna_count = len(self.seznam_entit["zakladny"])
        zakladna_check = []
        for zakladna in self.seznam_entit["zakladny"]:
            if zakladna.fallen:
                zakladna_check.append(zakladna)
        if zakladna_count == len(zakladna_check):
            log.write_to_log(f"Zjištěno padlých základen: {zakladna_count}")
            self.game_over = True

    def update_wave_count(self):
        self.wave_count += 1
        self.aktualni_vlna_dokoncena = False

    def speed_game_up(self, speed):
        for tower in self.seznam_entit["veze"]:
            tower.attack_cooldown /= speed
        for enemy in self.seznam_entit["nepratele"]:
            enemy.speed *= speed

    class Nepritel:
        def __init__(self, typ_nepritele, spawner_location, spawner_side, location_offset, hra_instance):
            """
                Vytvořit nepřítele.

                :type typ_nepritele: str
                :param typ_nepritele: Typ nepřítele (např. normal, fast,..).

                :type spawner_location: list
                :param spawner_location: Umístění spawneru.

                :type spawner_side: str
                :param spawner_side: Strana na kterou je spawner otočen.

                :type location_offset: int
                :param location_offset: Hodnota udávající jak moc má být posunut.
                                        Pozor! Program si sám přizpůsobý + a -.

                :return: Nepřítel
            """

            self.typ_nepritele = typ_nepritele
            self.location = [spawner_location[0] + 20, spawner_location[1] + 20]
            self.otocen_na_stranu = spawner_side
            self.rect = pygame.Rect(self.location[0] - (21 / 2), self.location[1] - (21 / 2), 27, 27)

            # spawn hodnoty
            # při spawnu se budou spawnovat pozadu, podle typu, a až poté, co projdou spawnerem se budou vykreslovat a
            # bude možné na ně střílet
            self.spawned = False
            location_offset += self.rect.width
            self.odmena = 3

            match self.otocen_na_stranu:
                case "dolu":
                    self.location[1] -= location_offset
                case "nahoru":
                    self.location[1] += location_offset
                case "doleva":
                    self.location[0] += location_offset
                case "doprava":
                    self.location[0] -= location_offset

            match self.typ_nepritele:
                case "normal":
                    self.hp = 5
                    self.speed = 2
                    self.rect_color = (255, 0, 0)
                case "fast":
                    self.hp = 2
                    self.speed = 3
                    self.rect_color = (255, 255, 0)
                    self.odmena = 5
                case "tank":
                    self.hp = 50
                    self.speed = 1
                    self.rect_color = (0, 0, 0)
                    self.odmena = 8
                case "boss":
                    self.hp = 500
                    self.speed = 0.5
                    self.rect_color = (255, 0, 255)
                    self.odmena = 250
                case _:
                    self.hp = 4
                    self.speed = 2
                    self.rect_color = (255, 0, 0)

            self.speed = self.speed / 1.5 * hra_instance.speed_up_multiplier

        def utok_na_zakladnu(self, hra_instance, zakladna_int, log):
            hra_instance.seznam_entit["zakladny"][zakladna_int].enemy_attack(self, log)
            hra_instance.seznam_entit["nepratele"].remove(self)

        def utok_na_vesnici(self, hra_instance, vesnice_int, log):
            hra_instance.seznam_entit["vesnice"][vesnice_int].enemy_attack(self, log)
            hra_instance.seznam_entit["nepratele"].remove(self)

        def check_to_spawn(self, spawners):
            for spawner in spawners:
                if self.rect.colliderect(spawner):
                    match self.otocen_na_stranu:
                        case "dolu":
                            if self.rect.y > spawner.rect.y:
                                self.spawned = True
                        case "nahoru":
                            if self.rect.y < spawner.rect.bottom:
                                self.spawned = True
                        case "doleva":
                            if self.rect.x < spawner.rect.right:
                                self.spawned = True
                        case "doprava":
                            if self.rect.x > spawner.rect.x:
                                self.spawned = True

        def move(self):  # Nový, nefunguje, jsou v sobě
            match self.otocen_na_stranu:
                case "dolu":
                    self.location[1] += self.speed
                case "nahoru":
                    self.location[1] -= self.speed
                case "doprava":
                    self.location[0] += self.speed
                case "doleva":
                    self.location[0] -= self.speed

            self.rect.x = int(self.location[0])
            self.rect.y = int(self.location[1])

        def check_for_turn(self, path_list):
            for path in path_list:
                if self.rect.colliderect(path.cesta):
                    if self.otocen_na_stranu != path.turn_to:
                        match path.turn_to:

                            # horizontální
                            case "doleva":
                                if self.otocen_na_stranu == "dolu":
                                    if path.cesta.y < self.rect.centery - 10 < path.cesta.bottom:
                                        self.otocen_na_stranu = "doleva"

                                elif self.otocen_na_stranu == "nahoru":
                                    if path.cesta.y < self.rect.centery + 10 < path.cesta.bottom:
                                        self.otocen_na_stranu = "doleva"

                            case "doprava":
                                if self.otocen_na_stranu == "dolu":
                                    if path.cesta.y < self.rect.centery - 10 < path.cesta.bottom:
                                        self.otocen_na_stranu = "doprava"

                                if self.otocen_na_stranu == "nahoru":
                                    if path.cesta.y < self.rect.centery + 10 < path.cesta.bottom:
                                        self.otocen_na_stranu = "doprava"

                            # vertikální
                            case "dolu":
                                if self.otocen_na_stranu == "doleva":
                                    if path.cesta.x < self.rect.centerx + 13 < path.cesta.right:
                                        self.otocen_na_stranu = "dolu"

                                if self.otocen_na_stranu == "doprava":
                                    if path.cesta.x < self.rect.centerx - 13 < path.cesta.right:
                                        self.otocen_na_stranu = "dolu"

                            case "nahoru":
                                if self.otocen_na_stranu == "doleva":
                                    if path.cesta.x < self.rect.centerx + 13 < path.cesta.right:
                                        self.otocen_na_stranu = "nahoru"

                                if self.otocen_na_stranu == "doprava":
                                    if path.cesta.x < self.rect.centerx - 13 < path.cesta.right:
                                        self.otocen_na_stranu = "nahoru"

        def check_for_skryte_turn(self, path_list):
            for path in path_list:
                if self.rect.colliderect(path.cesta):
                    if self.otocen_na_stranu != path.turn_to:
                        match path.turn_to:

                            # horizontální
                            case "doleva":
                                if self.otocen_na_stranu == "dolu":
                                    if path.cesta.y < self.rect.centery - 10 < path.cesta.bottom:
                                        self.otocen_na_stranu = "doleva"

                                elif self.otocen_na_stranu == "nahoru":
                                    if path.cesta.y < self.rect.centery + 10 < path.cesta.bottom:
                                        self.otocen_na_stranu = "doleva"

                            case "doprava":
                                if self.otocen_na_stranu == "dolu":
                                    if path.cesta.y < self.rect.centery - 10 < path.cesta.bottom:
                                        self.otocen_na_stranu = "doprava"

                                if self.otocen_na_stranu == "nahoru":
                                    if path.cesta.y < self.rect.centery + 10 < path.cesta.bottom:
                                        self.otocen_na_stranu = "doprava"

                            # vertikální
                            case "dolu":
                                if self.otocen_na_stranu == "doleva":
                                    if path.cesta.x < self.rect.centerx + 13 < path.cesta.right:
                                        self.otocen_na_stranu = "dolu"

                                if self.otocen_na_stranu == "doprava":
                                    if path.cesta.x < self.rect.centerx - 13 < path.cesta.right:
                                        self.otocen_na_stranu = "dolu"

                            case "nahoru":
                                if self.otocen_na_stranu == "doleva":
                                    if path.cesta.x < self.rect.centerx + 13 < path.cesta.right:
                                        self.otocen_na_stranu = "nahoru"

                                if self.otocen_na_stranu == "doprava":
                                    if path.cesta.x < self.rect.centerx - 13 < path.cesta.right:
                                        self.otocen_na_stranu = "nahoru"

        def check_turn_rozcesti(self, rozcesti_list):
            choices_hor = ("doleva", "doprava")
            choices_ver = ("nahoru", "dolu")

            for rozcesti in rozcesti_list:
                if self.rect.colliderect(rozcesti.rect):
                    match rozcesti.orientation:
                        case "horizontalne":
                            if self.otocen_na_stranu != choices_hor[0] and self.otocen_na_stranu != choices_hor[1]:
                                if rozcesti.rect.y <= self.rect.y <= rozcesti.rect.bottom:
                                    turn_to = random.choice(choices_hor)
                                    self.otocen_na_stranu = turn_to
                        case "vertikalne":
                            if self.otocen_na_stranu != choices_ver[0] and self.otocen_na_stranu != choices_ver[1]:
                                if rozcesti.rect.x <= self.rect.x and self.rect.right - 1 <= rozcesti.rect.right:
                                    turn_to = random.choice(choices_ver)
                                    self.otocen_na_stranu = turn_to
                        case _:
                            pass

        def outofbounds_check(self, log):
            if self.spawned:
                if self.rect.x < 0 or self.rect.x > 1200 or self.rect.y < 0 or self.rect.y > 800:
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
            self.fallen = False

            self.rect = pygame.Rect(x, y, 50, 50)

            # kapacita pro střelivo
            self.kapacita_streliva = 200

        def enemy_attack(self, enemy, log):
            self.hp -= enemy.hp
            if self.hp <= 0:
                self.fallen = True
                log.write_to_log("Základna padla!")

    class Spawner:
        def __init__(self, hra_instance, location, rotace_spawneru):

            self.location = location
            self.rotace_spawneru = rotace_spawneru  # strany jako do leva, do prava, dolu, nahoru

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
            location_offset = 0

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
                enemy = hra_instance.Nepritel(
                    "normal",
                    self.location,
                    self.rotace_spawneru,
                    location_offset,
                    hra_instance
                )

                list_of_enemies.append(enemy)
                location_offset += enemy.rect.width + 10

            # Generate special enemies
            for _ in range(max_special):
                special_enemy = hra_instance.Nepritel(
                    random.choice(self.special_moznosti),
                    self.location,
                    self.rotace_spawneru,
                    location_offset,
                    hra_instance
                )

                list_of_enemies.append(special_enemy)
                location_offset += special_enemy.rect.width + 10

            if hra_instance.wave_count == 10:
                list_of_enemies.append(hra_instance.Nepritel("boss", self.location, self.rotace_spawneru, 0,
                    hra_instance))

            if hra_instance.wave_count > 15:
                list_of_enemies.append(hra_instance.Nepritel("boss", self.location, self.rotace_spawneru, 0,
                    hra_instance))

            return list_of_enemies

        def placeholder_draw(self, window):
            pygame.draw.rect(window, (255, 255, 0), self.rect)

        def spawn_wave(self, hra_instance):
            hra_instance.enemies_list.append(self.generate_wave(hra_instance))
            return hra_instance

        def spawn_enemy(self, enemy_type, hra_instance):
            enemy = hra_instance.Nepritel(enemy_type)
            hra_instance.enemies_list.append(enemy)
            return hra_instance

    class Cesta:
        def __init__(self, x, y, sirka, vyska, otocit_se_na):
            self.cesta = pygame.Rect(x, y, sirka, vyska)
            self.turn_to = otocit_se_na

            match otocit_se_na:
                case "dolu":
                    self.rect_border = pygame.Rect(x, y, 60, 20)
                case "nahoru":
                    self.rect_border = pygame.Rect(x, y + vyska, 60, 20)
                case "doprava":
                    self.rect_border = pygame.Rect(x, y, 20, 60)
                case "doleva":
                    self.rect_border = pygame.Rect(x + sirka, y, 20, 60)

    class Rozcesti:
        def __init__(self, x, y, strana):
            self.orientation = strana

            match strana:
                case "horizontalne":
                    self.rect = pygame.Rect(x, y, 130, 30)
                case "vertikalne":
                    self.rect = pygame.Rect(x, y, 30, 130)

    class Vez:
        def __init__(self, typ, location, hra_instance):
            self.type = typ
            self.location = location

            self.damage = 0
            self.attack_cooldown = 0
            self.cooldown = 0
            self.radius = 0

            self.placement_cost = 0
            self.placement_radius = 65

            self.testing_rect = pygame.Rect(location[0], location[1], 45, 45)
            self.center = self.testing_rect.center
            self.blittable = None

            self.define_rest_of_stats(hra_instance)
            self.space_taken = pygame.Rect(self.center[0], self.center[1], self.placement_radius, self.placement_radius)
            self.space_taken.center = self.center

        def define_rest_of_stats(self, hra_instance):
            match self.type:
                case "normal_tower":  # basic tower
                    self.damage = 5
                    self.attack_cooldown = 75
                    self.radius = 150
                    self.blittable = hra_instance.vez_1_textura
                    self.placement_cost = 150

                case "speedy_tower":  # fast, short range tower
                    self.damage = 2
                    self.attack_cooldown = 25
                    self.radius = 70
                    self.blittable = hra_instance.vez_2_textura
                    self.placement_cost = 185

                case "sniper_tower":
                    self.damage = 15
                    self.attack_cooldown = 300
                    self.radius = 600
                    self.blittable = hra_instance.vez_3_textura
                    self.placement_cost = 350
                    self.placement_radius = 100

                case _:  # v případě chyby
                    self.damage = 5
                    self.attack_cooldown = 100
                    self.radius = 200
                    self.placement_cost = 100

            self.attack_cooldown /= hra_instance.speed_up_multiplier

        def shoot(self, seznam_nepratel, hra_instance):
            if self.cooldown < 1:
                closest_enemy = self.find_closest_enemy(seznam_nepratel)
                if closest_enemy is not None and closest_enemy.spawned:
                    if hra_instance.mnozstvi_streliva > 0:
                        closest_enemy.hp -= self.damage
                        self.cooldown = self.attack_cooldown

                        hra_instance.mnozstvi_streliva -= 1

        def shooting(self):  # vzhledově
            pass

        def find_closest_enemy(self, seznam_nepratel):
            if not seznam_nepratel:
                return None

            closest = seznam_nepratel[0]
            closest_dist = math.isqrt(abs(seznam_nepratel[0].rect.centerx - self.testing_rect.centerx) ** 2 + abs(
                seznam_nepratel[0].rect.centery - self.testing_rect.centery) ** 2)
            for enemy in seznam_nepratel:
                x = abs(enemy.rect.centerx - self.testing_rect.centerx)
                y = abs(enemy.rect.centery - self.testing_rect.centery)

                distance = math.isqrt(x ** 2 + y ** 2)
                if closest_dist > distance:
                    closest_dist = distance
                    closest = enemy
            if closest_dist < self.radius:
                return closest
            else:
                return None

    class Vesnice:
        def __init__(self, hra_instance,
                     location: list, value):  # usedliště civilistů, kteří produkují munici
            self.location = location
            self.ownership = True
            self.rect = pygame.Rect(location[0], location[1], 50, 50)
            self.color = (255, 255, 0)  # pro případy, kdy není žádná textura
            self.value = value  # Hodnota dolu, tato hodnota bude přičtena na konci každého kola k nábojům
            self.fallen = False
            self.hp = 40

            match hra_instance.obtiznost:
                case 1:
                    self.hp = 40
                case 2:
                    self.hp = 35
                case 3:
                    self.hp = 25

        def enemy_attack(self, enemy, log):
            self.hp -= enemy.hp
            if self.hp <= 0:
                self.fallen = True
                log.write_to_log("Vesnice padla!")

    class Tlacitko:
        def __init__(self, hra_instance, x, y, action):
            self.rect = pygame.Rect(x, y, 90, 90)
            self.action = action

            if self.action == "normal_tower":
                self.cost = 150
                self.range = 150
                self.damage = 5
            elif self.action == "speedy_tower":
                self.cost = 185
                self.damage = 2
                self.range = 70
            elif self.action == "sniper_tower":
                self.cost = 350
                self.range = 600
                self.damage = 15
            else:
                self.cost, self.range, self.damage = None, None, None

        def buy_ammo(self, hra_instance):
            if self.action == "buy_ammo":
                if hra_instance.penezenka >= 200 and hra_instance.mnozstvi_streliva < hra_instance.celkova_kapacita_streliva:
                    hra_instance.mnozstvi_streliva += 50
                    hra_instance.penezenka -= 200

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
