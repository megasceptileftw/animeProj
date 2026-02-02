import os

path = os.path.dirname(os.path.abspath(__file__))

os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]

import mpv
from pathlib import Path
from sortingAnimeFn import displayAnime
from animeDatabase import fetchAnime
import glob
import threading

episode_ended = threading.Event()

autoplay = False

player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, osc=True, keep_open ='yes')
player.fullscreen = True

@player.property_observer('eof-reached')
def check_eof(_name, value):
    if value is True:
        episode_ended.set()


def watch_anime(connection):
    global autoplay

    displayAnime(connection)

    while True:
        anime2watch = input("Which anime would you like to watch?: ")
        animeTup = fetchAnime(connection, anime2watch)
        if animeTup != None:
            break
        print("Anime not found, try again")

    num_ep = animeTup[3]

    ep_path_txt = animeTup[2]
    episodes_path = Path(ep_path_txt)

    directory_name = animeTup[0] + " EP"

    while True:
        try:
            ep2watch = int(input("What episode do you want to watch?: "))

            if 0 < ep2watch < num_ep:
                break
            else:
                print("Episode is not in this anime, try again")

        except ValueError:
            print("Not an integer value :(")
    
    while True:
        autoplay_input = input("Would you like to turn on autoplay (type 'yes' or 'no')?: ").strip().lower()
        if autoplay_input == "yes":
            autoplay = True
            break
        elif autoplay_input == "no":
            autoplay = False
            break
        else:
            print("Invalid Input, try again")

    queue = []

    curr_ep = ep2watch

    while curr_ep < num_ep+1:
        curr_directory_name = directory_name + f"{curr_ep}"
        curr_dir_path_txt = ep_path_txt + "\\" + curr_directory_name

        for file in glob.glob(curr_dir_path_txt+"\\"+"*.mkv"):
            vidFile = file

        for file in glob.glob(curr_dir_path_txt+"\\"+"*.srt"):
            capFile = file

        if vidFile:
            queue.append((vidFile, capFile))
        
        curr_ep += 1

    for vidFile, capFile in queue:

        player.loadfile(vidFile, sub_file=capFile)

        player.pause = False

        episode_ended.wait()

        episode_ended.clear()

        if not autoplay:
            while True:
                cont = input("Do you want to watch the next episode(type 'yes' or 'no')?: ").strip().lower()
                if cont == "yes":
                    break
                elif cont == "no":
                    player.quit()
                    return
                else:
                    print("Wrong input, try again")