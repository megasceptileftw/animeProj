import os

# necessary (in conjunction with libmpv-2.dll) for 'import mpv' to work, make sure to add 'libmpv-2.dll' to this folder
path = os.path.dirname(os.path.abspath(__file__))

os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]

import mpv
from pathlib import Path
from sortingAnimeFn import displayAnime
from animeDatabase import fetchAnime, insertEp, fetchEp, updateEp
import glob
import threading
import msvcrt as m
import time

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

        # setting the default start time of episodes to 0
        startTime = 0
        # getting the tuple for the episode status if it exists
        epTup = fetchEp(connection, vidFile)

        # if the user is not using autoplay
        if not autoplay:
            # if there is data on the episode
            if epTup != None:
                # if the episode is not completed
                if epTup[1] < 1501:
                    # ask the user if they want to resume the episode where it was previously ended and set the start time accordingly
                    while True:
                        question = input(f"The episode was previously ended at {round(epTup[1]/60, 2)} minutes, would you like to start there (type 'yes' or 'no')?: ").strip().lower()
                        if question == "yes":
                            startTime = epTup[1]
                            break
                        elif question == "no":
                            startTime = 0
                            break
                        else:
                            print("Wrong input, try again")

        # loading the first episode in the queue
        player.loadfile(vidFile, sub_file=capFile, start=startTime)

        # when the next episode plays (autoplay not on), it is paused, so we make sure it plays
        player.pause = False

        print("Press 'q' to quit the episode, press 'a' to toggle autoplay")
        # waiting for end of episode to be flagged
        while not episode_ended.is_set():
            # checking if the keyboard is hit
            if m.kbhit():
                key = m.getch()
                # if the 'q' key is pressed, quit the episode and insert or update the status of the episode to the EpWatched table
                if key == b'q':
                    if epTup == None:
                        insertEp(connection, vidFile, player.time_pos, 0) # insert the episode if it isn't already, set completed to 0 because the episode hasn't been completed yet
                    else:
                        updateEp(connection, vidFile, player.time_pos, epTup[2]) # update the episode if it is already in the table
                    player.stop()
                    return
                # if the 'a' key is pressed, turn on/off autoplay
                if key == b'a':
                    if autoplay:
                        autoplay = False
                        print("autoplay is now off")
                    else:
                        autoplay = True
                        print("autoplay is now on")

            # let the cpu not cook
            time.sleep(0.1)
            

        # clearing the flag so we can use it again later
        episode_ended.clear()

        # update the status of an episode at the end also
        if epTup == None:
            insertEp(connection, vidFile, player.time_pos, 1) # insert the episode if it isn't already, set completed to 1 bc ep is now completed
        else:
            updateEp(connection, vidFile, player.time_pos, epTup[2]+1) # update the episode if it is already in the table, iterate completed bc ep is now completed

        # if the autoplay is not on, we let the user choose if they want to watch next ep
        if not autoplay:
            while True:
                cont = input("Do you want to watch the next episode(type 'yes' or 'no')?: ").strip().lower()
                if cont == "yes":
                    break
                elif cont == "no":
                    player.stop()
                    return
                else:
                    print("Wrong input, try again")