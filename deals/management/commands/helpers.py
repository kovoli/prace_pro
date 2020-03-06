import csv
from bs4 import BeautifulSoup


def clean_desc(html):
    soup = BeautifulSoup(html, "html.parser")
    tag_list = soup.findAll(True)
    for t in tag_list:
        del t.attrs['class']
    return soup


def open_csv():
    data = {}
    with open('../imports/yan.csv') as deal_csv:
        reader = csv.DictReader(deal_csv, delimiter=',')
        for row in reader:
            data['name'] = row['name']
            data['price'] = row['price']
            data['oldprice'] = row['oldprice']
            data['description'] = clean_desc(row['description'])
            data['image'] = row['image']
            data['brand'] = row['brand']
            data['shop'] = row['shop']
            data['category'] = row['category']
            data['link_to_shop'] = row['link_to_shop']

        return data

print(open_csv())
