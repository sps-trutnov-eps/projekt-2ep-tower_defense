import pygame
import random

pygame.font.init()

wave_text = pygame.font.SysFont("Arial", 25)
menu_text = pygame.font.SysFont("Arial", 25)

# barvičky
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (30, 30, 30)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED_TRANSLUCENT = (255, 0, 0, 50)      # původně 255,0,0,128

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

    tower1button = hra.Tlacitko(hra, 0, 180, "normal_tower")
    tower2button = hra.Tlacitko(hra, 0, 275, "speedy_tower")
    tower3button = hra.Tlacitko(hra, 0, 370, "sniper_tower")
    hra.list_of_buttons.append(tower1button)
    hra.list_of_buttons.append(tower2button)
    hra.list_of_buttons.append(tower3button)

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


def get_circle_radius(hra, current_action):
    match current_action:
        case "normal_tower":
            return 65
        case "speedy_tower":
            return 50
        case "sniper_tower":
            return 95
        case _:
            return 75


def test_for_collisions(nova_vez, hra):
    for vez in hra.seznam_entit["veze"]:
        if nova_vez.testing_rect.colliderect(vez.space_taken):
            return True
    for cesta in hra.seznam_entit["cesty"]:
        if nova_vez.testing_rect.colliderect(cesta.rect_border):
            return True
    for spawner in hra.seznam_entit["spawnery"]:
        if nova_vez.testing_rect.colliderect(spawner.rect):
            return True
    for zakladna in hra.seznam_entit["zakladny"]:
        if nova_vez.testing_rect.colliderect(zakladna.rect):
            return True


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
    hra.check_for_loss(log)

    if not hra.seznam_entit["nepratele"] and not hra.aktualni_vlna_dokoncena:
        hra.aktualni_vlna_dokoncena = True

        value = 0
        for vesnice in hra.seznam_entit["vesnice"]:
            if not vesnice.fallen:
                value += vesnice.value
        hra.mnozstvi_streliva += value
        if hra.mnozstvi_streliva > hra.celkova_kapacita_streliva:
            hra.mnozstvi_streliva = hra.celkova_kapacita_streliva

    if hra.aktualni_vlna_dokoncena:
        log.write_to_log(f"Zjištěno že není aktivní žádná vlna, spouštím vlnu: {hra.wave_count + 1}")

        for spawner in hra.seznam_entit["spawnery"]:
            spawner.make_wave(hra)
        hra.update_wave_count()
        if hra.wave_count != 1:
            hra.mnozstvi_streliva += 15
            if hra.wave_count < 10:
                hra.penezenka += 100
            elif hra.wave_count < 25:
                hra.penezenka += 500
            else:
                hra.penezenka += 1000

        log.write_to_log(f"Vygenerováno: {count_entities('nepratele', hra.seznam_entit)}")
        log.write_to_log(f"Vlna {hra.wave_count} úspěšně vygenerována")

    if not hra.seznam_entit["nepratele"][0]:
        try_spawning_enemies(hra, big_enough_gap=0)

    move_enemies(hra.seznam_entit["nepratele"])

    for enemy in hra.seznam_entit["nepratele"]:
        kill_enemy = enemy.outofbounds_check(log)
        if kill_enemy or enemy.hp <= 0:
            hra.penezenka += enemy.odmena
            hra.seznam_entit["nepratele"].remove(enemy)
            hra.enemies_killed += 1
        if not enemy.spawned:
            enemy.check_to_spawn(hra.seznam_entit["spawnery"])

        enemy.check_for_turn(hra.seznam_entit["cesty"])

        enemy.check_for_turn(hra.seznam_entit["skryte_cesty"])

        enemy.check_turn_rozcesti(hra.seznam_entit["rozcesti"])

        for zakladna in hra.seznam_entit["zakladny"]:
            if enemy.rect.colliderect(zakladna.rect):
                if not zakladna.fallen:
                    enemy.utok_na_zakladnu(hra, hra.seznam_entit["zakladny"].index(zakladna), log)

                    if zakladna.fallen:
                        hra.get_max_resource_count()

        for vesnice in hra.seznam_entit["vesnice"]:
            if enemy.rect.colliderect(vesnice.rect):
                if not vesnice.fallen:
                    enemy.utok_na_vesnici(hra, hra.seznam_entit["vesnice"].index(vesnice), log)

    for vez in hra.seznam_entit["veze"]:
        vez.shoot(hra.seznam_entit["nepratele"], hra)
        vez.cooldown -= 1


def draw_menu(window, hra, texts):
    # rámeček
    # pygame.draw.rect(window, WHITE, (90, 0, 2, 1200))
    window.blit(hra.side_menu_textura, (0, 0))

    # stats (vlna, střelivo, peníze)
    window.blit(texts[3], (45 - texts[3].get_width() / 2, 30))
    window.blit(texts[4], (45 - texts[4].get_width() / 2, 58 + 26))
    window.blit(texts[5], (45 - texts[5].get_width() / 2, 138))

    # obrázky věží
    # window.blit(pygame.transform.scale(hra.vez_1_textura, 45), (0, 150))   <--- není obrázek
    pygame.draw.rect(window, BLUE, (0, 180, 90, 90))

    window.blit(pygame.transform.scale(hra.vez_2_textura, (90, 90)), (0, 275))
    # window.blit(pygame.transform.scale(hra.vez_3_textura, (90, 90)), (0, 250))
    pygame.draw.rect(window, GREEN, (0, 370, 90, 90))

    # Velký text, není potřeba
    # window.blit(texts[0], (1200 - texts[0].get_width(), 800 - texts[0].get_height()))
    # window.blit(texts[1], (100, 800 - texts[1].get_height()))
    # window.blit(texts[2], (100, 800 - texts[1].get_height()*2))


def game_window_draw(window, hra, texts, circle_surface, circle_radius):
    window.fill(BLACK)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    circle_surface.fill((0, 0, 0, 0))
    pygame.draw.circle(circle_surface, RED_TRANSLUCENT, (400, 400), circle_radius)

    for cesta in hra.seznam_entit["cesty"]:  # in dev only
        pygame.draw.rect(window, WHITE, cesta.cesta)

    for cesta in hra.seznam_entit["skryte_cesty"]:  # in dev only
        pygame.draw.rect(window, GRAY, cesta.cesta)

    for rozcesti in hra.seznam_entit["rozcesti"]:
        pygame.draw.rect(window, WHITE, rozcesti.rect)

    for vez in hra.seznam_entit["veze"]:  # in dev only
        if vez.type == "normal_tower":
            pass
            # window.blit(vez.blittable, vez.location)
        elif vez.type == "speedy_tower":
            window.blit(vez.blittable, vez.location)
        elif vez.type == "sniper_tower":
            pass
            # window.blit(vez.blittable, vez.location)
        elif vez.type == "test_tower":
            pygame.draw.rect(window, BLUE, vez.testing_rect)
        else:
            pygame.draw.rect(window, BLUE, vez.testing_rect)

    for enemy in hra.seznam_entit["nepratele"]:  # in dev only
        if enemy.spawned:
            if enemy.rect_color != RED:
                pygame.draw.rect(window, enemy.rect_color, enemy.rect)  # in dev only

            if enemy.typ_nepritele == "normal":
                stupne = preklad_na_stupne(enemy)
                window.blit(
                    pygame.transform.rotate(hra.nepritel_normal_textura, stupne),
                    (enemy.rect.x, enemy.rect.y)
                )

    for vesnice in hra.seznam_entit["vesnice"]:  # in dev only
        pygame.draw.rect(window, vesnice.color, vesnice.rect)

    for spawner in hra.seznam_entit["spawnery"]:  # in dev only
        pygame.draw.rect(window, RED, spawner.rect)

    for zakladna in hra.seznam_entit["zakladny"]:
        pygame.draw.rect(window, (153, 24, 240), zakladna.rect)

    window.blit(circle_surface, (mouse_x - 400, mouse_y - 400))

    draw_menu(window, hra, texts)

    pygame.display.flip()


def game_main(mapa, obtiznost):
    from classes import Hra

    circle_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
    circle_radius = 0

    time = False
    clock = pygame.time.Clock()

    game_window = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption(f"Tower Defense - {mapa_translation(mapa)}")
    game_running = True

    current_action = None

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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action_changed = False
                for button in hra.list_of_buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        current_action = button.action
                        action_changed = True
                if not action_changed and current_action:
                    x, y = pygame.mouse.get_pos()
                    nova_vez = hra.Vez(current_action, (x - 22, y - 22), hra)
                    if not test_for_collisions(nova_vez, hra) and hra.penezenka > nova_vez.placement_cost:
                        hra.seznam_entit["veze"].append(nova_vez)
                        hra.penezenka -= nova_vez.placement_cost

        if current_action:
            circle_radius = get_circle_radius(hra, current_action)

        if hra.game_over:
            game_running = False

        text_vlna = wave_text.render(f'Vlna: {hra.wave_count}', False, WHITE)
        text_strelivo = wave_text.render(f'Střelivo: {hra.mnozstvi_streliva}/{hra.celkova_kapacita_streliva}',
                                         False, WHITE)
        text_penize = wave_text.render(f'Peníze: {hra.penezenka}', False, WHITE)

        text_menu_wave_count = menu_text.render(f"{hra.wave_count}", False, BLACK)
        text_menu_strelivo = menu_text.render(f"{hra.mnozstvi_streliva}/{hra.celkova_kapacita_streliva}", False, BLACK)
        text_menu_penize = menu_text.render(f"{hra.penezenka}", False, BLACK)

        game_updates(hra, log)

        game_window_draw(game_window, hra, [text_vlna, text_strelivo, text_penize, text_menu_wave_count,
                                            text_menu_penize, text_menu_strelivo], circle_surface, circle_radius)

        # dá čas hráči pro rozkoukání
        if not time:
            # pygame.time.wait(2500)
            time = True

        clock.tick(FPS)

    #                   Po skončení hry
    ####################################################
    big_font = pygame.font.SysFont(None, 150)
    game_over_text = big_font.render("Konec Hry", False, BLACK)

    stats_font = pygame.font.SysFont(None, 60)
    enemies_killed = stats_font.render(f'Zabitých neprátel: {hra.enemies_killed}', False, BLACK)
    money_left_over = stats_font.render(f'Vaše peníze: {hra.penezenka}', False, BLACK)

    exit_menu_running = True
    while exit_menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_menu_running = False
                log.write_to_log("Tlačítko QUIT zmáčknuto")
        game_window.fill(RED)

        game_window.blit(game_over_text, (game_window.get_width() / 2 - game_over_text.get_width() / 2,
                                          game_window.get_height() / 2 - 300))
        game_window.blit(enemies_killed,
                         (game_window.get_width() / 2 - enemies_killed.get_width() / 2, game_window.get_height() / 2))
        game_window.blit(money_left_over, (
        game_window.get_width() / 2 - money_left_over.get_width() / 2, game_window.get_height() / 2 + 60))
        pygame.display.flip()
    log.write_to_log("Hra ukončena")


if __name__ == "__main__":
    game_main(0, 1)
