def main():
    from menu import menu_main

    menu_variables = menu_main()

    if menu_variables[2]:
        from game import game_main
        game_main(menu_variables[0], menu_variables[1])

if __name__ == "__main__":
    main()