import requests
import json
import pandas as pd
from datetime import datetime

tickr = 'AAPL'
interval ='2m'
range = '1d'
yahoo_url = 'https://query1.finance.yahoo.com/v8/finance/chart/{}' \
            '?region=US&lang=en-US&includePrePost=false&interval={}&range={}' \
            '&corsDomain=finance.yahoo.com&.tsrc=finance'.format(tickr, interval, range)

yahoo_response = requests.get(yahoo_url)
yahoo_response_string = yahoo_response.text
yahoo_response_json = json.loads(yahoo_response_string)

yahoo_tickr_data = dict()
yahoo_tickr__meta = yahoo_response_json['chart']['result'][0]['meta']
yahoo_tickr_data['timestamp_utc'] = yahoo_response_json['chart']['result'][0]['timestamp']
yahoo_response_indicators = yahoo_response_json['chart']['result'][0]['indicators']
yahoo_tickr_data['close'] = yahoo_response_indicators['quote'][0]['close']
yahoo_tickr_data['open'] = yahoo_response_indicators['quote'][0]['open']
yahoo_tickr_data['high'] = yahoo_response_indicators['quote'][0]['high']
yahoo_tickr_data['volume'] = yahoo_response_indicators['quote'][0]['volume']
yahoo_tickr_data['low'] = yahoo_response_indicators['quote'][0]['low']

yahoo_tickr_df = pd.DataFrame(yahoo_tickr_data)

yahoo_tickr_df['timestamp'] = yahoo_tickr_df['timestamp_utc'].map(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))

yahoo_tickr_df
