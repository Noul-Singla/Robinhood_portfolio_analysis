import requests
import json

tickr = 'AAPL'
interval ='2m'
range = '1d'
yahoo_url = 'https://query1.finance.yahoo.com/v8/finance/chart/AAPL?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'
yahoo_response = requests.get(yahoo_url)
yahoo_response_string = yahoo_response.text
yahoo_response_json = json.loads(yahoo_response_string)
yahoo_response_json['chart']['result'][0].keys()
yahoo_response_meta = yahoo_response_json['chart']['result'][0]['meta']
yahoo_response_timestamp = yahoo_response_json['chart']['result'][0]['timestamp']
yahoo_response_indicators = yahoo_response_json['chart']['result'][0]['indicators']
yahoo_response_indicators['quote'][0].keys()
yahoo_response_close = yahoo_response_indicators['quote'][0]['close']
yahoo_response_open = yahoo_response_indicators['quote'][0]['open']
yahoo_response_high = yahoo_response_indicators['quote'][0]['high']
yahoo_response_volume = yahoo_response_indicators['quote'][0]['volume']
yahoo_response_low = yahoo_response_indicators['quote'][0]['low']

yahoo_response_close[1]
yahoo_response_open[1]
yahoo_response_high[1]
yahoo_response_low[2]

