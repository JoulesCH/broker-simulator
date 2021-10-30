# Installed packages
from flask import render_template, request, redirect, make_response
import yfinance as yf
from datetime import date

def get(symbol=None):
    if not symbol:
        symbol=request.get_json()['symbol']
    data = yf.Ticker(symbol).history(period="D1", start=str(date(2021, 2, 5)), end = str(date.today()))
    close_values = data.Close.to_list()
    labels=[str(date).replace(' 00:00:00', '') for date in data.index]
    return {'symbol': symbol, 'data':close_values, 'labels':labels}     