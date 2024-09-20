def load_entities(entity_type, initiated_game):

    match entity_type:
        case "zakladny":
            # obtiznost, x ,y
            to_return = [initiated_game.Zakladna(initiated_game.obtiznost, 50, 50)]
        case "spawnery":
            # hra_instance, x ,y
            to_return = [initiated_game.Spawner(initiated_game, 100, 50)]
        case "nepratele":
            # typ_nepritele     vrací se prázdné, spawnery je tvoří
            to_return = [None]
        case "veze":
            # typ, (x, y)
            to_return = [initiated_game.Vez("test_tower", (75, 50))]        # dočasná
        case "doly":
            #
            to_return = [initiated_game.Doly()]     # není dokončená třída
        case "vesnice":
            #
            to_return = [initiated_game.Vesnice()]      # není dokončená třída
        case _:
            to_return = [None]

    return to_return