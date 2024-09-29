def load_entities(entity_type, initiated_game):

    match entity_type:
        case "zakladny":
            # obtiznost, x ,y
            to_return = [
                initiated_game.Zakladna(initiated_game.obtiznost, 605, 170)
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
                initiated_game.Vez("test_tower", (350, 250))   # dočasná
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
                initiated_game.Cesta(initiated_game, 615, 220, 30, 300, "nahoru")
            ]
        case _:
            to_return = [
                None
            ]

    return to_return