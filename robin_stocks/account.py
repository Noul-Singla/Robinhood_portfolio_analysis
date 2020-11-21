"""Contains functions for getting information related to the user account."""

from robin_stocks import helper as helper, profiles as profiles, stocks as stocks, urls as urls


@helper.login_required
def get_open_stock_positions(info=None):
    """Returns a list of stocks that are currently held.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: [list] Returns a list of dictionaries of key/value pairs for each ticker. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.
    :Dictionary Keys: * url
                      * instrument
                      * account
                      * account_number
                      * average_buy_price
                      * pending_average_buy_price
                      * quantity
                      * intraday_average_buy_price
                      * intraday_quantity
                      * shares_held_for_buys
                      * shares_held_for_sells
                      * shares_held_for_stock_grants
                      * shares_held_for_options_collateral
                      * shares_held_for_options_events
                      * shares_pending_from_options_events
                      * updated_at
                      * created_at

    """
    url = urls.positions()
    payload = {'nonzero': 'true'}
    data = helper.request_get(url, 'pagination', payload)

    return(helper.filter(data, info))

@helper.login_required
def get_all_watchlists(info=None):
    """Returns a list of all watchlists that have been created. Everyone has a 'My First List' watchlist.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of the watchlists. Keywords are 'url', 'user', and 'name'.

    """
    url = urls.watchlists()
    data = helper.request_get(url, 'result')
    return(helper.filter(data, info))


@helper.login_required
def get_watchlist_by_name(name="My First List", info=None):
    """Returns a list of information related to the stocks in a single watchlist.

    :param name: The name of the watchlist to get data from.
    :type name: Optional[str]
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries that contain the instrument urls and a url that references itself.

    """

    #Get id of requested watchlist
    all_watchlists = get_all_watchlists()
    watchlist_id = ''
    for wl in all_watchlists['results']:
        if wl['display_name'] == name:
            watchlist_id = wl['id']

    url = urls.watchlists(name)
    data = helper.request_get(url, 'list_id', {'list_id':watchlist_id})
    return(helper.filter(data, info))


@helper.login_required
def build_holdings(with_dividends=False):
    """Builds a dictionary of important information regarding the stocks and positions owned by the user.

    :param with_dividends: True if you want to include divident information.
    :type with_dividends: bool
    :returns: Returns a dictionary where the keys are the stock tickers and the value is another dictionary \
    that has the stock price, quantity held, equity, percent change, equity change, type, name, id, pe ratio, \
    percentage of portfolio, and average buy price.

    """
    positions_data = get_open_stock_positions()
    portfolios_data = profiles.load_portfolio_profile()
    accounts_data = profiles.load_account_profile()

    # user wants dividend information in their holdings
    if with_dividends is True:
        dividend_data = get_dividends()

    if not positions_data or not portfolios_data or not accounts_data:
        return({})

    if portfolios_data['extended_hours_equity'] is not None:
        total_equity = max(float(portfolios_data['equity']), float(
            portfolios_data['extended_hours_equity']))
    else:
        total_equity = float(portfolios_data['equity'])

    cash = "{0:.2f}".format(
        float(accounts_data['cash']) + float(accounts_data['uncleared_deposits']))

    holdings = {}
    for item in positions_data:
        # It is possible for positions_data to be [None]
        if not item:
            continue

        try:
            instrument_data = stocks.get_instrument_by_url(item['instrument'])
            symbol = instrument_data['symbol']
            fundamental_data = stocks.get_fundamentals(symbol)[0]

            price = stocks.get_latest_price(instrument_data['symbol'])[0]
            quantity = item['quantity']
            equity = float(item['quantity']) * float(price)
            equity_change = (float(quantity) * float(price)) - \
                (float(quantity) * float(item['average_buy_price']))
            percentage = float(item['quantity']) * float(price) * \
                100 / (float(total_equity) - float(cash))
            if (float(item['average_buy_price']) == 0.0):
                percent_change = 0.0
            else:
                percent_change = (float(
                    price) - float(item['average_buy_price'])) * 100 / float(item['average_buy_price'])

            holdings[symbol] = ({'price': price})
            holdings[symbol].update({'quantity': quantity})
            holdings[symbol].update(
                {'average_buy_price': item['average_buy_price']})
            holdings[symbol].update({'equity': "{0:.2f}".format(equity)})
            holdings[symbol].update(
                {'percent_change': "{0:.2f}".format(percent_change)})
            holdings[symbol].update(
                {'equity_change': "{0:2f}".format(equity_change)})
            holdings[symbol].update({'type': instrument_data['type']})
            holdings[symbol].update(
                {'name': stocks.get_name_by_symbol(symbol)})
            holdings[symbol].update({'id': instrument_data['id']})
            holdings[symbol].update({'pe_ratio': fundamental_data['pe_ratio']})
            holdings[symbol].update(
                {'percentage': "{0:.2f}".format(percentage)})

            if with_dividends is True:
                # dividend_data was retrieved earlier
                holdings[symbol].update(get_dividends_by_instrument(
                    item['instrument'], dividend_data))

        except:
            pass

    return(holdings)


@helper.login_required
def build_user_profile():
    """Builds a dictionary of important information regarding the user account.

    :returns: Returns a dictionary that has total equity, extended hours equity, cash, and divendend total.

    """
    user = {}

    portfolios_data = profiles.load_portfolio_profile()
    accounts_data = profiles.load_account_profile()

    if portfolios_data:
        user['equity'] = portfolios_data['equity']
        user['extended_hours_equity'] = portfolios_data['extended_hours_equity']

    if accounts_data:
        cash = "{0:.2f}".format(
            float(accounts_data['cash']) + float(accounts_data['uncleared_deposits']))
        user['cash'] = cash

    user['dividend_total'] = get_total_dividends()

    return(user)

