import requests
from bs4 import BeautifulSoup
import time
from multiprocessing.pool import ThreadPool as Pool
import pandas as pd
import os

df = pd.read_csv('asura_scans.csv')

links = df['Link'].tolist()

def get_page(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup

def get_divs_by_class(soup, class_name):
    return soup.find("div", class_=class_name)

def get_details(url):
    page = get_page(url)
    main_box = get_divs_by_class(page, "entry-content entry-content-single")
    p_tags = main_box.find_all("p")
    return p_tags
    
def preprocess_data(data):
    for i in range(len(data)):
        data[i] = data[i].text
    data = " ".join(data)
    data = data.replace("<p>", "")
    data = data.replace("</p>", "")
    data = data.replace("<strong>", "")
    data = data.replace("</strong>", "")
    data = data.replace("<em>", "")
    data = data.replace("</em>", "")
    data = data.replace("<br/>", "")
    data = data.replace("<br>", "")
    return data

def scrape_single_page(link):
    data = get_details(link)
    data = preprocess_data(data)
    fileName = link.split("/")[-2]
    with open("scraped/" + fileName + ".txt", "w") as f:
        f.write(data)

def sequential_scrape():
    data = []
    for link in links:
        data.append(scrape_single_page(link))

def parallel_scrape():
    pool = Pool(os.cpu_count())

    for i in links:
        pool.apply_async(scrape_single_page, args=(i,))
        
    pool.close()
    pool.join()

# Time sequential scrape
start = time.time()
sequential_scrape()
end = time.time()

print("Sequential scrape took: ", end - start)

# Time parallel scrape
start = time.time()
parallel_scrape()
end = time.time()

print("Parallel scrape took: ", end - start)