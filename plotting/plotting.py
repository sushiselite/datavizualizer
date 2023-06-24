import plotly.express as px
import numpy as np

def get_plot(df, plot_type, column):
    if plot_type == 'histogram':
        fig = px.histogram(df, x=column)
    elif plot_type == 'bar':
        fig = px.bar(df, x=column)
    elif plot_type == 'pie':
        fig = px.pie(df, values=column)
    elif plot_type == 'scatter':
        fig = px.scatter(df, x=column, y=df.select_dtypes(include=[np.number]).columns[2])
    elif plot_type == 'line':
        fig = px.line(df, x=column, y=df.select_dtypes(include=[np.number]).columns[2])
    elif plot_type == 'boxplot':
        fig = px.box(df, y=column)
    elif plot_type == 'scatter_matrix':
        fig = px.scatter_matrix(df)
    elif plot_type == 'area':
        fig = px.area(df, x=df.index, y=column)
    elif plot_type == 'stacked_bar':
        fig = px.bar(df, x=column, y=df.select_dtypes(include=[np.number]).columns[2], 
                     color=df.select_dtypes(include=[np.number]).columns[3], barmode='stack')
    else:
        raise ValueError(f"Invalid plot type: {plot_type}")

    return fig
