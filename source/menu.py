import pygame
bila = (255, 255,  255)
cerna = (0, 0, 0)


def menu_main():
    pygame.init()
    menu_window = pygame.display.set_mode((800, 600))
    menu_open = True

    while menu_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_open = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    menu_screen(menu_window)

        menu_draw(menu_window)
        
    pygame.quit()


def menu_draw(window):
    window.fill(bila)
    
    global button_rect
    font = pygame.font.SysFont(None, 55)
    text = font.render('HRÁT', True, bila)
    button_rect = pygame.Rect(350, 250, 100, 50)
    pygame.draw.rect(window, cerna, button_rect)
    text_rect = text.get_rect(center=button_rect.center)
    window.blit(text, text_rect)
    
    
    pygame.display.flip()
    
def menu_screen(window):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        
        window.fill(bila)
        
        font = pygame.font.SysFont(None, 75)
        text = font.render('MAPY', True, cerna)  
        text_rect = text.get_rect(center=(400, 100))  
        window.blit(text, text_rect) 
        
        pygame.display.flip()
    
    
if __name__ == "__main__":
    menu_main()