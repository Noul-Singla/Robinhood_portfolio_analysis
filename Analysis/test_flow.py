from Analysis.rh_data_extraction import *
from robin_stocks import authentication



authentication.login()
portfolio_df = get_RHportfolio_data()
display_portfolio_pie(portfolio_df)
display_portfolio_bar(portfolio_df)
tickr_list = ['NIO','XPEV']
yahoo_data = get_tickr_data(tickr_list, range = '10d')
display_tickr_line_chart(yahoo_data)