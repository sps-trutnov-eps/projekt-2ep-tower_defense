def load_entities(entity_type, initiated_game):

    match entity_type:
        case "zakladny":
            # obtiznost, x ,y
            to_return = [
                initiated_game.Zakladna(initiated_game.obtiznost, 50, 50)
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
                initiated_game.Vez("test_tower", (75, 50))   # dočasná
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
                initiated_game.Cesta(initiated_game, 115, 155, 180, 30, "doprava")
            ]
        case _:
            to_return = [
                None
            ]

    return to_return