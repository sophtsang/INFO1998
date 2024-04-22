import json
import requests
from bs4 import BeautifulSoup
# import httpx
# import numpy as np
import pandas as pd
import lxml as lxml
# from sklearn.model_selection import train_test_split
# from sklearn.neighbors import KNeighborsClassifier
# from parsel import Selector

# Model that predicts % difference (increase) of market price to accepted offer: predicts how much over
# the market price you have to offer to guarantee an accepted offer in n neighborhood.

# TODO 1: Do web scraping on initial market vs final sold price of houses.
#         Web scrape Zillow, Redfin, other housing websites.
#         Maybe eventually apply to Cornell housing.
#         RESOURCES: https://scrapfly.io/blog/how-to-scrape-zillow/#scraping-properties

class Zillow(object):
    # make region of houses user input: https://www.zillow.com/<city-state>/?searchQueryState=%7B"
    url = "https://www.zillow.com/ithaca-ny/?searchQueryState=%7B"
    data = {}
    df = pd.DataFrame(columns=["price", "area", "address"])
    l = list()
    req_headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.8',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/6.0'
            }
    r = requests.get(url, headers = req_headers)

    soup = BeautifulSoup(r.text, "html.parser")
    properties = soup.find_all("div", class_ = "StyledPropertyCardDataWrapper-c11n-8-100-7__sc-hfbvv9-0 bmhhEb property-card-data")

    for i in range (0, len(properties)):
        # price column
        try:
            data["price"] = properties[i].find("div", {"class" : "StyledPropertyCardDataArea-c11n-8-100-7__sc-10i1r6-0 imqyAK"}).text
        except:
            data["price"] = None
        # area
        try:
            data["area"] = properties[i].find("div", {"class" : "StyledPropertyCardDataArea-c11n-8-100-7__sc-10i1r6-0 eObjGE"}).text
        except:
            data["area"] = None
        # address
        try:
            data["address"] = properties[i].find("a", {"class" : "StyledPropertyCardDataArea-c11n-8-100-7__sc-10i1r6-0 izzuNb property-card-link"}).text
        except:
            data["address"] = None
        l.append(data)
        # find a way to save dictionary data as a dataframe
        df = pd.DataFrame(data)
    
    print(l)

    # TODO 2: Model the data. Features to predict final sold price include initial market price, neighborhood, time of year of sale,
            # bed and baths, age of house, house dimensions.
        
    # Correlation method: returns n columns of the given dataframe that contain the highest correlation with target column.
    # Requires that target column not be returned as one of the returned features.
    #
    # @param String target: target column to be predicted (housing final price)
    # @param int n: number of features to be returned

    # def correlate(self, target, n):
    #     matrix = self.df.corr()
    #     features = abs((matrix.loc[target])-1).sort_values().tail(n)
    #     return self.df[features.keys()]

    # TODO 3: User interface. Takes in a url to the user's listing of choice, webscrapes the page, runs data through a model,
    #         and predicts final selling price that guarantees offer acceptance.

if __name__ == 'info':
    Zillow()