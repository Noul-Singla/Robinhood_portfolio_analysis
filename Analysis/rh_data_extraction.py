from Analysis.yahoo_finance import get_yahoo_tickr_data
from robin_stocks import account
import pandas as pd
import plotly.express as px

"""
Our purpose is to take that data and build a way to visualize and analyse it in more user friendly and detailed manner
"""
def get_RHportfolio_data():
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

    return portfolio_df

def display_portfolio_pie(portfolio_df):
    fig = px.pie(portfolio_df, values='percent_share', names='tickr', title='Investment Stocks Distribution',
                 hover_name ='tickr',
                 hover_data=["name", "total_buy_cost"],hole=.4,
                 labels={'total_buy_cost': 'Cost ', 'name': 'Name ', 'percent_share' : 'Share (%) ', 'tickr': 'Tickr '})
    fig.update_traces(textposition='inside', textinfo='label')
    fig.show()


def display_portfolio_bar(portfolio_df):
    fig = px.bar(portfolio_df, y='percent_share', x='tickr', title='Investment Stocks Distribution',
                 hover_name ='tickr',
                 hover_data=["name", "total_buy_cost"],
                 labels={'total_buy_cost': 'Cost ', 'name': 'Name', 'percent_share' : 'Share (%)', 'tickr': 'Tickr'})
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    fig.show()


def display_tickr_line_chart(input_df):
    y_axis = "close"
    fig = px.line(input_df, x="timestamp", y=y_axis, title='Data for stocks', color ='tickr')
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    fig.show()


def get_tickr_data(tickr_list, interval = '2m', range = '1d'):
    yahoo_data = pd.DataFrame()
    for tickr in tickr_list:
        yahoo_data = yahoo_data.append(get_yahoo_tickr_data(tickr, interval, range))
    return yahoo_data

#def if __name__ == '__main__':
