import requests
from bs4 import BeautifulSoup
res = requests.get('https://analytics.icmr.org.in/public/dashboard/149a9c89-de6d-4779-9326-5e8fed3323b6')
print(res.text)