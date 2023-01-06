import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictReader

webPage = "http://quotes.toscrape.com"

def read(filename):
    with open(filename, "r", encoding="utf-8") as csv_file:
        csv_reader = DictReader(csv_file)
        return list(csv_reader)

def game(quotes):
    quote = choice(quotes)
    remaining_lives = 4
    print("Your quote is: ")
    print(quote["text"])
    guess = ''

    while guess.lower() != quote["author"].lower() and remaining_lives > 0:
        guess = input(f"Guesses remaining: {remaining_lives}\nWhose quote is it? ")
        if guess.lower() == quote["author"].lower():
            print("Great job! You got the author right!")
            break

        remaining_lives -= 1
        
        if remaining_lives == 3:
            response = requests.get(f"{webPage}{quote['link']}")
            soup = BeautifulSoup(response.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text(),
            birth_place = soup.find(class_="author-born-location").get_text(),
            print(f"Here's hint number 1: The author was born on {birth_date}{birth_place}")
        elif remaining_lives == 2:
            print(f"Here's hint number 2: The author's first name starts with: {quote['author'][0]}")
        elif remaining_lives == 1:
            last_name = quote['author'].split(" ")[1][0]
            print(f"Here's hint number 3: The author's last name starts with {last_name}")
        else: print(f"You ran out of guesses! The correct answer was {quote['author']}")

    again = ''

    while again.lower() not in ['y', 'yes', 'n', 'no']:
        again = input("Would you like to play again? (y/n)")
    if again.lower() in ('yes', 'y'):
        return game(quotes)
    else:
        print("Goodbye, then!")

quotes = read("quotes.csv")
game(quotes)