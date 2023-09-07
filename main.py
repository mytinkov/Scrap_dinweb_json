import requests
from bs4 import BeautifulSoup
import lxml
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

# Collect all fests URLs
fests_urls_list = []

for i in range(0, 120, 24):

    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&where%5B%5D=2&where%5B%5D=3&where%5B%5D=4&maxprice=500&o={i}&bannertitle=September"

    req = requests.get(url=url, headers=headers)
    json_data = json.loads(req.text)
    html_response = json_data['html']

    with open(f'data/index_{i}.html', 'w') as file:
        file.write(html_response)

    with open(f'data/index_{i}.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    cards = soup.find_all('a', class_='card-details-link')

    for item in cards:
        fest_url = 'https://skiddle.com' + item.get('href')
        fests_urls_list.append(fest_url)

# Collect fest info
count = 0
fest_list_result = []
for url in fests_urls_list:
    count += 1
    print(count)
    print(url)

    req = requests.get(url=url, headers=headers)

    try:
        soup = BeautifulSoup(req.text, 'lxml')
        fest_info_block = soup.find('div', class_='MuiContainer-root')
        fest_name = fest_info_block.find('h1').text.strip()
        fest_info_block = soup.find('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol')
        fest_date = fest_info_block.find('span').text.strip() + ", " + fest_info_block.findNext('span').findNext(
            'span').text.strip()
        fest_local = fest_info_block.findNext('span').findNext('span').findNext('span').text.strip()

        fest_list_result.append(
            {
                "Fest name": fest_name,
                "Fest date": fest_date,
                "Fest local": fest_local
            }
        )

    except Exception as ex:
        print(ex)
        print('Damn...There was same error...')

with open('fest_list_result.json', 'a', encoding='utf-8') as file:
    json.dump(fest_list_result, file, indent=4, ensure_ascii=False)
