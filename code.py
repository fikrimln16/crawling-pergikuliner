import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

# Replace with the actual base URL from the website (after checking for permission)
base_url = "https://pergikuliner.com/hendy_christianto_chandra?city=Semua&date_range=&from_date=&last_view=2024-02-23&page="
page_range = range(1, 200)

df = pd.DataFrame(columns=['user', 'restoran', 'text', 'pesanan', 'harga', 'lokasi', 'kategori', 'rating'])

for page_number in page_range:
    url = f"{base_url}{page_number}&search_name_cuisine=&search_place=Bandung&to_date="

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    parent = soup.find('ul', class_="timeline")

    
    if parent:
        for child in parent.find_all('li'):

            # Extract rating
            ratings = child.find_all('span', class_="item-rating-result")
            for rating in ratings:
                rating_text = rating.text.strip()

            # Extract restoran name
            titles = child.find_all(class_="title-wrapper")
            for title in titles:
                restorans = title.find_all('a')
                for restoran in restorans:
                    restoran_name = restoran.text.strip()
            
            # Extract harga
            bottom_part = child.find_all('div', class_='bottom-part')
            for part in bottom_part:
                harga_text = part.text.strip()

            # Extract pesanan
            pesanan = child.find_all('span', class_="bold")
            for part in pesanan:
                pesanan_text = part.text.strip()
                
            # Extract review
            top_part = child.find_all(class_="top-part")
            for review in top_part:
                review_text = review.text.strip()

            # Extract restoran name
            lokasi = child.find_all(class_="title-wrapper")
            for lok in lokasi:
                located = lok.find_all('span')
                for tempat in located:
                    lokasi_text = tempat.text.strip()

                    # Split lokasi_text menjadi dua kata
                    lokasi_split = lokasi_text[2:-2].split(",")
                    if len(lokasi_split) == 2:
                        lokasi_1 = lokasi_split[0].strip()
                        lokasi_2 = lokasi_split[1].strip()
                    else:
                        lokasi_1 = lokasi_text.strip()
                        lokasi_2 = ""

                    # Append new data to the DataFrame
                    df = df.append({
                          'user': "hendy_christianto_chandra",
                          'restoran': restoran_name, 
                          'text': review_text, 
                          'pesanan' : pesanan_text,
                          'harga' : harga_text.split('orang:')[1][:-50], 
                          'lokasi': lokasi_1,
                          'kategori': lokasi_2,
                          'rating': rating_text
                        }, ignore_index=True)
    else:
        print("Parent element (ul with class='timeline') not found")

# Save the DataFrame to a CSV file
df.to_csv('hendy_christianto_chandra.csv', index=False)
