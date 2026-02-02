import os

# necessary (in conjunction with libmpv-2.dll) for 'import mpv' to work, make sure to add 'libmpv-2.dll' to this folder
path = os.path.dirname(os.path.abspath(__file__))

os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]

import mpv
from pathlib import Path
from sortingAnimeFn import displayAnime
from animeDatabase import fetchAnime
import glob
import threading

episode_ended = threading.Event()

player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, osc=True, keep_open ='yes')
player.fullscreen = True

# observing when the end of episode is reached
@player.property_observer('eof-reached')
def check_eof(_name, value):
    # if the end of episode is reached, we set the flag to be true
    if value is True:
        episode_ended.set()


def watch_anime(connection):

    # displaying the anime in the database currently
    displayAnime(connection)

    # getting user input for the anime they want to watch
    while True:
        anime2watch = input("Which anime would you like to watch?: ")
        animeTup = fetchAnime(connection, anime2watch)
        if animeTup != None:
            break
        print("Anime not found, try again")

    # animeTup is currently set as (title of anime, path to location of captions originally, path to location of episodes, number of episodes)
    num_ep = animeTup[3]

    ep_path_txt = animeTup[2]
    episodes_path = Path(ep_path_txt)

    # each directory should be 'title of anime' + ' EP ' + 'episode numer ' after everything is sorted
    directory_name = animeTup[0] + " EP"

    # getting user input for what episode they want to watch
    while True:
        try:
            ep2watch = int(input("What episode do you want to watch?: "))

            if 0 < ep2watch < num_ep:
                break
            else:
                print("Episode is not in this anime, try again")

        except ValueError:
            print("Not an integer value :(")
    
    # asking user if they want to turn on autoplay
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

    # queue for the episodes
    queue = []

    # curr_ep is the variable to iterate through
    curr_ep = ep2watch

    # iterating through the folders and files and adding them to the queue as a tuple (vidFile, capFile)
    while curr_ep < num_ep+1:
        # setting up the correct path for the current episode
        curr_directory_name = directory_name + f"{curr_ep}"
        curr_dir_path_txt = ep_path_txt + "\\" + curr_directory_name

        # finding the vidFile
        for file in glob.glob(curr_dir_path_txt+"\\"+"*.mkv"):
            vidFile = file

        # finding the capFile
        for file in glob.glob(curr_dir_path_txt+"\\"+"*.srt"):
            capFile = file

        # appending them to the queue as a tuple
        if vidFile:
            queue.append((vidFile, capFile))
        
        # iterating curr_ep
        curr_ep += 1

    # feeding each video and caption one at a time to play, so that the video doesn't autoplay when we don't want it to
    for vidFile, capFile in queue:

        # loading the first episode in the queue
        player.loadfile(vidFile, sub_file=capFile)

        # when the next episode plays (autoplay not on), it is paused, so we make sure it plays
        player.pause = False

        # waiting for end of episode to be flagged
        episode_ended.wait()

        # clearing the flag so we can use it again later
        episode_ended.clear()

        # if the autoplay is not on, we let the user choose if they want to watch next ep
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