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
    chart_cds_df = get(stock, 'chart/1m')
    chart = pd.DataFrame(chart)
    chart = chart.set_index(pd.to_datetime(chart.date))

    chart_cds = ColumnDataSource(chart)

    p = Figure(x_axis_label="Date", y_axis_label="Price", x_axis_type="datetime", title="{} - 5Y Graph".format(stock),
               sizing_mode='scale_width')
    # p.background_fill_color = '#8FBC8F'
    # p.background_fill_alpha = 0.2
    p.grid.grid_line_alpha = 0.3

    p.line(x='date', y='close', source=chart_cds, line_width=1, color='#F2583E')

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

    cdl = Figure(x_axis_label="Date", y_axis_label="Price", x_axis_type="datetime",
                 title="{} - Candlestick".format(stock), sizing_mode='scale_width')

    chart_cds_df = pd.DataFrame(chart_cds_df)
    chart_cds_df = chart_cds_df.set_index(pd.to_datetime(chart_cds_df.date))

    inc = chart_cds_df.close > chart_cds_df.open
    dec = chart_cds_df.open > chart_cds_df.close
    w = 12 * 60 * 60 * 1000

    cdl.segment(chart_cds_df.index, chart_cds_df.high, chart_cds_df.index, chart_cds_df.low, color='black')
    cdl.vbar(chart_cds_df.index[inc], w, chart_cds_df.open[inc], chart_cds_df.close[inc], fill_color='#D5E1DD',
             line_color='black')
    cdl.vbar(chart_cds_df.index[dec], w, chart_cds_df.open[dec], chart_cds_df.close[dec], fill_color='#F2583E',
             line_color='black')

    cdl.grid.grid_line_alpha = 0.3

    cdl_s, cdl_div = components(cdl)

    script, div = components(p)

    return {
        "stock_quote": stock_quote,
        "stock_news": stock_news,
        "company_data": company_data,
        "key_stats": key_stats,
        "chart_script": script,
        "chart_div": div,
        "s": cdl_s,
        "d": cdl_div
    }
