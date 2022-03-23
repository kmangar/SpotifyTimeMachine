from bs4 import BeautifulSoup
import requests
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

# Create an input() prompt that asks what year you would like to travel to in YYYY-MM-DD format. e.g.
travel_date = input("Which year would you like to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{travel_date}"

response = requests.get(URL)
chart = response.text

soup = BeautifulSoup(chart, "html.parser")

song_titles = [title.text.strip() for title in soup.find_all(name="h3", class_="u-letter-spacing-0021", id="title-of-a-story")]
scraped_art = [artist.getText().strip("\n") for artist in soup.find_all(name="span", class_="c-label")]
print(scraped_art)
print(song_titles)

# print(song_titles[::3][1])
valueToBeRemoved = 'Imprint/Promotion Label:'
myList = [value for value in song_titles if value != valueToBeRemoved]
valueToBeRemoved2 = 'Producer(s):'
newList = [value for value in myList if value != valueToBeRemoved2]
valueToBeRemoved3 = 'Songwriter(s):'
song_names = [value for value in newList if value != valueToBeRemoved3]

total = []
value = 0
for song in song_names:
    value = value + 1
    total.append(f"{value}. {song}\n")


artist_names = [artist.split(" Featuring")[0].split(" Duet")[0].replace("Ke$ha", "Kesha") for artist in scraped_art
                if not artist.isnumeric()
                if artist != "-"
                if artist != "NEW"
                if 'ENTRY' not in artist
                ]

artist_names = [x.replace('\t', '').replace('\n', '').replace('NEW', '').replace('-', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '') for x in artist_names ]
print(song_names)

while "" in artist_names:
    artist_names.remove("")

print(artist_names)


def authorization_flow(scope=""):

    # Create a Spotify API Client
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id='SPOTIPY_CLIENT_ID',
            client_secret='SPOTIPY_CLIENT_SECRET',
            redirect_uri="http://example.com",
            cache_path="token.txt",
            scope=scope
        )
    )
    return sp


sp = authorization_flow(scope="playlist-modify-private")


user_name = sp.current_user()["display_name"]
user_id = sp.current_user()["id"]

song_urls = []
for song, artist in zip(song_names, artist_names):
    items = sp.search(q=f"track: {song} artist: {artist}", type="track")["tracks"]["items"]
    if len(items) > 0:
        song_urls.append(items[0]["uri"])


playlist_id = sp.user_playlist_create(user=user_id, name=f"{travel_date} Billboard 100", public=False)["id"]

sp.playlist_add_items(playlist_id=playlist_id, items=song_urls)


# with open(f"{travel_date}.txt", "w") as file:
#     file.writelines(total)








