import pygame
import random


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


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


def try_spawning_enemies(hra, seznam_entit):
    for enemy_number in hra.enemies_to_spawn_count:
        if enemy_number > 0:
            random_spawner = random.randint(0, len(seznam_entit["spawnery"]) - 1)
            seznam_entit["spawnery"][random_spawner].spawn_enemy(hra.enemies_list[0])
            hra.enemies_list[0].remove()


def move_enemies(list_of_enemies):
    for enemy in list_of_enemies:
        enemy.move()


def game_updates(hra, seznam_entit):
    # po kontrole zda nějací existují, posune nepřáteli
    if seznam_entit["nepratele"][0]:
        move_enemies(seznam_entit["nepratele"])

    try_spawning_enemies(hra, seznam_entit)


def game_window_draw(window):
    window.fill(BLACK)

    pygame.display.flip()


def game_main(mapa, obtiznost):
    from classes import Hra

    game_window = pygame.display.set_mode((1200, 800))
    game_running = True

    hra = Hra(mapa, obtiznost)
    log = hra.Logging()
    log.write_to_log("Hra běží")

    # [ základny | spawnery | nepratele | veze | doly | vesnice ]
    log.write_to_log("Zkouším načíst entity")
    seznam_entit = load_seznam_entit(hra, log)
    log.write_to_log("Entity načteny")

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                log.write_to_log("Tlačítko QUIT zmáčknuto")

        game_updates(hra, seznam_entit)
        game_window_draw(game_window)

    log.write_to_log("Hra ukončena")


if __name__ == "__main__":
    game_main(1, 1)


# TODO: importování map, nějak, nebo, pro každou mapu zvlášť celá hra??