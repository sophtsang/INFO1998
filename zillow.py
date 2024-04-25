from info import *

class Zillow(object):
    ws = WebScrape()
    df = ws.scrape(url = "https://www.zillow.com/somerset-county-nj/?searchQueryState=%7B")

if __name__ == 'info':
    Zillow()