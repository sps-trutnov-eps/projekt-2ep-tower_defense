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
                    menu_mapy(menu_window)

        menu_draw(menu_window)
        
    pygame.quit()


def menu_draw(window):
    window.fill(bila)
    
    global button_rect
    font = pygame.font.SysFont(None, 50)
    text = font.render('HRÁT', True, bila)
    button_rect = pygame.Rect(350, 250, 100, 50)
    pygame.draw.rect(window, cerna, button_rect)
    text_rect = text.get_rect(center=button_rect.center)
    window.blit(text, text_rect)
    
    
    pygame.display.flip()
    
def menu_mapy(window):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mapa1.collidepoint(event.pos):
                    menu_obtiznosti(window)
                    mapa = mapa1
                elif mapa2.collidepoint(event.pos):
                    menu_obtiznosti(window)
                    mapa = mapa2
                elif mapa3.collidepoint(event.pos):
                    menu_obtiznosti(window)
                    mapa = mapa3
           
           
        window.fill(bila)
        
        font = pygame.font.SysFont(None, 140)
        text = font.render('MAPY', True, cerna)  
        text_rect = text.get_rect(center=(400, 100))  
        window.blit(text, text_rect)
        
        mapa1 = pygame.Rect(108, 200, 180, 180)
        pygame.draw.rect(window, cerna, mapa1)
        mapa2 = pygame.Rect(308, 200, 180, 180)
        pygame.draw.rect(window, cerna, mapa2)
        mapa3 = pygame.Rect(508, 200, 180, 180)
        pygame.draw.rect(window, cerna, mapa3)
        
        
        pygame.display.flip()
        
        
        
def menu_obtiznosti(window):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if obtiznost1.collidepoint(event.pos):
                    obtiznost = obtiznost1
                elif obtiznost2.collidepoint(event.pos):
                    obtiznost = obtiznost2
                elif obtiznost3.collidepoint(event.pos):
                    obtiznost = obtiznost3
        
        window.fill(bila)
        
        font = pygame.font.SysFont(None, 140)
        text = font.render('OBTÍŽNOSTI', True, cerna)
        text_rect = text.get_rect(center=(400, 100))
        window.blit(text, text_rect)
        
        obtiznost1 = pygame.Rect(108, 200, 180, 180)
        pygame.draw.rect(window, cerna, obtiznost1)
        obtiznost2 = pygame.Rect(308, 200, 180, 180)
        pygame.draw.rect(window, cerna, obtiznost2)
        obtiznost3 = pygame.Rect(508, 200, 180, 180)
        pygame.draw.rect(window, cerna, obtiznost3)
        
        pygame.display.flip()
        
        

    
    
if __name__ == "__main__":
    menu_main()