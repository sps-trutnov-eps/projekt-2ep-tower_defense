import pygame

zluta = (255, 255, 0)
zelena = (0, 255, 0)
cervena = (255, 0, 0)
bila = (255, 255,  255)
cerna = (0, 0, 0)
tlacitko_hrat = pygame.image.load("menu_obrazky/tlacitko_hrat.png")

menu_open = True
running = True
obtiznosti_running = True


def menu_main():
    pygame.init()
    menu_window = pygame.display.set_mode((800, 600))

    global menu_open

    while menu_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                obtiznosti_running = False
                running = False
                menu_open = False
                return (False, False, False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    map_difficulty = menu_mapy(menu_window)
                    menu_open = False

        menu_draw(menu_window)
        
    pygame.quit()

    return map_difficulty[0], map_difficulty[1], True


def menu_draw(window):
    global button_rect

    window.fill(bila)

    button_rect = pygame.Rect(250, 200, 300, 150)
    window.blit(pygame.transform.scale(tlacitko_hrat, (button_rect.width, button_rect.height)), button_rect.topleft) 

    pygame.display.flip()


def menu_mapy(window):
    global running, obtiznosti_running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                obtiznosti_running = False
                running = False
                menu_open = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mapa1.collidepoint(event.pos):
                    mapa = 1
                    running = False
                elif mapa2.collidepoint(event.pos):
                    mapa = 2
                    running = False
                elif mapa3.collidepoint(event.pos):
                    mapa = 3
                    running = False

        window.fill(bila)
        
        font = pygame.font.SysFont(None, 150)
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

    if obtiznosti_running:
        obtiznost = menu_obtiznosti(window)
    else:
        obtiznost = False

    return (mapa, obtiznost)

        
def menu_obtiznosti(window):
    global obtiznosti_running
    while obtiznosti_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                obtiznosti_running = False
                running = False
                menu_open = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if obtiznost1.collidepoint(event.pos):
                    obtiznost = 1
                    obtiznosti_running = False
                elif obtiznost2.collidepoint(event.pos):
                    obtiznost = 2
                    obtiznosti_running = False
                elif obtiznost3.collidepoint(event.pos):
                    obtiznost = 3
                    obtiznosti_running = False
        
        window.fill(bila)
        
        font = pygame.font.SysFont(None, 150)
        text = font.render('OBTÍŽNOSTI', True, cerna)
        text_rect = text.get_rect(center=(400, 100))
        window.blit(text, text_rect)
        
        obtiznost1 = pygame.Rect(108, 200, 180, 180)
        pygame.draw.rect(window, cerna, obtiznost1)
        obtiznost2 = pygame.Rect(308, 200, 180, 180)
        pygame.draw.rect(window, cerna, obtiznost2)
        obtiznost3 = pygame.Rect(508, 200, 180, 180)
        pygame.draw.rect(window, cerna, obtiznost3)
        
        font_text = pygame.font.SysFont(None, 50)
        text_lehka = font_text.render('LEHKÁ', True, zelena)
        text_stredni = font_text.render('STŘEDNÍ', True, zluta)
        text_tezka = font_text.render('TĚŽKÁ', True, cervena)
        
        window.blit(text_lehka, (obtiznost1.x + 30, obtiznost1.y + 200))
        window.blit(text_stredni, (obtiznost2.x + 15, obtiznost2.y + 200))
        window.blit(text_tezka, (obtiznost3.x + 30, obtiznost3.y + 200))
        
        pygame.display.flip()

    return obtiznost

    
if __name__ == "__main__":
    menu_main()