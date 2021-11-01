# Installed packages
from flask import request
import yfinance as yf
import redis

# Built in packages
from datetime import date
import os
import json

r = redis.Redis.from_url(os.getenv('REDIS_URL'))

def get(symbol=None):
    
    if not symbol:
        symbol=request.get_json()['symbol']
    
    if r.exists(symbol):
        print(f'Leyendo desde cache datos: {r.memory_usage(symbol)}', flush=True)
        data = json.loads(r.get(symbol))
    else: 
        print('Consultando datos', flush=True)
        data = yf.Ticker(symbol).history(period="D1", start=str(date(2021, 2, 5)), end = str(date.today()))
        close_values = data.Close.to_list()
        labels=[str(date).replace(' 00:00:00', '') for date in data.index]
        data = dict(data=close_values, labels=labels, symbol=symbol)
        r.set(symbol, json.dumps(data)) 
        r.expire(symbol, 60*60*12)

    return data # {'symbol': symbol, 'data':close_values, 'labels':labels}     