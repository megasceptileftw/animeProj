import os
from pathlib import Path
import shutil
import re
import glob
from animeDatabase import insertAnime, fetchAnime, fetchAnime4Tbl, deleteAnime
from table2ascii import table2ascii as t2a, PresetStyle

def get_anime_name():
    anime_name_pattern = r"[a-zA-Z0-9 \-\.!:']+$"
    while True:

        anime_name = input("Name of anime: ").strip()

        if re.fullmatch(anime_name_pattern, anime_name):
            print("Your anime's name is " + anime_name)
            break
        else:
            print("Your anime name is invalid, try again")

    return anime_name


def get_path(item):
    path_pattern = r"^[a-zA-Z]:\\\\[^<>:\"/|?*]+(\\\\[^<>:\"/|?*]+)*$"
    while True:
        path_txt = input(f"Path to {item} (remember to include double backslashes): ")
        if re.fullmatch(path_pattern, path_txt):
            print("The path to your captions is " + path_txt)
            break
        else:
            print("Your path is invalid, try again")
    
    return path_txt


def sort_anime(connection):

    anime_name = get_anime_name()
    directory_name = anime_name + " EP"

    cap_path_txt = get_path("captions")
    captions_path = Path(cap_path_txt)
    captions = os.listdir(captions_path)

    ep_path_txt = get_path("episodes")
    episodes_path = Path(ep_path_txt)
    episodes = os.listdir(episodes_path)

    num_ep = len(episodes)
    print(f"Your anime has {num_ep} episodes")

    decision = False
    while decision == False:
        print("Do you wish to proceed?")
        answer = input("Type 'yes' or 'no' to continue: ").strip().lower()
        if answer == "yes":
            decision = True
        elif answer == "no":
            return
        else:
            print("Invalid Input, try again")

    curr_ep = 1

    while curr_ep < num_ep+1:

        curr_directory_name = directory_name + f"{curr_ep}"

        full_path = os.path.join(episodes_path, curr_directory_name)

        try:
            os.mkdir(full_path)
        except FileExistsError:
            print(f"Directory '{curr_directory_name}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{curr_directory_name}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        needed_cap_path = Path(cap_path_txt+"\\"+captions[curr_ep-1])
        needed_ep_path = Path(ep_path_txt+"\\"+episodes[curr_ep-1])

        shutil.move(needed_cap_path, full_path)
        shutil.move(needed_ep_path, full_path)

        curr_ep = curr_ep + 1
    
    os.system('cls')
    print("Your anime has been sorted!")

    insertAnime(connection, anime_name, cap_path_txt, ep_path_txt, len(episodes))

def unsort_anime(connection):

    displayAnime(connection)

    while True:
        anime2unsort = input("Which anime would you like to unsort?: ")
        animeTup = fetchAnime(connection, anime2unsort)
        if animeTup != None:
            break
        print("Anime not found, try again")
    
    cap_path_txt = animeTup[1]
    captions_path = Path(cap_path_txt)

    ep_path_txt = animeTup[2]
    episodes_path = Path(ep_path_txt)

    directory_name = animeTup[0] + " EP"

    num_ep = animeTup[3]

    decision = False
    while decision == False:
        print("Do you wish to proceed?")
        answer = input("Type 'yes' or 'no' to continue: ").strip().lower()
        if answer == "yes":
            decision = True
        elif answer == "no":
            os.system('cls')
            return
        else:
            print("Invalid Input, try again")

    curr_ep = 1

    while curr_ep < num_ep+1:
    
        curr_directory_name = directory_name + f"{curr_ep}"

        curr_dir_path_txt = ep_path_txt + "\\" + curr_directory_name
        curr_dir_path = Path(curr_dir_path_txt)

        for file in glob.glob(curr_dir_path_txt+"\\"+"*.srt"):
            shutil.move(file, captions_path)
        
        for file in glob.glob(curr_dir_path_txt+"\\"+"*.mkv"):
            shutil.move(file, episodes_path)
        
        try:
            os.rmdir(curr_dir_path)
        except FileNotFoundError:
            print(f"Error: Folder '{curr_dir_path}' not found.")
        except OSError as e:
            print(f"Error deleting folder {curr_dir_path}: {e}")

        curr_ep = curr_ep + 1
    
    os.system('cls')
    print("Your anime has been unsorted!")
    
    deleteAnime(connection, animeTup[0])


def displayAnime(connection):
    currDB = fetchAnime4Tbl(connection)

    chartBody = []

    for entry in currDB:
        chartBody.append([entry[0], entry[1]])
    
    output = t2a(
        header=["Anime", "NumEPs"],
        body=chartBody
    )

    print(output)