def load_entities(entity_type, initiated_game):

    match entity_type:
        case "zakladny":
            # obtiznost, x ,y
            to_return = [
            ]
        case "spawnery":
            # hra_instance, x ,y
            to_return = [
            ]
        case "nepratele":
            # typ_nepritele     vrací se prázdné, spawnery je tvoří
            to_return = [
            ]
        case "veze":
            # typ, (x, y)
            to_return = [   # dočasné, nemá vracet nic!
            ]
        case "vesnice":
            #
            to_return = [
            ]
        case "cesty":
            to_return = [

            ]
        case "skryte_cesty":        # Když je základna zničená, tak chodí po "skrýté" cestě, která vede k další základně
            to_return = [

            ]
        case "rozcesti":
            to_return = [

            ]
        case _:
            to_return = [
                None
            ]

    return to_return