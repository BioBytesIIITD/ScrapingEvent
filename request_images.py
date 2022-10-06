import requests
import pandas as pd

df = pd.read_csv('asura_scans.csv')

images = df['Image'].tolist()
links = df['Link'].tolist()

for image, link in zip(images, links):
    fileName = link.split("/")[-2]
    f = open(f'images/{fileName}.jpg','wb')
    f.write(requests.get(image).content)
    f.close()