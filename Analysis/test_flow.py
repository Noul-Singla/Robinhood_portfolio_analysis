from Analysis.rh_data_extraction import *
from robin_stocks import authentication

# Login to Robin Hood
authentication.login()

#export portfolio from RH and getting data and adding some information
portfolio_df = get_RHportfolio_data()
display_portfolio_pie(portfolio_df)
display_portfolio_bar(portfolio_df)

# Getting tickr data from yahoo finance
tickr_list = ['NIO', 'XPEV', 'LI']
yahoo_data = get_tickr_data(tickr_list, range='10d')
display_tickr_line_chart(yahoo_data)


watchlist_list = get_watchilists()
#import is just for randomness testing, wont be needed in code
import random
watchlist_name = random.choice(watchlist_list)
watchlist_data = get_watchlist_data(watchlist_name)
yahoo_data = get_tickr_data(watchlist_data.symbol[0:5], range='30d')
display_tickr_line_chart(yahoo_data)
