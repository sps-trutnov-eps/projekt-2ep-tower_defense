import pygame
pygame.font.init()
import random

wave_text = pygame.font.SysFont(None, 50)

# barvičky
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (30, 30, 30)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FPS = 60


def load_seznam_entit(hra, log):
    # [ základny | spawnery | nepratele | veze | doly | vesnice ]
    seznam_entit = {
        "zakladny": [],
        "spawnery": [],
        "nepratele": [],
        "veze": [],
        "doly": [],
        "vesnice": [],
        "cesty": [],
        "skryte_cesty": []
    }

    match hra.mapa:
        case 0:
            from mapy.mapa_0 import load_entities
            seznam_entit["zakladny"] = load_entities("zakladny", hra)
            log.write_to_log("Načteny základny")

            seznam_entit["spawnery"] = load_entities("spawnery", hra)
            log.write_to_log("Načteny spawnery")

            seznam_entit["veze"] = load_entities("veze", hra)
            log.write_to_log("Načteny veze")

            seznam_entit["doly"] = load_entities("doly", hra)
            log.write_to_log("Načteny doly")

            seznam_entit["vesnice"] = load_entities("vesnice", hra)
            log.write_to_log("Načteny vesnice")

            seznam_entit["cesty"] = load_entities("cesty", hra)
            log.write_to_log("Načteny cesty")

            seznam_entit["skryte_cesty"] = load_entities("skryte_cesty", hra)

            seznam_entit["rozcesti"] = load_entities("rozcesti", hra)
            log.write_to_log("Načteny rozcestí")

            # TODO: veze, doly, vesnice

        case _:
            pass

    return seznam_entit


def count_entities(entity_type: str, seznam_entit):
    count = 0
    for _ in seznam_entit[entity_type]:
        count += 1

    return count


def preklad_na_stupne(enemy):
    strana = enemy.otocen_na_stranu
    stupne = 0
    match strana:
        case "dolu":
            stupne = 0
        case "doprava":
            stupne = 90
        case "nahoru":
            stupne = 180
        case "doleva":
            stupne = 270

    return stupne


def mapa_translation(mapa):
    match mapa:
        case 1:
            translation = "Mapa 1"
        case _:
            translation = "How did we get here?"

    return translation


def try_spawning_enemies(hra, big_enough_gap):
    big_enough_gap += 1
    for enemy_number in hra.enemies_to_spawn_count:
        if big_enough_gap > 50:
            if enemy_number > 0:
                random_spawner = random.randint(0, len(hra.seznam_entit["spawnery"]) - 1)
                hra.seznam_entit["spawnery"][random_spawner].spawn_enemy(hra.enemies_list[0])
                hra.enemies_list[0].remove()
                big_enough_gap = 0

    return big_enough_gap


def move_enemies(list_of_enemies):
    for enemy in list_of_enemies:
        enemy.move()


def game_updates(hra, log):
    hra.check_for_loss()

    if not hra.seznam_entit["nepratele"] and not hra.aktualni_vlna_dokoncena:
        hra.aktualni_vlna_dokoncena = True

    if hra.aktualni_vlna_dokoncena:
        log.write_to_log(f"Zjištěno že není aktivní žádná vlna, spouštím vlnu: {hra.wave_count+1}")

        for spawner in hra.seznam_entit["spawnery"]:
            spawner.make_wave(hra)
        hra.update_wave_count()

        log.write_to_log(f"Vygenerováno: {count_entities('nepratele', hra.seznam_entit)}")
        log.write_to_log(f"Vlna {hra.wave_count} úspěšně vygenerována")

    if not hra.seznam_entit["nepratele"][0]:
        try_spawning_enemies(hra, big_enough_gap=0)

    move_enemies(hra.seznam_entit["nepratele"])

    for enemy in hra.seznam_entit["nepratele"]:
        kill_enemy = enemy.outofbounds_check(log)
        if kill_enemy or enemy.hp <= 0:
            hra.seznam_entit["nepratele"].remove(enemy)
            hra.enemies_killed += 1
        if not enemy.spawned:
            enemy.check_to_spawn(hra.seznam_entit["spawnery"])

        enemy.check_for_turn(hra.seznam_entit["cesty"])

        enemy.check_for_turn(hra.seznam_entit["skryte_cesty"])

        enemy.check_turn_rozcesti(hra.seznam_entit["rozcesti"])

        for zakladna in hra.seznam_entit["zakladny"]:
            if enemy.rect.colliderect(zakladna.rect):
                """
                if zakladna.fallen and not enemy.reverse_direction:
                    enemy.reverse_direction = True

                    match enemy.otocen_na_stranu:
                        case "nahoru":
                            enemy.otocen_na_stranu = "dolu"
                        case "dolu":
                            enemy.otocen_na_stranu = "nahoru"
                        case "doleva":
                            enemy.otocen_na_stranu = "doprava"
                        case "doprava":
                            enemy.otocen_na_stranu = "doleva"
                """
                if not zakladna.fallen:
                    enemy.utok_na_zakladnu(hra, hra.seznam_entit["zakladny"].index(zakladna), log)

                    if zakladna.fallen:
                        hra.get_max_resource_count()

    for vez in hra.seznam_entit["veze"]:
        vez.shoot(hra.seznam_entit["nepratele"], hra)
        vez.cooldown -= 1


def game_window_draw(window, hra, texts):
    window.fill(BLACK)

    for cesta in hra.seznam_entit["cesty"]:                                 # in dev only
        pygame.draw.rect(window, WHITE, cesta.cesta)

    for cesta in hra.seznam_entit["skryte_cesty"]:  # in dev only
        pygame.draw.rect(window, GRAY, cesta.cesta)

    for rozcesti in hra.seznam_entit["rozcesti"]:
        pygame.draw.rect(window, WHITE, rozcesti.rect)

    for vesnice in hra.seznam_entit["vesnice"]:                                 # in dev only
        pygame.draw.rect(window, vesnice.color, vesnice.rect)

    for dul in hra.seznam_entit["doly"]:                                 # in dev only
        pygame.draw.rect(window, dul.color, dul.rect)

    for vez in hra.seznam_entit["veze"]:                                 # in dev only
        if vez.type == "normal_tower":
            pass
            #window.blit(vez.blittable, vez.location)
        elif vez.type == "speedy_tower":
            window.blit(vez.blittable, vez.location)
        elif vez.type == "sniper_tower":
            pass
            #window.blit(vez.blittable, vez.location)
        elif vez.type == "test_tower":
            pygame.draw.rect(window, BLUE, vez.testing_rect)
        else:
            pygame.draw.rect(window, BLUE, vez.testing_rect)

    for enemy in hra.seznam_entit["nepratele"]:                                 # in dev only
        if enemy.spawned:
            pygame.draw.rect(window, enemy.rect_color, enemy.rect)  # in dev only
            if enemy.typ_nepritele == "normal":
                stupne = preklad_na_stupne(enemy)
                window.blit(
                    pygame.transform.rotate(hra.nepritel_normal_textura, stupne),
                    (enemy.rect.x, enemy.rect.y)
                )

    for spawner in hra.seznam_entit["spawnery"]:                                 # in dev only
        pygame.draw.rect(window, RED, spawner.rect)

    for zakladna in hra.seznam_entit["zakladny"]:
        pygame.draw.rect(window, (153, 24, 240), zakladna.rect)

    window.blit(texts[0], (1200 - texts[0].get_width(), 800 - texts[0].get_height()))
    window.blit(texts[1], (5, 800 - texts[1].get_height()))

    pygame.display.flip()


def game_main(mapa, obtiznost):
    from classes import Hra

    time = False
    clock = pygame.time.Clock()

    game_window = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption(f"Tower Defense - {mapa_translation(mapa)}")
    game_running = True

    hra = Hra(mapa, obtiznost)
    log = hra.Logging()
    log.write_to_log("Hra spuštěna")

    # [ základny | spawnery | nepratele | veze | doly | vesnice ]
    log.write_to_log("Zkouším načíst entity")
    hra.seznam_entit = load_seznam_entit(hra, log)
    hra.get_max_resource_count()

    log.write_to_log("Entity načteny")

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                log.write_to_log("Tlačítko QUIT zmáčknuto")

        if hra.game_over:
            game_running = False

        text_vlna = wave_text.render(f'Vlna: {hra.wave_count}', False, WHITE)
        text_strelivo = wave_text.render(f'Střelivo: {hra.mnozstvi_streliva}/{hra.celkova_kapacita_streliva}',
                                         False, WHITE)

        game_updates(hra, log)

        game_window_draw(game_window, hra, texts=[text_vlna, text_strelivo])

        # dá čas hráči pro rozkoukání
        if not time:
            #pygame.time.wait(2500)
            time = True

        clock.tick(FPS)

    #                   Po skončení hry
    ####################################################
    big_font = pygame.font.SysFont(None, 150)
    game_over_text = big_font.render("Konec Hry", False, BLACK)

    stats_font = pygame.font.SysFont(None, 60)
    enemies_killed = stats_font.render(f'Enemies killed: {hra.enemies_killed}', False, BLACK)

    exit_menu_running = True
    while exit_menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_menu_running = False
                log.write_to_log("Tlačítko QUIT zmáčknuto")
        game_window.fill(RED)

        game_window.blit(game_over_text, (game_window.get_width()/2 - game_over_text.get_width() / 2,
                                game_window.get_height()/2 - 300))
        game_window.blit(enemies_killed, (game_window.get_width()/2 - enemies_killed.get_width() / 2, game_window.get_height()/2))
        pygame.display.flip()
    log.write_to_log("Hra ukončena")


if __name__ == "__main__":
    game_main(0, 1)
