from pprint import pprint
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import csv
from collections import Counter

import warnings
warnings.filterwarnings("ignore")

def extract_card_extensions(url, headers):
    website = requests.get(url, headers = headers, timeout=5)
    soup = BeautifulSoup(website.content, "html.parser")
    extension_list = [i.a["href"] for i in soup.find_all(class_ = "deck-card")]
    # make sure only complete decks are returned (1 ruler + 40 main deck + 10 stone)
    if (len(extension_list) >= 51) and (len(extension_list) < 300):
        return Counter(extension_list)
    else:
        return {}


def extensions_to_cardname(extension, headers={'User-Agent': 'Mozilla/5.0'}):
    card_url = f"https://www.forceofwind.online{extension}"
    card_website = requests.get(card_url, headers = headers)
    card_soup = BeautifulSoup(card_website.content, "html.parser")
    card_name = card_soup.find(class_ = "card-text-info-text").text.strip()
    return card_name


def save_csv(name, card_dict):
    print(f"saving results to csv: {name}.csv ...")
    card_dict_sorted = {k: v for k, v in sorted(card_dict.items(), key=lambda item: item[1], reverse=True)}
    with open(f'{name}.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file,delimiter=";")
        for key, value in card_dict_sorted.items():
            writer.writerow([key, value])


def extract_card_distribution(url, headers):
    card_ext_distribution = Counter()
    # loop over decks and extract card extensions + occurences
    for deck_num in tqdm(range(1,2275), desc="Decks processed", colour="green"):
        deck_url = f"{url}/{deck_num}"
        card_ext_dict = extract_card_extensions(url=deck_url, headers=headers)
        card_ext_distribution += card_ext_dict
    # get names from card extensions
    card_names = [extensions_to_cardname(extension=ext) for ext in tqdm(card_ext_distribution,
                                                                        desc="get card names...",
                                                                        colour="green")]
    # change card extensions for names and save to dict
    final_card_distribution = {k: v for k, v in zip(card_names, card_ext_distribution.values())}
    save_csv(name="forceofwind", card_dict=final_card_distribution)

        




if __name__ == "__main__":
    url = "https://www.forceofwind.online/view_decklist"
    headers = {'User-Agent': 'Mozilla/5.0'}   

    extract_card_distribution(url=url, headers=headers)

