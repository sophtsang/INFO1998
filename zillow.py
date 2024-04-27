from info import *
from model import *
import requests
import pandas as pd

class Zillow(object):
    ws = WebScrape()
    # Create dataframe with data of sold houses in same region that user inputted url: target = price[0], percent change = rate of price increase
    #results = ws.scrape(url = "https://www.zillow.com/somerset-county-nj/sold/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A40.758005%2C%22south%22%3A40.374397%2C%22east%22%3A-74.401839%2C%22west%22%3A-74.797841%7D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22rs%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A2552%2C%22regionType%22%3A4%7D%5D%2C%22pagination%22%3A%7B%7D%7D")
    results = ws.fromJson("zillowdata.json")
    df = ws.getDataFrame(results)
    df.to_csv('data.csv')

    model = Model() 
    values = model.linearModel("08540", 1700, 10000, df)   #TODO: fill INNNNNNNNN! 
    print('Linear Regression:' + values) 

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
