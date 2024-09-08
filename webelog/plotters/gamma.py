import matplotlib.pyplot as plt
from pandas import DataFrame


class GammaPlot:

    @staticmethod
    def singleGamma(df_: DataFrame, title: str = None, save=False):
        """
        Plotter for a single Gamma plot.
        """

        fig, ax = plt.subplots(figsize=(10, 15), dpi=300)

        plt.title(title)
        ax1 = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)
        ylim = (df_['DEPT'].max(), df_['DEPT'].min())
        ax1.plot('GR', 'DEPT', data=df_)  # Call the data from the df dataframe
        ax1.set_xlabel("Gamma")  # Assign a track title
        ax1.set_xlim(0, 200)  # Change the limits for the curve being plotted
        ax1.set_ylim(ylim)  # Set the depth range
        ax1.grid()  # Display the grid
        if save:
            plt.savefig(f'{title}.png')
            plt.close(fig)
            return

    @staticmethod
    def Rgamma(df_: DataFrame, title: str = None, save=False):
        """
        Plotter for RGR plots.
        """

        fig = plt.subplots(figsize=(10, 15), dpi=300)

        plt.title(title)
        ax1 = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)
        ylim = (df_['DEPT'].max(), df_['DEPT'].min())
        # Call the data from the df dataframe
        ax1.plot('RGR', 'DEPT', data=df_)
        ax1.set_xlabel("Gamma")  # Assign a track title
        ax1.set_xlim(0, 200)  # Change the limits for the curve being plotted
        ax1.set_ylim(ylim)  # Set the depth range
        ax1.grid()  # Display the grid
        if save:
            plt.savefig(f'{title}.png')
