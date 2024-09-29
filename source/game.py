import pygame
import random


# barvičky
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
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
        "cesty": []
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

            seznam_entit["rozcesti"] = load_entities("rozcesti", hra)
            log.write_to_log("Načteny rozcestí")

            # TODO: zakladny, veze, doly, vesnice
            #       spawnery potřebují opravit mezery u spawnu a obrázky nepřátel
            #       generování vln nefunguje jak má - spustí se pouze první

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
                #if previous_enemy_is_far_enough:
                random_spawner = random.randint(0, len(hra.seznam_entit["spawnery"]) - 1)
                hra.seznam_entit["spawnery"][random_spawner].spawn_enemy(hra.enemies_list[0])
                hra.enemies_list[0].remove()
                big_enough_gap = 0

    return big_enough_gap


def move_enemies(list_of_enemies):
    for enemy in list_of_enemies:
        enemy.move()


def game_updates(hra, log):
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
        if kill_enemy:
            hra.seznam_entit["nepratele"].remove(enemy)
        if not enemy.spawned:
            enemy.check_to_spawn(hra.seznam_entit["spawnery"])

        enemy.check_for_turn(hra.seznam_entit["cesty"], log)
        enemy.check_turn_rozcesti(hra.seznam_entit["rozcesti"])

        for zakladna in hra.seznam_entit["zakladny"]:
            if enemy.rect.colliderect(zakladna.rect):
                enemy.utok_na_zakladnu(hra, hra.seznam_entit["zakladny"].index(zakladna))


def game_window_draw(window, hra):
    window.fill(BLACK)

    for cesta in hra.seznam_entit["cesty"]:                                 # in dev only
        pygame.draw.rect(window, WHITE, cesta.cesta)

    for rozcesti in hra.seznam_entit["rozcesti"]:
        pygame.draw.rect(window, WHITE, rozcesti.rect)

    for vesnice in hra.seznam_entit["vesnice"]:                                 # in dev only
        pygame.draw.rect(window, vesnice.color, vesnice.rect)

    for dul in hra.seznam_entit["doly"]:                                 # in dev only
        pygame.draw.rect(window, dul.color, dul.rect)

    for vez in hra.seznam_entit["veze"]:                                 # in dev only
        if vez.type == "test_tower":
            pygame.draw.rect(window, BLUE, vez.testing_rect)
        else:
            pass

    for enemy in hra.seznam_entit["nepratele"]:                                 # in dev only
        if enemy.spawned:
            #pygame.draw.rect(window, RED, enemy.rect)  # in dev only
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

    log.write_to_log("Entity načteny")

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                log.write_to_log("Tlačítko QUIT zmáčknuto")

        game_updates(hra, log)

        game_window_draw(game_window, hra)

        # dá čas hráči pro rozkoukání
        if not time:
            #pygame.time.wait(2500)
            time = True

        clock.tick(FPS)

    log.write_to_log("Hra ukončena")


if __name__ == "__main__":
    game_main(0, 1)
