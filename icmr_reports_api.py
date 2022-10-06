#Cards scraped from https://analytics.icmr.org.in/public/dashboard/149a9c89-de6d-4779-9326-5e8fed3323b6

import json
import requests, csv

url = 'https://analytics.icmr.org.in/api/public/dashboard/149a9c89-de6d-4779-9326-5e8fed3323b6'
request_headers = {'Accept': 'application/json',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
'Connection': 'keep-alive',
'Content-Type': 'application/json',
'Host': 'analytics.icmr.org.in',
'Referer': 'https://analytics.icmr.org.in/public/dashboard/149a9c89-de6d-4779-9326-5e8fed3323b6',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'Sec-GPC': '1',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
}

def save_as_csv(data:json,id):
    data = data['data']
    headers = []
    for col in data['cols']:
        headers.append(col['display_name'])
    file = open(str(id)+'.csv','w')
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(data['rows'])
    return file.name

def get_cards():
    print('Fetching cards...')
    res = requests.get(url,headers=request_headers)
    if not res.ok:
        print('Error fetching cards!')
        exit(0)
    res = res.json()
    cards = []
    for card in res['ordered_cards']:
        try:
            card = card['card']
            card_id = card['id']
            card_name = card['name']
        except KeyError:
            continue
        cards.append((card_id,card_name))
    print('Fetched all the cards!')
    print()
    return cards

def scrape_cards(cards):
    for card in cards:
        request_url = url + '/card/' + str(card[0]) + '?parameters=%5B%5D'
        print('Card Name:',card[1])
        print('Fetching URL:',request_url)
        res = requests.get(request_url,headers=request_headers)
        if not res.ok:
            print('Could not fetch URL:',request_url,'! Continuing....')
            continue
        print('URL:',request_url,'fetched!')
        print('Saving as csv...')
        file_name = save_as_csv(res.json(),card[0])
        print('CSV saved as:',file_name)
        print()

cards = get_cards()
with open('keys.txt','w') as file:
    for card in cards:
        file.write(f"{card[0]}, {card[1]}\n")
print(cards)
# scrape_cards(cards)