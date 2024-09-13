import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame


def plot_all_curves(data: DataFrame, depth_column: str = 'DEPT', figsize=(12, 8), title='Geological Curves') -> Figure:
    """
    Function to create subplots for each column with depth as index.

    Parameters:
        data (pd.DataFrame): DataFrame containing the data.
        depth_column (str): The name of the depth column.
        figsize (tuple): Size of the figure.
        title (str): Title of the plot.
    """
    # Get the list of columns to plot (exclude the depth column)
    columns = [col for col in data.columns if col != depth_column]
    num_plots = len(columns)
    # Create subplots
    fig, axes = plt.subplots(nrows=1, ncols=num_plots, figsize=figsize, sharey=True)
    axes: list[Axes]

    # TODO Find a a better way to deal with color cycling
    # Colors for the plots (cycle through colors if there are more columns than colors)
    colors = ['green', 'red', 'blue', 'black', 'purple']

    for i, col in enumerate(columns):
        axes[i].plot(data[col], data[depth_column], label=col, color=colors[i % len(colors)])
        axes[i].set_xlabel(col)
        axes[i].grid(True)

    # Set shared y-axis label and invert y-axis
    axes[0].set_ylabel(depth_column)
    axes[0].invert_yaxis()  # Invert the y-axis to have depth increase downwards

    # Set the title
    fig.suptitle(title)
    # Adjust layout to make room for the title
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
    return fig
