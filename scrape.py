import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter

webPage = "http://quotes.toscrape.com"

def get_quotes():
    quotes = []
    url = "/page/1"
    while url:
        response = requests.get(f"{webPage}{url}")
        whole_html = BeautifulSoup(response.text, "html.parser")
        all_quotes = whole_html.select("div.quote")

        for quote in all_quotes:
            quotes.append({
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "link": quote.find("a")["href"]
            })
        next_button = whole_html.find(class_="next")
        url = next_button.find("a")["href"] if next_button else None
        sleep(1)
    return quotes

def write_to_csv(quotes):
    with open("quotes.csv", "w", encoding="utf-8") as csv_file:
        headers = ["text", "author", "link"]
        csv_writer = DictWriter(csv_file, fieldnames = headers)
        csv_writer.writeheader()

        for quote in quotes:
            csv_writer.writerow(quote)

quotes = get_quotes()
write_to_csv(quotes)