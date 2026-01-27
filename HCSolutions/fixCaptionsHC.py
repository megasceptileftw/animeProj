import os
from pathlib import Path
import pysubs2

cap_path_txt = "C:\\Users\\megas\\OneDrive\\Desktop\\Cardcaptor Sakura (01-70)"
captions_path = Path(cap_path_txt)
captions = os.listdir(captions_path)

mid_card_time = 595000
shift1 = -500
shift2 = 5500

for file in captions:
    sub_path = cap_path_txt + "\\" + file
    subs = pysubs2.load(sub_path, "utf-8")

    for line in subs:
        if line.start < mid_card_time:
            line.start += shift1
            line.end += shift1
        else:
            line.start += shift2
            line.end += shift2
    
    subs.save(sub_path)
    print(f"Fixed {file}")
