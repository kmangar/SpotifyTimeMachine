from bs4 import BeautifulSoup
import requests

# Create an input() prompt that asks what year you would like to travel to in YYYY-MM-DD format. e.g.
travel_date = input("Which year would you like to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{travel_date}"

response = requests.get(URL)

chart = response.text

first_one = "c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet"
first_artist = "c-label  a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet"

all_the_rest = "c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"
rest_the_artists = "c-label  a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only"


soup = BeautifulSoup(chart, "html.parser")

# top_song = soup.find(name="h3", id="title-of-a-story", class_=all_the_rest)
# top_artist = soup.findAll(name="h3", class_=first_artist)

top_ninety_nine = soup.find_all(name="h3", class_="u-letter-spacing-0021", id="title-of-a-story")
top_ninety_nine_artist = soup.findAll(name="h3", class_=rest_the_artists)

song_titles = [song.getText() for song in top_ninety_nine]
artists_names = [artist.getText() for artist in top_ninety_nine_artist ]

song_titles = [title.text.strip() for title in top_ninety_nine]

# print(song_titles[::3][1])
valueToBeRemoved = 'Imprint/Promotion Label:'
myList = [value for value in song_titles if value != valueToBeRemoved]
valueToBeRemoved2 = 'Producer(s):'
newList = [value for value in myList if value != valueToBeRemoved2]
valueToBeRemoved3 = 'Songwriter(s):'
finalList = [value for value in newList if value != valueToBeRemoved3]

total = []
value = 0
for song in finalList:
    value = value + 1
    total.append(f"{value}. {song}\n")

with open(f"{URL}", "w") as file:
    file.write(total)



