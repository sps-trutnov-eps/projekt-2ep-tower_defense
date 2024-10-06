def load_entities(entity_type, initiated_game):

    match entity_type:
        case "zakladny":
            # obtiznost, x ,y
            to_return = [
                initiated_game.Zakladna(initiated_game.obtiznost, 1000, 80),
                initiated_game.Zakladna(initiated_game.obtiznost, 1025, 690)
                         ]
        case "spawnery":
            # hra_instance, x ,y
            to_return = [
                initiated_game.Spawner(initiated_game, (100, 50), "dolu")
            ]
        case "nepratele":
            # typ_nepritele     vrací se prázdné, spawnery je tvoří
            to_return = [
                None
            ]
        case "veze":
            # typ, (x, y)
            to_return = [
                initiated_game.Vez("test_tower", (350, 250), initiated_game),
                initiated_game.Vez("test_tower", (950, 650), initiated_game)    # dočasná
            ]
        case "doly":
            #
            to_return = [
                initiated_game.Doly(initiated_game, (220, 80))
            ]     # není dokončená třída
        case "vesnice":
            #
            to_return = [
                initiated_game.Vesnice(initiated_game, (150, 80))
            ]      # není dokončená třída
        case "cesty":
            to_return = [
                initiated_game.Cesta(initiated_game, 115, 55, 30, 100, "dolu"),
                initiated_game.Cesta(initiated_game, 115, 155, 180, 30, "doprava"),
                initiated_game.Cesta(initiated_game, 295, 155, 30, 180, "dolu"),
                initiated_game.Cesta(initiated_game, 145, 310, 180, 30, "doleva"),
                initiated_game.Cesta(initiated_game, 115, 310, 30, 180, "dolu"),
                initiated_game.Cesta(initiated_game, 115, 490, 500, 30, "doprava"),
                # rozcestník

                # horní cesta
                initiated_game.Cesta(initiated_game, 615, 140, 30, 300, "nahoru"),
                initiated_game.Cesta(initiated_game, 615, 110, 200, 30, "doprava"),
                initiated_game.Cesta(initiated_game, 815, 110, 30, 270, "dolu"),
                initiated_game.Cesta(initiated_game, 815, 380, 200, 30, "doprava"),
                initiated_game.Cesta(initiated_game, 1010, 130, 30, 280, "nahoru"),

                # dolní cesta
                initiated_game.Cesta(initiated_game, 615, 570, 30, 120, "dolu"),
                initiated_game.Cesta(initiated_game, 615, 690, 150, 30, "doprava"),
                initiated_game.Cesta(initiated_game, 765, 600, 30, 120, "nahoru"),
                initiated_game.Cesta(initiated_game, 765, 570, 270, 30, "doprava"),
                initiated_game.Cesta(initiated_game, 1035, 570, 30, 120, "dolu")
            ]
        case "skryte_cesty":        # Když je základna zničená, tak chodí po "skrýté" cestě, která vede k další základně
            to_return = [
                initiated_game.Cesta(initiated_game, 1010, 90, 100, 30, "doprava"),     # TODO: to ale funguje jen z jedný strany??
                initiated_game.Cesta(initiated_game, 1110, 90, 30, 610, "dolu"),
                initiated_game.Cesta(initiated_game, 1070, 700, 70, 30, "doleva")
            ]
        case "rozcesti":
            to_return = [
                initiated_game.Rozcesti(615, 440, "vertikalne")
            ]
        case _:
            to_return = [
                None
            ]

    return to_return