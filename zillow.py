from info import *
import requests
import pandas as pd

class Zillow(object):
    ws = WebScrape()
    results = ws.scrape(url = "https://www.zillow.com/new-haven-ct/")
    df = ws.getDataFrame(results)
    print(df)


if __name__ == 'info':
    Zillow()

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
