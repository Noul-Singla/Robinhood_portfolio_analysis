from Analysis.rh_data_extraction import *
from robin_stocks import authentication

# Login to Robin Hood
authentication.login()

#export portfolio from RH and getting data and adding some information
portfolio_df = get_RHportfolio_data()
display_portfolio_pie(portfolio_df, 'percent_share')
display_portfolio_pie(portfolio_df, 'percent_change')

data = get_tickr_data(portfolio_df.tickr, interval='1d',range='2d')
data.sort_values(['tickr', 'timestamp'], inplace=True)
data['diffs'] = data.groupby('tickr')['close'].diff()
display_tickr_bar_chart(data, y_axis='diffs')
display_tickr_pie_chart(data, distribution_on='diffs')

display_portfolio_bar(portfolio_df)
portfolio_df.tickr
yahoo_data = get_tickr_data(portfolio_df.tickr, range='2d')
display_tickr_line_chart(yahoo_data)



# Getting tickr data from yahoo finance
tickr_list = ['NIO', 'XPEV', 'LI']
yahoo_data = get_tickr_data(tickr_list, range='10d')
display_tickr_line_chart(yahoo_data)


watchlist_list = get_watchilists()
#import is just for randomness testing, wont be needed in code
import random
watchlist_name = random.choice(watchlist_list)
watchlist_data = get_watchlist_data('EV')
yahoo_data = get_tickr_data(watchlist_data.symbol, range='2d')
display_tickr_line_chart(yahoo_data)
