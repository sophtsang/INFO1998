import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml as lxml
from parsel import Selector
import threading

# Model that predicts % difference (increase) of market price to accepted offer: predicts how much over
# the market price you have to offer to guarantee an accepted offer in n neighborhood.

# TODO 1: Do web scraping on initial market vs final sold price of houses.
#         Web scrape Zillow, Redfin, other housing websites.
#         Maybe eventually apply to Cornell housing.
#         RESOURCES: https://scrapfly.io/blog/how-to-scrape-zillow/#scraping-properties

### WebScrape class provides live webscraping of a search page on Zillow and outputs a DataFrame containing data on the first 40 houses
### displayed on the search page.
class WebScrape(object):
    links = list()
    results = list()
    pool = list()
    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Chrome/124.0.6367.60'
    }   

    ###
    def scrape(self, url):
        r = requests.get(url, headers = self.req_headers)
        print(r.status_code)
        selector = Selector(r.text)
        data = selector.css("script#__NEXT_DATA__::text").get()
        data = data.replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace(",", "").split('"')
        for i in range(0, len(data)):
            self.links.append(data[i]) if ("homedetails" in data[i]) and not data[i] in self.links else None


        for n in range(0, len(self.links)):
            self.pool.append(threading.Thread(target = self.target, args = (n,)))
            self.pool[-1].start()

        # wait for all threads in pool to finish before next line runs
        for thread in self.pool: thread.join()

        # if len(l) = 1, then user inputted link
        with open("data.json", "w") as f:
            json.dump(self.results, f)
        
        return self.results
    
    ###
    def target(self, n):
            r = requests.get(self.links[n], headers = self.req_headers)
            selector = Selector(r.text)
            data = selector.css("script#__NEXT_DATA__::text").get()
            if data:
                data = json.loads(data)
                property_data = json.loads(data["props"]["pageProps"]["componentProps"]["gdpClientCache"])
                property_data = property_data[list(property_data)[0]]['property']
            else:
                # Option 2: other times it's in Apollo cache
                data = selector.css("script#hdpApolloPreloadedData::text").get()
                data = json.loads(json.loads(data)["apiCache"])
                property_data = next(
                    v["property"] for k, v in data.items() if "ForSale" in k
                )
            self.results.append(property_data)

    ###
    def getDataFrame(self, results):
        df = pd.DataFrame(columns=["city", "state", "home status", "street address", "bedrooms", "bathrooms", "sold price", "rate of price change", 
                                   "sale price", "year built", "zipcode", "county", "home type", "monthly HOA", "zestimate", 
                                   "nearby schools", "tax paid", "rate of tax change", "time on Zillow", "page view count", "favorite count",
                                   "mortgage rate", "last sold price", "url", "lot area (acres)", "sqft"])

        for dict in results:
            schools = [school.get("name") for school in dict.get("schools")]
            rating = [rate.get("rating") for rate in dict.get("schools")]
            nearby_schools = [{schools[n] : rating[n]} for n in range(0, len(schools))]
            try:
                price_sold = dict.get("priceHistory")[0].get("price")
            except:
                price_sold = None
            try:
                price_sale = dict.get("priceHistory")[1].get("price")
            except:
                price_sale = None
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
                                    dict.get("bedrooms"), dict.get("bathrooms"), price_sold, price_inc, price_sale,
                                    dict.get("yearBuilt"), dict.get("zipcode"), dict.get("county"), dict.get("homeType"), dict.get("monthlyHoaFee"),
                                    dict.get("zestimate"), nearby_schools, tax_paid, tax_inc, dict.get("timeOnZillow"), dict.get("pageViewCount"),
                                    dict.get("favoriteCount"), dict.get("mortgageRates").get("thirtyYearFixedRate"), dict.get("lastSoldPrice"),
                                    "zillow.com" + dict.get("hdpUrl"), dict.get("lotAreaValue"), dict.get("adTargets").get("sqft")]
            
        return df
        


