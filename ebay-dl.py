import argparse
import json
import csv
import time
import re

import requests
from bs4 import BeautifulSoup


def get_text(item, selector):
    tag = item.select_one(selector)
    if tag is None:
        return None
    return tag.text


def dollars_to_cents(text):
    match = re.search(r'(\d[\d,]*)(\.\d+)?', text)
    if match is None:
        return None
    dollars = int(match.group(1).replace(',', ''))
    if match.group(2) is None:
        cents = 0
    else:
        cents = int(match.group(2)[1:3].ljust(2, '0'))
    return dollars * 100 + cents


def parse_price(item):
    text = get_text(item, '.s-item__price')
    if text is None:
        return None
    return dollars_to_cents(text)


def parse_shipping(item):
    text = get_text(item, '.s-item__shipping')
    if text is None:
        return None
    if 'free' in text.lower():
        return 0
    return dollars_to_cents(text)


def parse_free_returns(item):
    text = get_text(item, '.s-item__free-returns')
    if text is None:
        return None
    return 'free returns' in text.lower()


def parse_items_sold(item):
    text = get_text(item, '.s-item__hotness')
    if text is None:
        return None
    match = re.search(r'\d[\d,]*', text)
    if match is None:
        return None
    return int(match.group().replace(',', ''))


def parse_listings(html):
    soup = BeautifulSoup(html, 'html.parser')
    listings = []
    for item in soup.select('.s-item'):
        listing = {
            'name': get_text(item, '.s-item__title'),
            'price': parse_price(item),
            'status': get_text(item, '.SECONDARY_INFO'),
            'shipping': parse_shipping(item),
            'free_returns': parse_free_returns(item),
            'items_sold': parse_items_sold(item),
        }
        listings.append(listing)
    return listings


def get_page_html(page_number, search, pages_dir):
    if pages_dir:
        path = pages_dir + '/page-' + str(page_number) + '.html'
        with open(path, encoding='utf-8') as f:
            return f.read()
    response = requests.get(
        'https://www.ebay.com/sch/i.html',
        params={'_nkw': search, '_pgn': page_number},
        headers={'User-Agent': 'Mozilla/5.0'},
        timeout=10,
    )
    response.raise_for_status()
    return response.text


parser = argparse.ArgumentParser(description='Download eBay search results as JSON.')
parser.add_argument('--search', required=True)
parser.add_argument('--pages-dir')
parser.add_argument('--csv', action='store_true')
args = parser.parse_args()

all_listings = []
for page_number in range(1, 11):
    html = get_page_html(page_number, args.search, args.pages_dir)
    page_listings = parse_listings(html)
    print('page', page_number, 'found', len(page_listings), 'listings')
    all_listings.extend(page_listings)
    if not args.pages_dir:
        time.sleep(1)

if args.csv:
    filename = args.search + '.csv'
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'price', 'status', 'shipping', 'free_returns', 'items_sold'])
        writer.writeheader()
        writer.writerows(all_listings)
else:
    filename = args.search + '.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_listings, f, indent=2)
print('saved', len(all_listings), 'listings to', filename)