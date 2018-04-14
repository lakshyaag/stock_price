import pandas as pd
import requests
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import Figure


# get function
def get(search, query):
    return requests.get(URL_ENDPOINT.format(str(search).lower(), query)).json()


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
        "volume": "{:,}".format(quote['latestVolume']),
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

    # Get chart stats and make bokeh
    chart = get(stock, "chart/5y")
    chart = pd.DataFrame(chart)
    chart = chart.set_index(pd.to_datetime(chart.date))

    chart_cds = ColumnDataSource(chart)

    p = Figure(x_axis_label="Date", y_axis_label="Price", x_axis_type="datetime", title="{} - 5Y Graph".format(stock))
    p.toolbar.active_scroll = 'auto'
    p.background_fill_color = '#8FBC8F'
    p.background_fill_alpha = 0.2

    p.line(x='date', y='close', source=chart_cds, line_width=1, color='#b71c1c')

    hover = HoverTool(mode='vline')
    hover.tooltips = [
        ('Date', '@label'),
        ('Open', '$@open{%0.2f}'),
        ('High', '$@high{%0.2f}'),
        ('Low', '$@low{%0.2f}'),
        ('Close', '$@close{%0.2f}')
    ]
    hover.formatters = {
        'open': 'printf',
        'high': 'printf',
        'low': 'printf',
        'close': 'printf'
    }
    p.add_tools(hover)

    script, div = components(p)

    return {
        "stock_quote": stock_quote,
        "stock_news": stock_news,
        "company_data": company_data,
        "key_stats": key_stats,
        "chart_script": script,
        "chart_div": div
    }
