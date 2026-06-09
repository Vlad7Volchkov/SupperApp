import plotly.graph_objects as go

def make_exchange_rate_graph(exchange_rate_data):
    fig = go.Figure()
    for currency_name, exchange_rate in exchange_rate_data.items():
        x_data = [row['CursDate'] for row in exchange_rate]
        y_data = [row['Vcurs'] for row in exchange_rate]
        fig.add_scatter(
            x=x_data,
            y=y_data,
            name=currency_name,)
    fig.update_layout(autosize=True)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')