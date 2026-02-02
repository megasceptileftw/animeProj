import os
from sortingAnimeFn import sort_anime, unsort_anime
from animeDatabase import getConnection, createTable

def main():
    try:
        connection = getConnection("anime.db")
        createTable(connection)

        while True:
            print("Anime!")
            print("1) Sort Anime")
            print("2) Unsort Anime")

            choice = select_option()

            match choice:
                case "Sort Anime":
                    os.system('cls')
                    sort_anime(connection)
                case "Unsort Anime":
                    os.system('cls')
                    unsort_anime(connection)
                case _:
                    return
    finally:
        connection.close()
    
            
def select_option():
    selection = ""
    options = int(input("Make a selection (0 to exit selection): "))
    match options:
        case 0:
            print("Exiting")
        case 1:
            selection = "Sort Anime"
        case 2:
            selection = "Unsort Anime"
        case _:
            print("invalid selction")
            selection = select_option()
    return selection

main()