import os
from pathlib import Path
import shutil


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

    full_path = os.path.join(episodes_path, curr_directory_name)

    try:
        os.mkdir(full_path)
        print(f"Directory '{curr_directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{curr_directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{curr_directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    needed_cap_path = Path(cap_path_txt+"\\"+captions[curr_ep-1])
    needed_ep_path = Path(ep_path_txt+"\\"+episodes[curr_ep-1])

    move_cap = shutil.move(needed_cap_path, full_path)
    move_ep = shutil.move(needed_ep_path, full_path)

    curr_ep = curr_ep + 1