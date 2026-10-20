# eBay Scraper

`ebay-dl.py` is a command-line program that scrapes eBay search results. Given a search term, it downloads the first 10 pages of results, extracts each listing's name, price, condition, shipping cost, free returns, and number sold, and saves them as a JSON file named after the search term. Prices and shipping are stored in cents as integers.

This project is from CSCI 40: [Project 2: Scraping eBay](https://csci40.rtealwitter.com/projects/02_webscraping/project.html)

## How to run it

Install the libraries:

```
python -m pip install requests beautifulsoup4
```

All three JSON files in this repo use the **artificial practice pages** from the course. These are the exact commands I ran:

```
python ebay-dl.py --search "garden tools" --pages-dir practice-pages
python ebay-dl.py --search "stuffed animal" --pages-dir practice-pages
python ebay-dl.py --search "golf clubs" --pages-dir practice-pages
```

To scrape live eBay instead, leave off `--pages-dir`:

```
python ebay-dl.py --search "garden tools"

```
CSV saves spreadsheet style file instead of JSON
```
python ebay-dl.py --search "garden tools" --pages-dir practice-pages --csv
python ebay-dl.py --search "stuffed animal" --pages-dir practice-pages --csv
python ebay-dl.py --search "golf clubs" --pages-dir practice-pages --csv
```