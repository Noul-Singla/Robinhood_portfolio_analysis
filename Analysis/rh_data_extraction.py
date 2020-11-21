from robin_stocks import authentication, account
import pandas as pd
import plotly.express as px
"""
Our purpose is to take that data and build a way to visualize and analyse it in more user friendly and detailed manner
"""
authentication.login()
portfolio = account.build_holdings(with_dividends=False)
for item in portfolio:
    portfolio[item]['tickr'] = item

portfolio_clean = list()
for item in portfolio:
    portfolio_clean.append(portfolio[item])

portfolio_clean[1]
portfolio_df = pd.DataFrame(portfolio_clean)

portfolio_df['quantity'] = pd.to_numeric(portfolio_df.quantity)
portfolio_df['average_buy_price'] = pd.to_numeric(portfolio_df.average_buy_price)
portfolio_df['total_buy_cost'] = round(portfolio_df['quantity']*portfolio_df['average_buy_price'],2)
total_investment = sum(portfolio_df['total_buy_cost'])
portfolio_df['percent_share'] = round((portfolio_df['total_buy_cost']/total_investment)*100, 2)

fig = px.pie(portfolio_df, values='percent_share', names='tickr', title='Investment Stocks Distribution',
             hover_name ='tickr',
             hover_data=["name", "total_buy_cost"],hole=.4,
             labels={'total_buy_cost': 'Cost ', 'name': 'Name ', 'percent_share' : 'Share (%) ', 'tickr': 'Tickr '})
fig.update_traces(textposition='inside', textinfo='label')
fig.show()



fig = px.bar(portfolio_df, y='percent_share', x='tickr', title='Investment Stocks Distribution',
             hover_name ='tickr',
             hover_data=["name", "total_buy_cost"],
             labels={'total_buy_cost': 'Cost ', 'name': 'Name', 'percent_share' : 'Share (%)', 'tickr': 'Tickr'})
fig.show()


portfolio_df.loc[1]


