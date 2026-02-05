import os
from sortingAnimeFn import sort_anime, unsort_anime
from animeDatabase import getConnection, createAnimeTable, createEpWatchedTable
from animeWatching import watch_anime

def main():
    try:
        connection = getConnection("anime.db")
        createAnimeTable(connection)
        createEpWatchedTable(connection)

        while True:
            print("Anime!")
            print("1) Watch Anime")
            print("2) Sort Anime")
            print("3) Unsort Anime")

            choice = select_option()

            match choice:
                case "Watch Anime":
                    os.system('cls')
                    watch_anime(connection)
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
    while True:
        try:
            options = int(input("Make a selection (0 to exit selection): "))
            match options:
                case 0:
                    print("Exiting")
                case 1:
                    selection = "Watch Anime"
                case 2:
                    selection = "Sort Anime"
                case 3:
                    selection = "Unsort Anime"
                case _:
                    print("invalid selction")
                    selection = select_option()
            return selection
        except ValueError:
                print("Not an integer value :(")

main()