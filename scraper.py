import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml as lxml # type: ignore
import threading
from parsel import Selector # type: ignore

# Only run this line if you are no longer going to run the script, as it takes longer to boot up again next time.

url = "https://www.zillow.com/somerset-county-nj/?searchQueryState=%7B%22isMapVisible%22%3Afalse%2C%22mapBounds%22%3A%7B%22north%22%3A41.0363502362281%2C%22south%22%3A40.09327930935458%2C%22east%22%3A-74.23866446289063%2C%22west%22%3A-74.96101553710938%7D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22price%22%3A%7B%22max%22%3A650000%2C%22min%22%3A500000%7D%2C%22mp%22%3A%7B%22max%22%3A3461%2C%22min%22%3A2662%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A9%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A2552%2C%22regionType%22%3A4%7D%5D%2C%22pagination%22%3A%7B%7D%7D"
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

r = requests.get(url, headers = req_headers)
print(r.status_code)
selector = Selector(r.text)
data = selector.css("script#__NEXT_DATA__::text").get()
data = data.replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace(",", "").split('"')
for i in range(0, len(data)):
    links.append(data[i]) if ("homedetails" in data[i]) and not data[i] in links else None

def target(n):
    r = requests.get(links[n], headers = req_headers)
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
    results.append(property_data)

for n in range(0, len(links)):
    pool.append(threading.Thread(target = target, args = (n,)))
    pool[-1].start()

# wait for all threads in pool to finish before next line runs
for thread in pool: thread.join()

# if len(l) = 1, then user inputted link
with open("data.json", "w") as f:
    json.dump(results, f)

df = pd.DataFrame(columns=["city", "state", "home status", "street address", "bedrooms", "bathrooms", "price", "rate of price change", 
                           "year built", "zipcode", "county", "home type", "monthly HOA", "zestimate", 
                           "nearby schools", "tax paid", "rate of tax change", "time on Zillow", "page view count", "favorite count",
                           "mortgage rate", "last sold price", "url", "lot area (acres)"])

#f = open("data.json")
#data = json.load(f)
# data[0].keys() to access all keys in dict

for dict in results:
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

    df.loc[len(df.index)] = [dict.get("city"), dict.get("state"), dict.get("homeStatus"), dict.get("address").get("streetAddress"), 
                             dict.get("bedrooms"), dict.get("bathrooms"), dict.get("price"), dict.get("priceHistory")[0].get("priceChangeRate"),
                             dict.get("yearBuilt"), dict.get("zipcode"), dict.get("county"), dict.get("homeType"), dict.get("monthlyHoaFee"),
                             dict.get("zestimate"), nearby_schools, tax_paid, tax_inc, dict.get("timeOnZillow"), dict.get("pageViewCount"),
                             dict.get("favoriteCount"), dict.get("mortgageRates").get("thirtyYearFixedRate"), dict.get("lastSoldPrice"),
                             "zillow.com" + dict.get("hdpUrl"), dict.get("lotAreaValue")]

#f.close()
print(df)

