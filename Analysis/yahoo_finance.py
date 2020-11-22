import requests
import json
import pandas as pd
from datetime import datetime


def get_rounded_list(input_list,decimal):
    return_list = [round(num, 3) for num in input_list]
    return return_list


def get_yahoo_tickr_data(tickr,interval = '2m', range ='1d'):

    yahoo_url = 'https://query1.finance.yahoo.com/v8/finance/chart/{}' \
                '?region=US&lang=en-US&includePrePost=false&interval={}&range={}' \
                '&corsDomain=finance.yahoo.com&.tsrc=finance'.format(tickr, interval, range)

    yahoo_response = requests.get(yahoo_url)
    yahoo_response_string = yahoo_response.text
    yahoo_response_json = json.loads(yahoo_response_string)

    yahoo_tickr_data = dict()
    yahoo_tickr__meta = yahoo_response_json['chart']['result'][0]['meta']
    yahoo_tickr_data['tickr'] = tickr
    yahoo_tickr_data['timestamp_utc'] = yahoo_response_json['chart']['result'][0]['timestamp']
    yahoo_response_indicators = yahoo_response_json['chart']['result'][0]['indicators']
    yahoo_tickr_data['close'] = get_rounded_list(yahoo_response_indicators['quote'][0]['close'], 3)
    yahoo_tickr_data['open'] = get_rounded_list(yahoo_response_indicators['quote'][0]['open'], 3)
    yahoo_tickr_data['high'] = get_rounded_list(yahoo_response_indicators['quote'][0]['high'], 3)
    yahoo_tickr_data['volume'] = get_rounded_list(yahoo_response_indicators['quote'][0]['volume'], 3)
    yahoo_tickr_data['low'] = get_rounded_list(yahoo_response_indicators['quote'][0]['low'], 3)

    yahoo_tickr_df = pd.DataFrame(yahoo_tickr_data)

    yahoo_tickr_df['timestamp'] = yahoo_tickr_df['timestamp_utc'].map(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))

    return yahoo_tickr_df
