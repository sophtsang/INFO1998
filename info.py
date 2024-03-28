import json
import httpx
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from parsel import Selector

# Model that predicts % difference (increase) of market price to accepted offer: predicts how much over
# the market price you have to offer to guarantee an accepted offer in n neighborhood.

# TODO 1: Do web scraping on initial market vs final sold price of houses.
#         Web scrape Zillow, Redfin, other housing websites.
#         Maybe eventually apply to Cornell housing.
#         RESOURCES: https://scrapfly.io/blog/how-to-scrape-zillow/#scraping-properties

class Zillow(object):
    df = pd.read_csv("the file that I webscraped from Zillow")

    # def parse_property(data: dict) -> dict:
    #     """parse zillow property"""
    #     # zillow property data is massive, let's take a look just
    #     # at the basic information to keep this tutorial brief:
    #     parsed = {
    #         "address": data["address"],
    #         "description": data["description"],
    #         "photos": [photo["url"] for photo in data["galleryPhotos"]],
    #         "zipcode": data["zipcode"],
    #         "phone": data["buildingPhoneNumber"],
    #         "name": data["buildingName"],
    #         # floor plans include price details, availability etc.
    #         "floor_plans": data["floorPlans"],
    #     }
    #     return parsed


    # BASE_HEADERS = {
    #     "accept-language": "en-US,en;q=0.9",
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "accept-language": "en-US;en;q=0.9",
    #     "accept-encoding": "gzip, deflate, br",
    # }


    # url = "some zillow proprety url"
    # with httpx.Client(http2=True, headers=BASE_HEADERS, follow_redirects=True) as client:
    #     resp = client.get(url)
    # sel = Selector(text=resp.text)
    # data = json.loads(sel.css("script#__NEXT_DATA__::text").get())
    # print(parse_property(data))

    # TODO 2: Model the data. Features to predict final sold price include initial market price, neighborhood, time of year of sale,
            # bed and baths, age of house, house dimensions.
        
    # Correlation method: returns n columns of the given dataframe that contain the highest correlation with target column.
    # Requires that target column not be returned as one of the returned features.
    #
    # @param String target: target column to be predicted (housing final price)
    # @param int n: number of features to be returned

    def correlate(self, target, n):
        matrix = self.df.corr()
        features = abs((matrix.loc[target])-1).sort_values().tail(n)
        return self.df[features.keys()]

    # TODO 3: User interface. Takes in a url to the user's listing of choice, webscrapes the page, runs data through a model,
    #         and predicts final selling price that guarantees offer acceptance.

