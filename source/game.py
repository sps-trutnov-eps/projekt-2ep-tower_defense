import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def game_window_draw(window):
    window.fill(BLACK)

    pygame.display.flip()


def game_main(mapa, obtiznost):
    game_window = pygame.display.set_mode((1200, 800))
    game_running = True

    from classes import Hra
    # TODO: importování map, nějak, nebo, pro každou mapu zvlášť celá hra??

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        game_window_draw(game_window)


if __name__ == "__main__":
    game_main(1, 1)