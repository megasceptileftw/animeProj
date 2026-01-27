import os
from pathlib import Path
import shutil
import glob

directory_name = "Cardcaptor Sakura EP"
num_ep = 70
curr_ep = 1

cap_path_txt = "C:\\Users\\megas\\OneDrive\\Desktop\\Cardcaptor Sakura (01-70)"
ep_path_txt = "D:\\Apps\\Anime stuff\\Cardcaptor Sakura Episodes"

captions_path = Path(cap_path_txt)
episodes_path = Path(ep_path_txt)

captions = os.listdir(captions_path)
episodes = os.listdir(episodes_path)

while curr_ep < num_ep+1:
    
    curr_directory_name = directory_name + f"{curr_ep}"

    curr_dir_path_txt = ep_path_txt + "\\" + curr_directory_name
    curr_dir_path = Path(curr_dir_path_txt)
    curr_dir = os.listdir(curr_dir_path)

    for file in glob.glob(curr_dir_path_txt+"\\"+"*.srt"):
        move_cap = shutil.move(file, captions_path)
    
    for file in glob.glob(curr_dir_path_txt+"\\"+"*.mkv"):
        move_ep = shutil.move(file, episodes_path)
    
    try:
        os.rmdir(curr_dir_path)
        print(f"Folder '{curr_dir_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"Error: Folder '{curr_dir_path}' not found.")
    except OSError as e:
        print(f"Error deleting folder {curr_dir_path}: {e}")

    curr_ep = curr_ep + 1