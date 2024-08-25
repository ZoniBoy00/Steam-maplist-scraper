import requests
from bs4 import BeautifulSoup

# URL of the Steam Workshop collection
url = "https://steamcommunity.com/sharedfiles/filedetails/?id=COLLECTION_ID"

# Send a request to the Steam Workshop page
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
    exit()

# Parse the page content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all map names (items in the collection)
map_items = soup.find_all('div', class_='workshopItemTitle')

# Extract map names and save to maplist.txt
with open('maplist.txt', 'w') as file:
    for item in map_items:
        map_name = item.text.strip()
        file.write(f"{map_name}\n")

print("Map names have been saved to maplist.txt.")
