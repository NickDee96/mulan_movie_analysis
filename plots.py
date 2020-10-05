import plotly.graph_objects as go
from scipy import signal
def get_pie(df):
    vals = df.label.value_counts().sort_index().to_dict()
    labels = list(vals.keys())
    values = list(vals.values())
    fig = go.Figure(
        go.Pie(
            labels = labels,
            values = values,
            hole = .5,
            pull=[0.2, 0],
            marker_colors = ["#FF1E91","#00DCFA"]
        )
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig

def get_time_series(time_df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = time_df.date,
            y = signal.savgol_filter(time_df.score,7,2),
            fill='tozeroy',
            marker =dict(color = "#00DCFA")
        )
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig
