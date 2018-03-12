import requests
from pprint import pprint


# get function
def get(search, query):
    return requests.get(URL_ENDPOINT.format(search, query)).json()


# Define variables
URL_ENDPOINT = "https://api.iextrading.com/1.0/stock/{}/{}"


# run function
def run(stock):

    # Get stock
    quote = get(stock, "quote")
    stock_quote = {
        "companyName": quote['companyName'],
        "latestPrice": quote['latestPrice'],
        "symbol": quote['symbol'],
        "change": "{0:.2%}".format(quote['changePercent']),
        "volume":"{:,}".format(quote['latestVolume']),
        "logo": get(stock, 'logo')['url']
    }

    # Get stock related news
    news = get(stock, "news/last/5")
    stock_news = []
    for article in news:
        stock_news.append(
            {
                "headline": article['headline'],
                "url": article['url']
            }
        )

    # Get stock related company data
    company = get(stock, "company")
    company_data = {
        "website": company['website'],
        "CEO": company['CEO'],
        "description": company['description']
    }

    # Get stock key stats
    stats = get(stock, "stats")
    key_stats = {
        "latestEPS": stats['latestEPS'],
        "day5Change": "{0:.2%}".format(stats['day5ChangePercent']),
        "month3Change": "{0:.2%}".format(stats['month3ChangePercent']),
        "year1Change": "{0:.2%}".format(stats['year1ChangePercent']),
    }

    return {
        "stock_quote": stock_quote,
        "stock_news": stock_news,
        "company_data": company_data,
        "key_stats": key_stats
    }
