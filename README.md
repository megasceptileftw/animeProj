# Anime Video Player
I developed a Python-based CLI (command line interface) tool to index and manage a local video library. I created this project to help organize and watch the anime on my computer. Before I made this project, I would have to open mpv and drag/drop each file into the player. This process was ok, but oftentimes I would be trying to watch anime on the couch and my cat would sit on top of me and I would be unable to get up and start the next episode. 

## How it's made:

**Tech Used:** Python, SQLite

I used Python's os and pathlib libraries to scan directories for the necessary files and sort anime episodes with their respective captions. This was necessary when I drag/dropped the episodes into the player because you can force mpv to use captions in the same folder (I want to use Japanese subtitles for Japanese learning). Furthermore, I used CRUD (Create, Read, Update, Delete) Operations to manage the content on the user's device and track episode progress.

## Current Drawbacks:

The program is built to sort anime downloaded anime that is just a folder of episodes (already sorted). This is because I was building this around watching Cardcaptor Sakura; however, as I download more anime I will update it to support different cases that I encounter.

## Lessons Learned:

I have learned how to programmatically navigate/manipulate the file system using Python. I also gained experience in database state management by using SQLite to track user progress across sessions. Finally, I learned process orchestration by using Python to interface with and control external applications like mpv.

## How to use:

1. Clone the repo:
    ```bash
    git clone https://github.com/megasceptileftw/animeProj.git
    ```

2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```