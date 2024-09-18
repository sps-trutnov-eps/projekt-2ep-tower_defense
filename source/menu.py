import pygame
bila = (255, 255,  255)

def menu_main():
    pygame.init()
    menu_window = pygame.display.set_mode((800, 600))
    menu_open = True

    while menu_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_open = False

        menu_draw(menu_window)
        
    pygame.quit()


def menu_draw(window):
    window.fill(bila)
    pygame.display.flip()
    
    
    
if __name__ == "__main__":
    menu_main()