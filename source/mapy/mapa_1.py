def load_entites(entity_type, initiated_game):

    match entity_type:
        case "zakladny":
            # obtiznost, x ,y
            to_return = [initiated_game.Zakladna(hra.obtiznost, 50, 50)]
        case "spawnery":
            # hra_instance, x ,y
            to_return = [initiated_game.Spawner(hra, 100, 50)]
        case "nepratele":
            # typ_nepritele     vrací se prázdné, spawnery je tvoří
            to_return = []
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