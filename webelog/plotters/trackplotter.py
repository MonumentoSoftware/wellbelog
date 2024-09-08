import matplotlib.pyplot as plt
import matplotlib.axes
from matplotlib.axes._axes import Axes
from matplotlib.axes._base import _AxesBase
from webelog.belodlis.schemas.dlis import FrameModel


class TrackPlotter:

    def gamma_density_neutron(belo_frame: FrameModel, save: bool = False):
        """ Plots a two track plot """

        _dataframe = belo_frame.data
        title = belo_frame.logical_file_id

        fig, ax = plt.subplots(figsize=(10, 10))

        plt.suptitle(title, fontsize=20)
        ylim = (_dataframe['DEPT'].max(), _dataframe['DEPT'].min())

        # Set up the plot axes
        ax1: matplotlib.axes.Axes = plt.subplot2grid((1, 3), (0, 0), rowspan=1, colspan=1)  # noqa
        ax2: matplotlib.axes.Axes = plt.subplot2grid((1, 3), (0, 1), rowspan=1, colspan=1)  # noqa
        # Twins the y-axis for the density track with the neutron track
        ax3 = ax2.twiny()

        # As our curve scales will be detached from the top of the track,
        # this code adds the top border back in without dealing with splines
        ax7 = ax1.twiny()
        ax7.xaxis.set_visible(False)
        ax8 = ax2.twiny()
        ax8.xaxis.set_visible(False)
        ax9 = ax3.twiny()
        ax9.xaxis.set_visible(False)

        # Gamma Ray track
        ax1.plot("GR", "DEPT", data=_dataframe, color="green")
        ax1.set_xlabel("Gamma")
        ax1.xaxis.label.set_color("green")
        ax1.set_xlim(0, 200)
        ax1.set_ylabel(f"Depth  {belo_frame.index_unit}")
        ax1.tick_params(axis='x', colors="green")
        ax1.spines["top"].set_edgecolor("green")
        ax1.title.set_color('green')
        ax1.set_xticks([0, 50, 100, 150, 200])

        # Density track
        ax2.plot("RHOB", "DEPT", data=_dataframe, color="red")
        ax2.set_xlabel("Density")
        ax2.set_xlim(1.95, 2.95)
        ax2.xaxis.label.set_color("red")
        ax2.tick_params(axis='x', colors="red")
        ax2.spines["top"].set_edgecolor("red")
        ax2.set_xticks([1.95, 2.2, 2.45, 2.7, 2.95])

        # Neutron track placed ontop of density track
        ax3.plot("NPHI", "DEPT", data=_dataframe, color="blue")
        ax3.set_xlabel('Neutron')
        ax3.xaxis.label.set_color("blue")
        ax3.set_xlim(0.45, -0.15)
        ax3.set_ylim(ylim)
        ax3.tick_params(axis='x', colors="blue")
        ax3.spines["top"].set_position(("axes", 1.08))
        ax3.spines["top"].set_visible(True)
        ax3.spines["top"].set_edgecolor("blue")
        ax3.set_xticks([0.45, 0.3, 0.15, 0, -0.15])

        # Common functions for setting up the plot can be extracted into
        # a for loop. This saves repeating code.
        for ax in [ax1, ax2, ax3]:
            ax.set_ylim(ylim)
            ax.grid(which='major', color='lightgrey', linestyle='-')
            ax.xaxis.set_ticks_position("top")
            ax.xaxis.set_label_position("top")

        plt.tight_layout()
        if save:
            plt.savefig(f'{title}.png')
            plt.close(fig)
            return
