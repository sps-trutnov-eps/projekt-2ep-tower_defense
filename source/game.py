import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def move_enemies(list_of_enemies):
    for enemy in list_of_enemies:
        enemy.move()


def game_window_draw(window):
    window.fill(BLACK)

    pygame.display.flip()


def game_main(mapa, obtiznost):
    from classes import Hra

    # Během vývoje:
    mapa = 1
    obtiznost = 1

    game_window = pygame.display.set_mode((1200, 800))
    game_running = True

    hra = Hra(mapa, obtiznost)
    log = hra.Logging()
    log.write_to_log("Hra běží")

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                log.write_to_log("Tlačítko QUIT zmáčknuto")

        game_window_draw(game_window)

    log.write_to_log("Hra ukončena")


if __name__ == "__main__":
    game_main(1, 1)


# TODO: importování map, nějak, nebo, pro každou mapu zvlášť celá hra??