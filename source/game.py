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
        "vesnice": []
    }

    match hra.mapa:
        case 1:
            from mapy.mapa_1 import load_entities
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

            # TODO: zakladny, spawnery, veze, doly, vesnice

        case _:
            pass

    return seznam_entit


def count_entities(type: str, seznam_entit):
    count = 0
    for entity in seznam_entit[type]:
        count += 1

    return count


def try_spawning_enemies(hra):
    for enemy_number in hra.enemies_to_spawn_count:
        if enemy_number > 0:
            random_spawner = random.randint(0, len(hra.seznam_entit["spawnery"]) - 1)
            hra.seznam_entit["spawnery"][random_spawner].spawn_enemy(hra.enemies_list[0])
            hra.enemies_list[0].remove()


def move_enemies(list_of_enemies):
    for enemy in list_of_enemies:
        enemy.move()


def game_updates(hra, log):
    if hra.aktualni_vlna_dokoncena:
        log.write_to_log(f"Zjištěno že není aktivní žádná vlna, spouštím vlnu: {hra.wave_count+1}")

        for spawner in hra.seznam_entit["spawnery"]:
            spawner.make_wave(hra)
        hra.update_wave_count()

        log.write_to_log(f"Vygenerováno: {count_entities('nepratele', hra.seznam_entit)}")
        log.write_to_log(f"Vlna {hra.wave_count} úspěšně vygenerována")

    # po kontrole zda nějací existují, posune nepřáteli
    try:
        if hra.seznam_entit["nepratele"][0]:
            move_enemies(hra.seznam_entit["nepratele"])

            try_spawning_enemies(hra, hra.seznam_entit)
    except:
        pass


def game_window_draw(window, hra):
    window.fill(BLACK)
    for vesnice in hra.seznam_entit["vesnice"]:
        pygame.draw.rect(window, vesnice.color, vesnice.rect)

    for dul in hra.seznam_entit["doly"]:
        pygame.draw.rect(window, dul.color, dul.rect)

    for vez in hra.seznam_entit["veze"]:
        if vez.type == "test_tower":
            pygame.draw.rect(window, BLUE, vez.testing_rect)

    for spawner in hra.seznam_entit["spawnery"]:
        pygame.draw.rect(window, RED, spawner.rect)

    pygame.display.flip()


def game_main(mapa, obtiznost):
    from classes import Hra

    clock = pygame.time.Clock()

    game_window = pygame.display.set_mode((1200, 800))
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

        clock.tick(FPS)

    log.write_to_log("Hra ukončena")


if __name__ == "__main__":
    game_main(1, 1)


# TODO: importování map, nějak, nebo, pro každou mapu zvlášť celá hra??