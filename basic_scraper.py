import bs4 as beautifulsoup
import requests
import pandas as pd

single_page_url = "https://asura.gg/"

def get_page(url):
    res = requests.get(url)
    soup = beautifulsoup.BeautifulSoup(res.text, "html.parser")
    return soup

def get_divs_by_class(soup, class_name):
    return soup.find_all("div", class_=class_name)

page = get_page(single_page_url)
div_title_info = get_divs_by_class(page, "luf")
div_image_info = get_divs_by_class(page, "imgu")

ls = []

for tdiv, idiv in zip(div_title_info, div_image_info):
    min_ls = []
    min_ls.append(tdiv.a['href'])
    min_ls.append(tdiv.a['title'])
    min_ls.append(idiv.a.img['src'])
    ls.append(min_ls)

print(ls)
df = pd.DataFrame(ls, columns=["Link", "Title", "Image"])
df.to_csv("asura_scans.csv", index=False)