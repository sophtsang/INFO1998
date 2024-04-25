import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml as lxml # type: ignore
import threading
from parsel import Selector # type: ignore

# from sklearn.model_selection import train_test_split
# from sklearn.neighbors import KNeighborsClassifier
# from parsel import Selector

# Model that predicts % difference (increase) of market price to accepted offer: predicts how much over
# the market price you have to offer to guarantee an accepted offer in n neighborhood.

# TODO 1: Do web scraping on initial market vs final sold price of houses.
#         Web scrape Zillow, Redfin, other housing websites.
#         Maybe eventually apply to Cornell housing.
#         RESOURCES: https://scrapfly.io/blog/how-to-scrape-zillow/#scraping-properties

# make region of houses user input: https://www.zillow.com/<city-state>/?searchQueryState=%7B"

# Only run this line if you are no longer going to run the script, as it takes longer to boot up again next time.

url = "https://www.zillow.com/somerset-county-nj/?searchQueryState=%7B%22isMapVisible%22%3Afalse%2C%22mapBounds%22%3A%7B%22north%22%3A41.0363502362281%2C%22south%22%3A40.09327930935458%2C%22east%22%3A-74.23866446289063%2C%22west%22%3A-74.96101553710938%7D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22price%22%3A%7B%22max%22%3A650000%2C%22min%22%3A500000%7D%2C%22mp%22%3A%7B%22max%22%3A3461%2C%22min%22%3A2662%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A9%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A2552%2C%22regionType%22%3A4%7D%5D%2C%22pagination%22%3A%7B%7D%7D"
df = pd.DataFrame(columns=["price", "beds and baths", "area", "address"])
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

print(len(links))
def target(n):
    r = requests.get(links[n], headers = req_headers)
    #print(r.status_code)
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
pool[0].join()

print(results)
# if len(l) = 1, then user inputted link
with open("data.json", "w") as f:
    json.dump(results, f)



# def target(n):
#     r = requests.get(links[n], headers = req_headers)
#     soup = BeautifulSoup(r.text, "lxml")
#     price = soup.find("span", attrs={"data-testid" : "price"}).text
#     try:
#         bed = soup.find("div", attrs = {"data-testid" : "bed-bath-sqft-facts"}).text.split(",")[0]
#     except:
#         bed = "N/A"
#     try:
#         area = soup.find("div", attrs = {"data-testid" : "bed-bath-sqft-facts"}).text.split(",")[1] 
#     except:
#         area = "N/A"
#     address = soup.find("div", attrs={"class" : "styles__AddressWrapper-fshdp-8-100-2__sc-13x5vko-0 jrtioM"}).text
#     df.loc[len(df.index)] = [price, bed, area, address] 

# for n in range(0, len(links)):
#     pool.append(threading.Thread(target = target, args = (n,)))
#     pool[-1].start()
    
# pool[0].join()
# print(df)
