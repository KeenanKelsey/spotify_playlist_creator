import os

with open('playlist_2002-02-22.txt', 'w') as file:
    file_path = "./playlists"
    if file.name in os.listdir(file_path):
        print(f"{file.name} found in {file_path}")
    else:
        new_path = os.path.join(file_path,file.name)

    print(new_path)   