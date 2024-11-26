def load_entities(entity_type, initiated_game):
    match entity_type:
        case "zakladny":
            to_return = [
                initiated_game.Zakladna(initiated_game.obtiznost, 600, 50),
                initiated_game.Zakladna(initiated_game.obtiznost, 600, 700)
            ]
        case "spawnery":
            to_return = [
                initiated_game.Spawner(initiated_game, (100, 375), "doprava"),
                initiated_game.Spawner(initiated_game, (1133, 375), "doleva")
            ]
        case "nepratele":
            to_return = []
        case "veze":
            to_return = []
        case "vesnice":
            to_return = [
                # levá strana
                initiated_game.Vesnice(initiated_game, (315, 235), 25),
                initiated_game.Vesnice(initiated_game, (315, 535), 25),

                # pravá strana
                initiated_game.Vesnice(initiated_game, (910, 235), 25),
                initiated_game.Vesnice(initiated_game, (910, 535), 25)
            ]
        case "cesty":
            to_return = [
                # levý spawner
                initiated_game.Cesta(125, 391, 200, 30, "doprava"),

                # cesta dolů
                initiated_game.Cesta(325, 475, 30, 70, "dolu"),
                initiated_game.Cesta(325, 545, 70, 30, "doprava"),

                # cesta nahoru
                initiated_game.Cesta(325, 275, 30, 70, "nahoru"),
                initiated_game.Cesta(325, 245, 70, 30, "doprava"),

                # pravý spawner
                initiated_game.Cesta(950, 391, 200, 30, "doleva"),

                # cesta dolů
                initiated_game.Cesta(920, 475, 30, 70, "dolu"),
                initiated_game.Cesta(880, 545, 70, 30, "doleva"),

                # cesta nahoru
                initiated_game.Cesta(920, 275, 30, 70, "nahoru"),
                initiated_game.Cesta(880, 245, 70, 30, "doleva"),

                # spawnery
                initiated_game.Cesta(610, 740, 30, 30, "nahoru"),
                initiated_game.Cesta(610, 40, 30, 30, "dolu")
            ]
        case "skryte_cesty":
            to_return = []
        case "rozcesti":
            to_return = [
                # levy spawner
                initiated_game.Rozcesti(325, 345, "vertikalne"),

                # pravy spawner
                initiated_game.Rozcesti(920, 345, "vertikalne"),

                # horni base
                initiated_game.Rozcesti(610, 175, "vertikalne"),

                # spodni base
                initiated_game.Rozcesti(610, 500, "vertikalne")
            ]
        case _:
            to_return = [None]

    return to_return