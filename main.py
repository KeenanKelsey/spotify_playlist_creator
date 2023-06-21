from datetime import date
from unittest import result
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from dotenv import load_dotenv
import os


load_dotenv()  # take environment variables from .env.

date_input = input("please enter date of the top 100 songs you want (YYYY-MM-DD):\n>")
content = requests.get("https://www.billboard.com/charts/hot-100/" + date_input)
soup = BeautifulSoup(content.text, "html.parser")
year = date_input.split('-')[0]

song_artist = soup.find_all(name="span", class_="a-no-trucate") # the class changes often. Will need to inspect page to change the class_ value


# song_title =  soup.find_all(name="h3",class_="a-no-trucate")
song_title =  soup.find_all(name='h3', class_="a-font-primary-bold-s")

s_artist = []
s_title = []


for x in song_title:
        # print(x.text.strip())
        s_title.append(x.text.strip())



for x in song_artist:
        # print(x.text.strip())
        s_artist.append(x.text.strip())


combined = zip(s_artist,s_title[2:])


for x, y in combined:
        # May need to write playlist_id to file and fetch it
        with open('playlist'+'_'+date_input+".txt", "a+") as file:
                file_path = '/playlists/'
                if file.name in file_path:
                        os.remove(file.name)
                else:
                        os.path.join(file_path, file)
                        file.write(x + ' ' + y + "\n")
                        
                

        print(x, y)

# check to see if playlist already exists.
user_playlists= []
user_id = '316cbhpn3c6p7x3osoz3kb7spyli'
playlist_mods = [
        "playlist-read-collaborative",
        "playlist-modify-public",
        "playlist-read-private",
        "playlist-modify-private"
]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        scope=playlist_mods))



# Create Playlist
sp.user_playlist_create(user=user_id,
    name=f"BILLBOARD 100 {date_input}",
    public=False,
    description=f"This playlist comprises of the top 100 songs on this date: {date_input}")

# # Get playlist id's
playlist_id = sp.current_user_playlists()['items'][0]['id']
print(playlist_id)





result = sp.search(q='Kendrick Lamar', type='artist')
artist_id = result['artists']['items'][0]['id']
# Add songs to playlist
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=artist_id )

