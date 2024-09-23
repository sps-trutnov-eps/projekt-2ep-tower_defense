def menu_main():
    import pygame
    menu_window = pygame.display.set_mode((800, 600))
    menu_open = True

    while menu_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_open = False

        menu_draw(menu_window)


def menu_draw(window):
    window.display.flip()