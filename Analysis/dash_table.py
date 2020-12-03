import dash
import dash_table
from robin_stocks import authentication
from Analysis.rh_data_extraction import *



# Login to Robin Hood
authentication.login()

#export portfolio from RH and getting data and adding some information
portfolio_df = get_RHportfolio_data()
app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in portfolio_df.columns],
    data=portfolio_df.to_dict('records'),
)

app.run_server(debug=True, port=49391)
