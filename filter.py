import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml as lxml # type: ignore
import threading
from parsel import Selector

### Given the json results of a web-scraped Zillow page, filters important data into a dataframe.
df = pd.DataFrame(columns=["city", "state", "home status", "street address", "bedrooms", "bathrooms", "price", "rate of price change", 
                           "year built", "zipcode", "county", "home type", "monthly HOA", "zestimate", 
                           "nearby schools", "tax paid", "rate of tax change", "time on Zillow", "page view count", "favorite count",
                           "mortgage rate", "last sold price", "url", "lot area (acres)"])
f = open("data.json")

data = json.load(f)
# data[0].keys() to access all keys in dict
for dict in data:
    schools = [school.get("name") for school in dict.get("schools")]
    rating = [rate.get("rating") for rate in dict.get("schools")]
    nearby_schools = [{schools[n] : rating[n]} for n in range(0, len(schools))]
    try: 
        tax_paid = dict.get("taxHistory")[0].get("taxPaid")
    except: 
        tax_paid = None
    try:
        tax_inc = dict.get("taxHistory")[0].get("taxIncreaseRate")
    except:
        tax_inc = None
    try :
        price_inc = dict.get("priceHistory")[0].get("priceChangeRate")
    except:
        price_inc = None

    df.loc[len(df.index)] = [dict.get("city"), dict.get("state"), dict.get("homeStatus"), dict.get("address").get("streetAddress"), 
                             dict.get("bedrooms"), dict.get("bathrooms"), dict.get("price"), price_inc,
                             dict.get("yearBuilt"), dict.get("zipcode"), dict.get("county"), dict.get("homeType"), dict.get("monthlyHoaFee"),
                             dict.get("zestimate"), nearby_schools, tax_paid, tax_inc, dict.get("timeOnZillow"), dict.get("pageViewCount"),
                             dict.get("favoriteCount"), dict.get("mortgageRates").get("thirtyYearFixedRate"), dict.get("lastSoldPrice"),
                             "zillow.com" + dict.get("hdpUrl"), dict.get("lotAreaValue")]

f.close()