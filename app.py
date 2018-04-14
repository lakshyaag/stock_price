from flask import Flask, render_template, request

import stock as stock

app = Flask(__name__)
app.debug = False


@app.route('/')
def form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def submit_data():
    stock_n = request.form['stock_code']

    data = stock.run(stock_n)

    stock_quote = data['stock_quote']
    stock_news = data['stock_news']
    company_data = data['company_data']
    key_stats = data['key_stats']

    return render_template('stock.html', companyName=stock_quote['companyName'], latestPrice=stock_quote['latestPrice'],
                           symbol=stock_quote['symbol'], change=stock_quote['change'], volume=stock_quote['volume'],
                           logo=stock_quote['logo'], news=stock_news, website=company_data['website'],
                           CEO=company_data['CEO'], description=company_data['description'],
                           latestEPS=key_stats['latestEPS'], day5Change=key_stats['day5Change'],
                           month3Change=key_stats['month3Change'], year1Change=key_stats['year1Change'],
                           chart_script=data['chart_script'], chart_div=data['chart_div'])


@app.errorhandler(500)
def error():
    return render_template('error.html')


if __name__ == "__main__":
    app.run()
