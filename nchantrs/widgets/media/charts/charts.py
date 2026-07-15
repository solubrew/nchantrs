# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid: 'e49e63fd-aad8-4ae3-b176-8ca67718fac6'
    name:
    description: >
        leverage visualizer to generate charts to displayed
        through test_nchantrs or warlock via an integrated test_nchantrs browser
    expirary: <[expiration]>
    version: <[version]>
    authority: document|this
    security: sec|lvl2
    <(WT)>: -32
"""

# -*- coding: utf-8 -*-
# ===============================Core Modules====================================||
from os.path import abspath, dirname, join
import datetime as dt

import logging

logger = logging.getLogger(__name__)
# ===============================================================================||
import numpy as np
import mplfinance as mpf
import seaborn as sns
import matplotlib as mat
import plotly.graph_objects as go
import matplotlib.pyplot as plt

mat.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.sankey import Sankey
from wordcloud import WordCloud
from pandas import date_range, DataFrame

# need other plotting options for non pyQT-guis and cmdline style programs
# ===============================================================================||
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidgetMixin
from kahndor import kahndor

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
# ===============================================================================||
pxcfg = join(abspath(here), "_data_", "charts.yaml")


class NchantdChart(NchantdWidgetMixin, FigureCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, parent=None, cfg={}):
        """ """
        width, height, dpi = 600, 4, 100
        self.config = kahndor.Instruct(pxcfg).select("NchantdChart")

        self.set_theme()
        fig = self.config.dikt.get("figure", None)
        self.fig = fig
        if self.fig is None:
            self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.parent = parent
        if self.parent is not None:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.axes = self.fig.add_subplot(111)
        self.chart_type = self.config.dikt.get("chart_type", None)

        # try:
        #     self.axes.hold(False)  # We want the axes cleared every time plot() is called
        # except:
        #     pass
        # sns.set_theme(style="darkgrid")
        # plt.style.use("dark_background")
        # Apply Seaborn themes globally

        FigureCanvas.setSizePolicy(self, pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Expanding)
        # FigureCanvas.updateGeometry(self)
        # self.setParent(parent)
        # self.plot_sample_data()
        self.data_series = None
        self.time_data = None
        self.time_series_values = None

    def initModel(self):
        """"""
        super().initModel()
        self.axes.clear()
        self.data_series = self.config.dikt.get("data_series", None)
        if self.data_series is None:
            self.load_sample_data()
        return self

    def initView(self):
        """"""
        super().initView()
        self.plot_chart()
        # self.plot_sample_data()
        # self.compute_initial_figure()
        # self.update_figure()
        return self

    def initWidget(self):
        """ """
        self.initModel()
        self.initView()
        return self

    def clear_axes(self):
        """Clear the current axes to prepare for a new chart."""
        self.axes.clear()

    def load_sample_data(self):
        """"""
        self.x = np.linspace(0, 10, 100)
        self.y1 = np.sin(self.x)
        self.y2 = np.cos(self.x)

    # def plot_sample_data(self):
    #     # Generate example data
    #     x = np.linspace(0, 10, 100)
    #     y1 = np.sin(x)
    #     y2 = np.cos(x)
    #
    #     # Create line plots
    #     self.axes.plot(x, y1, label="Sine Wave", linewidth=2.5)
    #     self.axes.plot(x, y2, label="Cosine Wave", linewidth=2.5)
    #
    #     # Add titles, legend, and labels
    #     self.axes.set_title("Seaborn Themed Chart", size=16)
    #     self.axes.set_xlabel("X-axis", size=12)
    #     self.axes.set_ylabel("Y-axis", size=12)
    #     self.axes.legend()
    #
    #     # Enhance tick labels
    #     self.axes.tick_params(axis="both", which="major", labelsize=10)

    def plot_chart(self):
        """"""
        logma.info(f"Chart Type{self.chart_type}")
        if self.chart_type is None:
            self.chart_type = "line"
        logma.info(f"Chart Type{self.chart_type}")
        chart_type = self.chart_type.lower()
        match chart_type:
            case "area":
                self.plot_area_chart()
            case "area3d":
                self.plot_area_chart_3D()
            case "bar":
                self.plot_bar_chart()
            case "bar3d":
                self.plot_bar_chart_3D()
            case "barstacked":
                self.plot_bar_chart_stacked()
            case "bubble":
                self.plot_bubble_chart()
            case "candlestick":
                self.plot_candlestick_chart()
            case "column":
                self.plot_column_chart()
            case "columnstacked":
                self.plot_column_chart_stacked()
            case "doughnut":
                self.plot_doughnut_chart()
            case "funnel":
                self.plot_funnel_chart()
            case "gantt":
                self.plot_gantt_chart()
            case "heatmap":
                self.plot_heatmap_chart()
            case "histogram":
                self.plot_histogram_chart()
            case "line":
                self.plot_line_chart()
            case "pie":
                self.plot_pie_chart()
            case "pie3d":
                self.plot_pie_chart()
            case "radar":
                self.plot_radar_chart()
            case "sankey":
                self.plot_sankey_chart()
            case "scatter":
                self.plot_scatter_chart()
            case "scatter3d":
                self.plot_scatter_chart_3D()
            case "surface":
                self.plot_surface_chart()
            case "timeseries":
                self.plot_time_series_chart()
            case "treemap":
                self.plot_treemap_chart()
            case "violin":
                self.plot_violin_chart()
            case "wordcloud":
                self.plot_wordcloud()
        return self

    def plot_area_chart(self):
        """Plot an area chart."""
        self.clear_axes()
        self.axes.fill_between(self.x, self.y1, color="blue", alpha=0.4, label="Sine Area")
        self.axes.fill_between(self.x, self.y2, color="orange", alpha=0.4, label="Cosine Area")
        self.axes.set_title("Area Chart")
        self.axes.set_xlabel("X-axis")
        self.axes.set_ylabel("Y-axis")
        self.axes.legend()
        self.draw()

    def plot_area_chart_3D(self):
        """Generate and plot a 3D area chart."""
        # TODO: this feature is not working the entire graph widget disappears when Area3D is selected in the chart type dropdown
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection="3d")

        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        z = np.zeros_like(x)

        dz = y
        ax.plot_trisurf(x, z, dz, cmap="coolwarm")
        ax.set_title("3D Area Chart")
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Fixed Z")
        ax.set_zlabel("Y Axis")

        self.draw()

    def plot_bar_chart(self):
        """Plot a bar chart."""
        self.clear_axes()
        categories = ["A", "B", "C", "D", "E"]
        values = [5, 8, 7, 6, 9]
        self.axes.bar(categories, values, color="teal", alpha=0.8)
        self.axes.set_title("Bar Chart")
        self.axes.set_xlabel("Categories")
        self.axes.set_ylabel("Values")
        self.draw()

    def plot_bar_chart_3D(self):
        """Generate and plot a 3D bar chart."""
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection="3d")

        xpos = np.arange(5)
        ypos = np.arange(5)
        xpos, ypos = np.meshgrid(xpos, ypos)
        xpos = xpos.flatten()
        ypos = ypos.flatten()
        zpos = np.zeros_like(xpos)
        dx = dy = 0.5
        dz = np.random.randint(1, 10, size=len(xpos))

        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color="lightblue", edgecolor="black")
        ax.set_title("3D Bar Chart")
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.set_zlabel("Height")

        self.draw()

    def plot_bar_chart_stacked(self):
        """Generate and plot a stacked bar chart."""
        # TODO: this feature is not working the entire graph widget disappears when BarStacked is selected in the chart type dropdown
        # Clear previous plots
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        # Example data: Groups and their components
        categories = ["Group 1", "Group 2", "Group 3"]
        subgroups = ["Component A", "Component B", "Component C"]

        # Example dataset (rows: categories, columns: subgroups)
        data = np.array(
            [
                [5, 3, 2],  # Data for Group 1
                [6, 4, 3],  # Data for Group 2
                [4, 2, 4],  # Data for Group 3
            ]
        )

        # Calculate cumulative heights for stacking
        bar_positions = np.arange(len(categories))  # Positions of the groups
        cumulative_heights = np.zeros(len(categories))  # Initialize stacking at 0

        # Colors for different components
        colors = ["lightblue", "orange", "green"]

        # Plot each subgroup as a portion of the stacked bar
        for i, (color, subgroup) in enumerate(zip(colors, subgroups)):
            ax.bar(
                bar_positions,
                data[:, i],  # Data for this component
                bottom=cumulative_heights,  # Start stacking from the current height
                color=color,
                label=subgroup,
            )
            cumulative_heights += data[:, i]  # Update the cumulative heights

        # Add title, labels, and legend
        ax.set_title("Stacked Bar Chart")
        ax.set_xticks(bar_positions)
        ax.set_xticklabels(categories)
        ax.set_ylabel("Values")
        ax.set_xlabel("Categories")
        ax.legend(title="Components")

        # Add grid for better readability
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        # Ensure a clear layout
        self.fig.tight_layout()

        # Redraw the chart
        self.draw()

    def plot_box_and_whisker(self):
        """Generate and plot a box-and-whisker plot."""
        # Clear any previous plots
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        # Example data to be visualized
        data = [
            [7, 8, 7.5, 9.0, 8.2, 7.8, 8.6],  # Group 1
            [6, 6.2, 6.8, 5.9, 6.5, 6.3, 6.7],  # Group 2
            [8, 8.3, 7.8, 8.4, 8.1, 8.7, 8.2],  # Group 3
            [9, 9.1, 9.3, 9.2, 9.0, 9.5, 9.4],  # Group 4
        ]

        categories = ["Group 1", "Group 2", "Group 3", "Group 4"]  # Labels for groups

        # Create the box-and-whisker plot
        box = ax.boxplot(
            data,
            vert=True,  # Vertical box plot orientation
            patch_artist=True,  # Fill with color
            labels=categories,  # Add category labels to the X-axis
            notch=True,  # Add notches to indicate confidence intervals for the median
        )

        # Customize the appearance of the boxes
        colors = ["lightblue", "orange", "green", "purple"]
        for patch, color in zip(box["boxes"], colors):
            patch.set_facecolor(color)  # Set the fill color

        # Customize additional plot elements
        ax.set_title("Box-and-Whisker Plot")
        ax.set_ylabel("Values")
        ax.grid(axis="y", linestyle="--", alpha=0.7)  # Add a grid for better readability

        # Redraw the chart
        self.draw()

    def plot_bubble_chart(self):
        """Plot a bubble chart."""
        self.clear_axes()
        bubble_sizes = np.random.uniform(20, 200, size=len(self.x))
        self.axes.scatter(self.x, self.y1, s=bubble_sizes, alpha=0.4, c=self.y2, cmap="viridis")
        self.axes.set_title("Bubble Chart")
        self.axes.set_xlabel("X-axis")
        self.axes.set_ylabel("Y-axis")
        self.draw()

    def plot_candlestick_chart(self):
        """Generate and plot a candlestick chart."""
        # Generate example OHLC data
        dates = date_range(dt.datetime(2023, 1, 1), periods=30)
        data = {
            "Open": np.random.uniform(100, 200, size=len(dates)),
            "High": np.random.uniform(200, 300, size=len(dates)),
            "Low": np.random.uniform(50, 100, size=len(dates)),
            "Close": np.random.uniform(100, 250, size=len(dates)),
            "Volume": np.random.randint(1000, 10000, size=len(dates)),
        }
        ohlc_data = DataFrame(data, index=dates)

        # Clear previous plots
        self.axes.clear()

        # Use mplfinance to plot the candlestick chart
        mpf.plot(
            ohlc_data,
            type="candle",
            ax=self.axes,
            style="yahoo",  # Preset styles like 'yahoo', 'classic', or define your own
            # volume=True,  # Enable volume subplot
            # title="Candlestick Chart",
            ylabel="Price (USD)",
            ylabel_lower="Volume",
        )

        # Update the canvas to show the new chart
        self.draw()

    def plot_column_chart(self):
        """Generate and plot a column chart."""
        # Generate example data
        categories = ["Category A", "Category B", "Category C", "Category D"]
        values = [25, 40, 35, 50]  # Example values
        # Clear previous plots
        self.axes.clear()
        # Plot the column chart
        self.axes.bar(categories, values, color="skyblue", edgecolor="black")
        # Add titles and labels
        self.axes.set_title("Column Chart", fontsize=16)
        self.axes.set_xlabel("Categories", fontsize=12)
        self.axes.set_ylabel("Values", fontsize=12)
        self.axes.grid(axis="y", linestyle="--", alpha=0.7)
        # Add text annotations for values above bars
        for i, value in enumerate(values):
            self.axes.text(
                i,
                value + 1,  # Position above the bar
                f"{value}",
                ha="center",
                va="bottom",
                fontsize=10,
            )
        # Update the canvas to display the new chart
        self.draw()

    def plot_column_chart_3D(self):
        """Generate and plot a 3D column chart."""
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection="3d")
        xpos = np.arange(5)
        ypos = np.zeros_like(xpos)
        zpos = np.zeros_like(xpos)
        dx = dy = 0.4
        dz = np.random.randint(1, 10, size=len(xpos))
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color="green", edgecolor="black")
        ax.set_title("3D Column Chart")
        ax.set_xlabel("Categories")
        ax.set_ylabel("Fixed Y")
        ax.set_zlabel("Value")
        self.draw()

    def plot_column_chart_stacked(self):
        """Generate and plot a stacked column chart."""
        # Clear any previous plots
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        # Example data
        categories = ["Group 1", "Group 2", "Group 3", "Group 4"]
        subgroups = ["Segment A", "Segment B", "Segment C"]
        data = np.array(
            [
                [4, 3, 2],  # Values for Group 1
                [6, 5, 3],  # Values for Group 2
                [3, 2, 6],  # Values for Group 3
                [5, 4, 4],  # Values for Group 4
            ]
        )

        # Column positions on the x-axis
        bar_positions = np.arange(len(categories))

        # Accumulate heights for stacking
        cumulative_heights = np.zeros(len(categories))

        # Define colors for each segment
        colors = ["skyblue", "orange", "green"]

        # Create stacked columns
        for i, (color, subgroup) in enumerate(zip(colors, subgroups)):
            ax.bar(
                bar_positions,
                height=data[:, i],  # Heights for this segment
                bottom=cumulative_heights,  # Start stacking from the current heights
                width=0.7,  # Column width
                color=color,
                label=subgroup,
            )
            # Update the cumulative heights for each column
            cumulative_heights += data[:, i]

        # Set plot elements
        ax.set_title("Stacked Column Chart")
        ax.set_xticks(bar_positions)
        ax.set_xticklabels(categories)
        ax.set_ylabel("Values")
        ax.set_xlabel("Groups")
        ax.legend(title="Segments")

        # Add grid for better readability
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        # Adjust layout to fit all elements properly
        self.fig.tight_layout()

        # Redraw the canvas
        self.draw()

    def plot_doughnut_chart(self):
        """Generate and plot a doughnut chart."""
        # Example data for the doughnut chart
        categories = ["Category A", "Category B", "Category C", "Category D"]
        values = [25, 35, 20, 20]  # Percentages

        # Clear previous plots
        self.axes.clear()

        # Create a pie chart (with doughnut effect)
        wedges, texts, autotexts = self.axes.pie(
            values,
            labels=categories,
            autopct="%1.1f%%",  # Show percentages inside the segments
            startangle=90,  # Start the pie chart at 90 degrees
            pctdistance=0.85,  # Position percentage labels closer to the center
            textprops=dict(color="black", fontsize=10),
        )

        # Add the "hole" in the middle of the chart to create the doughnut
        centre_circle = plt.Circle((0, 0), 0.70, color="white", fc="white", linewidth=0)
        self.axes.add_artist(centre_circle)

        # Ensure the chart is displayed as a circle
        self.axes.axis("equal")
        self.axes.set_title("Doughnut Chart", fontsize=16)

        # Update the canvas to display the new chart
        self.draw()

    def plot_doughnut_chart_3D(self):
        """Generate and plot a 3D doughnut chart (mocked with pie visualization)."""
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection="3d")

        categories = ["A", "B", "C", "D"]
        values = [40, 30, 20, 10]
        cumulative_values = np.cumsum(values)
        fractional = cumulative_values / sum(values)

        for i, val in enumerate(values):
            ax.bar3d(
                [i],
                [0],
                [0],
                0.5,
                1,
                val,
                color=plt.cm.Set3(i / len(values)),
                alpha=0.8,
            )

        ax.set_title("3D Doughnut Chart (Mocked)")
        ax.set_ylabel("Y Axis")
        ax.set_zlabel("Values")

        self.draw()

    def plot_funnel_chart(self):
        """Generate and plot a funnel chart."""
        # Example funnel data
        stages = ["Awareness", "Interest", "Consideration", "Evaluation", "Purchase"]
        values = [2000, 1500, 1000, 600, 300]  # Example stage values

        # Clear previous plots
        self.axes.clear()

        # Set the horizontal bar sizes and positions
        ypos = np.arange(len(stages), 0, -1)  # Reverse order for stages
        width_ratios = np.array(values) / max(values)

        # Draw the funnel layers
        for i, (stage, value) in enumerate(zip(stages, values)):
            self.axes.barh(
                ypos[i],
                width_ratios[i],
                color=f"C{i}",
                align="center",
                edgecolor="black",
                height=0.9,
            )
            # Add annotations with stage names and values
            self.axes.text(
                0.5,
                ypos[i],
                f"{stage}: {value}",
                ha="center",
                va="center",
                color="white",
                fontsize=12,
                fontweight="bold",
            )

        # Customize plot appearance
        self.axes.set_yticks([])  # Hide Y-axis ticks
        self.axes.set_xticks([])  # Hide X-axis ticks
        self.axes.set_xlim(0, 1)  # Funnel sections normalized
        self.axes.set_ylim(0, len(stages) + 1)
        self.axes.axis("off")  # Turn off axes for a cleaner look
        self.axes.set_title("Funnel Chart", fontsize=16)

        # Update the canvas
        self.draw()

    def plot_histogram_chart(self):
        """Generate and plot a histogram."""
        # Generate random data for the histogram
        data = np.random.normal(50, 10, 1000)  # Mean = 50, StdDev = 10, 1000 points

        # Clear previous plots
        self.axes.clear()

        # Plot the histogram
        self.axes.hist(
            data,
            bins=20,  # Number of bins
            color="skyblue",
            edgecolor="black",
            alpha=0.7,  # Transparency of bars
        )

        # Add titles and labels
        self.axes.set_title("Histogram Chart", fontsize=16)
        self.axes.set_xlabel("Value Range", fontsize=12)
        self.axes.set_ylabel("Frequency", fontsize=12)
        self.axes.grid(axis="y", linestyle="--", alpha=0.7)

        # Update the canvas to display the new chart
        self.draw()

    def plot_histogram_chart_3D(self):
        """Generate and plot a 3D histogram chart."""
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection="3d")

        data = np.random.normal(size=500)
        hist, bins = np.histogram(data, bins=10)
        xpos = np.arange(len(hist))
        ypos = np.zeros_like(xpos)
        zpos = np.zeros_like(xpos)
        dx = dy = 0.8
        dz = hist

        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color="purple", alpha=0.7)
        ax.set_title("3D Histogram")
        ax.set_xlabel("Bins")
        ax.set_ylabel("Fixed Y")
        ax.set_zlabel("Frequency")

        self.draw()

    def plot_gantt_chart(self):
        """Plot a Gantt chart."""
        # TODO: this feature is not working the entire graph widget disappears when gantt is selected in the chart type dropdown
        self.clear_axes()

        # Task positions (y-axis); reversed to plot Task A at the top
        task_positions = range(len(self.tasks))[::-1]

        # Plot each task as a horizontal bar
        for task, start_time, duration, y_pos in zip(self.tasks, self.start_times, self.durations, task_positions):
            self.axes.barh(
                y_pos,
                duration,
                left=start_time,
                height=0.5,
                align="center",
                color="skyblue",
                edgecolor="k",
                label=task if y_pos == task_positions[0] else "",
            )

        # Set y-axis ticks and labels
        self.axes.set_yticks(task_positions)
        self.axes.set_yticklabels(self.tasks)

        self.axes.set_title("Gantt Chart")
        self.axes.set_xlabel("Time")
        self.axes.set_ylabel("Tasks")
        self.axes.grid(axis="x", linestyle="--", alpha=0.7)
        self.draw()

    def plot_heat_chart(self):
        """Plot a heat chart."""
        # TODO: this feature is not working the entire graph widget disappears when HeatMap is selected in the chart type dropdown
        self.clear_axes()

        # Use Seaborn's heatmap function to create a heatmap
        sns.heatmap(
            self.heat_data,
            ax=self.axes,
            cmap="coolwarm",
            annot=True,
            fmt=".2f",
            cbar=True,
        )

        self.axes.set_title("Heat Chart")
        self.axes.set_xlabel("Columns")
        self.axes.set_ylabel("Rows")
        self.draw()

    def plot_line_chart(self):
        """Plot a basic line chart."""
        logma.info(f"Plot Line Chart")
        self.clear_axes()
        self.axes.plot(self.x, self.y1, label="Sine Wave", linewidth=2)
        self.axes.plot(self.x, self.y2, label="Cosine Wave", linewidth=2)
        self.axes.set_title("Line Chart")
        self.axes.set_xlabel("X-axis")
        self.axes.set_ylabel("Y-axis")
        self.axes.legend()
        self.draw()

    def plot_pareto_chart(self):
        """Generate and plot a Pareto chart."""
        # Clear previous plots
        self.fig.clear()
        ax1 = self.fig.add_subplot(111)

        # Example data
        categories = ["A", "B", "C", "D", "E", "F"]
        values = [40, 30, 15, 7, 5, 3]

        # Sort data in descending order
        sorted_data = sorted(zip(categories, values), key=lambda x: x[1], reverse=True)
        sorted_categories, sorted_values = zip(*sorted_data)

        # Cumulative percentage
        cumulative = np.cumsum(sorted_values) / sum(sorted_values) * 100

        # Create a Pareto chart
        bars = ax1.bar(
            sorted_categories,
            sorted_values,
            color="lightblue",
            alpha=0.7,
            label="Values",
        )
        ax1.set_ylabel("Value")
        ax1.set_xlabel("Categories")
        ax1.grid(axis="y", linestyle="--", alpha=0.6, linewidth=0.7)

        # Add a second axis to handle the cumulative percentage
        ax2 = ax1.twinx()
        ax2.plot(
            sorted_categories,
            cumulative,
            color="orange",
            marker="o",
            label="Cumulative %",
            linewidth=2,
        )
        ax2.set_ylabel("Cumulative Percentage (%)")
        ax2.set_ylim(0, 110)  # Ensure the scale matches the cumulative percentage range

        # Combine legends from both axes
        bars_legend = bars.get_legend_handles_labels()
        line_legend = ax2.get_legend_handles_labels()
        ax1.legend(*bars_legend, loc="upper left")
        ax2.legend(*line_legend, loc="upper right")

        # Title and layout
        ax1.set_title("Pareto Chart")
        self.fig.tight_layout()

        # Update the canvas
        self.draw()

    def plot_pie_chart(self):
        """Plots a pie chart."""
        self.clear_axes()
        values = [10, 30, 60]
        labels = ["blue", "green", "red"]
        self.axes.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            colors=sns.color_palette("pastel"),
        )
        self.axes.set_title("Pie Chart")
        self.draw()

    def plot_pie_chart_3D(self):
        """Generate and plot a 3D pie chart (as stacked bars)."""
        # TODO: Pie3D is showing the same graph as regular Pie chart
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection="3d")

        categories = ["A", "B", "C", "D"]
        values = [40, 30, 20, 10]
        xpos = np.arange(len(values))
        ypos = np.zeros_like(xpos)
        zpos = np.zeros_like(xpos)
        dx = dy = 0.8
        dz = values

        colors = plt.cm.Set3(np.linspace(0, 1, len(values)))
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors, edgecolor="black")
        ax.set_title("3D Pie Chart (Projected)")
        ax.set_xticks(xpos)
        ax.set_xticklabels(categories)
        ax.set_ylabel("Static Y")
        ax.set_zlabel("Value")

        self.draw()

    def plot_radar_chart(self):
        """Plots a radar chart."""
        self.clear_axes()
        values = [10, 30, 20, 10]
        labels = ["A", "B", "C", "D"]
        # Radar chart initialization
        num_vars = len(labels)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        values = values + [values[0]]  # Close the loop
        angles += angles[:1]  # Close the loop

        # Create radar plot
        self.axes = self.fig.add_subplot(111, polar=True)
        self.axes.fill(angles, values, color="skyblue", alpha=0.4)
        self.axes.plot(angles, values, color="blue", linewidth=2)

        self.axes.set_yticks([10, 20, 30, 40])  # Example tick marks
        self.axes.set_yticklabels(["10", "20", "30", "40"], color="grey", fontsize=8)

        # Set category names as labels
        self.axes.set_xticks(angles[:-1])
        self.axes.set_xticklabels(labels, fontsize=10)

        self.axes.set_title("Radar Chart", va="bottom")
        self.draw()

    def plot_sankey_chart(self):
        """Plots a Sankey chart."""
        self.clear_axes()
        Sankey(
            ax=self.axes,
            # Flow magnitudes (+ve = inflows, -ve = outflows)
            flows=[100, -40, -30, -30],
            # Labels for flows
            labels=["Input", "Output A", "Output B", "Output C"],
            # Orientation: 0 = horizontal, 1 = vertical
            orientations=[0, 1, -1, 0],
            scale=0.01,  # Adjust size of flows
            offset=0.2,
        ).finish()
        # colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],
        self.axes.set_title("Sankey Chart")
        self.draw()

    def plot_scatter_chart(self):
        """Plots a scatter plot."""
        self.clear_axes()
        self.axes.scatter(
            self.x,
            self.y1,
            alpha=0.7,
            s=50,  # Transparency and size of points
            color="teal",
        )
        self.axes.set_title("Scatter Plot")
        self.axes.set_xlabel("X-axis")
        self.axes.set_ylabel("Y-axis")
        self.draw()

    def plot_scatter_chart_3D(self):
        """Generate and plot a 3D scatter chart."""
        # Clear previous plots
        self.fig.clear()

        # Add a 3D subplot to the figure
        ax = self.fig.add_subplot(111, projection="3d")

        # Generate example data for the scatter plot
        num_points = 100
        x = np.random.uniform(-10, 10, num_points)  # X-axis values
        y = np.random.uniform(-10, 10, num_points)  # Y-axis values
        z = np.random.uniform(-10, 10, num_points)  # Z-axis values
        colors = np.random.rand(num_points)  # Colors for each point
        sizes = np.random.uniform(20, 200, num_points)  # Sizes for points

        # Create the scatter plot
        scatter_plot = ax.scatter(
            x,
            y,
            z,
            c=colors,  # Color gradient based on random values
            cmap="viridis",  # Colormap for colors
            s=sizes,  # Point sizes
            alpha=0.8,  # Transparency of points
            edgecolor="w",  # Add edgecolor for better visibility
        )

        # Add a color bar to represent the color scale
        self.fig.colorbar(scatter_plot, ax=ax, shrink=0.5, aspect=10)

        # Add titles and labels
        ax.set_title("3D Scatter Chart", fontsize=16)
        ax.set_xlabel("X-Axis")
        ax.set_ylabel("Y-Axis")
        ax.set_zlabel("Z-Axis")

        # Update the canvas
        self.draw()

    def plot_surface_chart(self):
        """Generate and plot a 3D surface chart."""
        # Clear previous plots
        self.fig.clear()

        # Add a 3D subplot to the figure
        ax = self.fig.add_subplot(111, projection="3d")

        # Generate example data for the surface
        X = np.linspace(-5, 5, 100)  # X-axis values
        Y = np.linspace(-5, 5, 100)  # Y-axis values
        X, Y = np.meshgrid(X, Y)  # Create a meshgrid for the surface
        Z = np.sin(np.sqrt(X**2 + Y**2))  # Function defining the surface

        # Plot the surface
        surf = ax.plot_surface(
            X,
            Y,
            Z,
            cmap="viridis",  # Colormap for surface colors
            edgecolor="none",
        )

        # Add color bar for reference
        self.fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

        # Add titles and labels
        ax.set_title("3D Surface Chart", fontsize=16)
        ax.set_xlabel("X-Axis")
        ax.set_ylabel("Y-Axis")
        ax.set_zlabel("Z-Axis")

        # Update the canvas
        self.draw()

    def plot_time_series_chart(self):
        """Plots a time series chart."""
        # TODO: this feature is not working the entire graph widget disappears when timeseries is selected in the chart type dropdown
        self.clear_axes()
        self.axes.plot(self.time_data, self.time_series_values, label="Cumulative Sum", linewidth=2)
        self.axes.set_title("Time Series Plot")
        self.axes.set_xlabel("Date")
        self.axes.set_ylabel("Value")
        self.axes.tick_params(axis="x", rotation=45)  # Rotate x-ticks for better readability
        self.axes.legend()
        self.draw()

    def plot_tree_chart(self):
        """Plot a basic line chart."""
        # pull in the DrillTreeChartWebEngine
        # TODO: this feature is not working the entire graph widget disappears when TreeMap is selected in the chart type dropdown

    def plot_violin_chart(self):
        """Generate and plot a violin chart."""
        # Clear any previous plot
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        # Example data: 4 categories with numeric data points
        categories = ["A", "B", "C", "D"]
        data = [
            np.random.normal(0, 1, 100),  # Category A
            np.random.normal(1, 0.5, 100),  # Category B
            np.random.normal(0, 1.5, 100),  # Category C
            np.random.normal(-1, 1, 100),  # Category D
        ]

        # Create the violin plot
        parts = ax.violinplot(data, showmeans=False, showmedians=True)

        # Customize the appearance of the violins
        for pc in parts["bodies"]:
            pc.set_facecolor("lightblue")  # Fill color
            pc.set_edgecolor("black")  # Border color
            pc.set_alpha(0.8)  # Transparency

        # Customize the other parts of the violin plot
        for partname in ("cbars", "cmins", "cmaxes", "cmedians"):
            if partname in parts:
                parts[partname].set_color("black")
                parts[partname].set_linewidth(1)

        # Set x-ticks (categories)
        ax.set_xticks(range(1, len(categories) + 1))
        ax.set_xticklabels(categories)

        # Set labels and titles
        ax.set_title("Violin Chart")
        ax.set_ylabel("Value")
        ax.set_xlabel("Category")

        # Add grid for better readability
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        # Redraw the chart
        self.draw()

    def plot_word_cloud(self):
        """Generate and plot a word cloud."""
        # Example text for the word cloud
        # TODO: this feature is not working the entire graph widget disappears when wordcloud is selected in the chart type dropdown
        text = (
            "Python programming, Matplotlib, PySide6, data visualization, charts, "
            "histograms, scatterplots, coding, pandas, NumPy, libraries, "
            "machine learning, AI, deep learning, integration"
        )

        # Clear previous plots
        self.axes.clear()

        # Create the Word Cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white",
            colormap="viridis",
            max_words=50,
            random_state=42,
        ).generate(text)

        # Display the Word Cloud
        self.axes.imshow(wordcloud, interpolation="bilinear")
        self.axes.axis("off")  # Hide axes for better visualization
        self.axes.set_title("Word Cloud", fontsize=16)

        # Update the canvas to display the new chart
        self.draw()

    def set_theme(self):
        """"""
        # sns.set_theme(style="darkgrid", palette="deep")  # Customize theme here
        themes = self.config.dikt.get("themes", None)
        if themes is None:
            theme = "DarkGrid"
            # Apply the custom theme using seaborn's `set_theme`
            sns.set_theme(style=theme.lower(), palette="deep")
            return self
        else:
            theme = themes["midnight_mist"]
        sns.set_theme(rc=theme)
        return self


class DrillTreeChart(pyqt.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Example data for hierarchical drill tree
        self.data = {
            "labels": [
                "Parent",
                "Child A",
                "Child B",
                "Child C",
                "Grandchild A1",
                "Grandchild A2",
                "Grandchild B1",
            ],
            "parents": [
                "",  # Parent node
                "Parent",
                "Parent",
                "Parent",
                "Child A",
                "Child A",
                "Child B",
            ],
            "values": [100, 30, 40, 30, 15, 15, 40],  # Values for each node
        }

        self.plot_drill_tree()

    def plot_drill_tree(self):
        """Renders the drill tree chart using Plotly."""
        fig = go.Figure(
            go.Treemap(
                labels=self.data["labels"],
                parents=self.data["parents"],
                values=self.data["values"],
                branchvalues="total",  # The numeric value of a parent includes its children
                hoverinfo="label+value+percent entry",  # Detailed information on hover
            )
        )

        fig.update_layout(title="Drill Tree Chart", margin=dict(t=50, l=25, r=25, b=25))

        # Render Plotly chart as HTML within QWebEngineView
        self.setHtml(fig.to_html(include_plotlyjs="cdn"))

    def set_theme(self):
        """"""
        theme = self.config.dikt.get("theme", None)
        if theme is None:
            theme = "DarkGrid"
            # Apply the custom theme using seaborn's `set_theme`
            sns.set_theme(theme)
            return self
        sns.set_theme(rc=theme)
        return self


class FunnelChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(None)  # Since we use Plotly, we don't need Matplotlib here
        self.parent = parent
        self.initialize_chart()

    def initialize_chart(self):
        """Generate and update the funnel chart."""
        # Example data for Funnel
        stages = ["Awareness", "Interest", "Consideration", "Evaluation", "Purchase"]
        values = [2000, 1500, 1000, 600, 300]

        # Create a Funnel Chart using Plotly
        funnel_chart = go.Figure(
            go.Funnel(
                y=stages,  # The stages of the funnel (y-axis)
                x=values,  # Corresponding values for each stage
                textinfo="value+percent previous",  # Add percentage and value to tooltips
            )
        )

        # Customize chart appearance
        funnel_chart.update_layout(
            title="Funnel Chart (with Plotly)",
            title_font_size=18,
            title_x=0.5,  # Center the title
            showlegend=False,  # No need for a legend in a funnel chart
            margin=dict(l=50, r=50, t=100, b=50),
        )

        # Save the funnel chart as an interactive HTML file
        funnel_chart.write_html("funnel_chart.html")

        # Display the funnel chart in a web browser
        logger.info(f"Saved 'funnel_chart.html'. Open it in a web browser!")

    def clear_canvas(self):
        """Clear the chart canvas (this is only relevant if you adapt this for live PySide6)."""
        pass

def render_bar_chart(self):
    """Render a bar chart with the provided series data."""
    for series in self.series:
        sns.barplot(
            x=series["data"]["x"],
            y=series["data"]["y"],
            label=series["data"]["label"].iloc[0],
            **series.get("kwargs", {}),
        )
    self.finalize_chart()


def render_line_chart(self):
    """Render a line chart with the provided series data."""
    for series in self.series:
        sns.lineplot(
            x=series["data"]["x"],
            y=series["data"]["y"],
            label=series["data"]["label"].iloc[0],
            **series.get("kwargs", {}),
        )
    self.finalize_chart()


def render_area_chart(self):
    """Render an area chart with the provided series data (using `fill_between`)."""
    for series in self.series:
        plt.fill_between(
            series["data"]["x"],
            series["data"]["y"],
            label=series["data"]["label"].iloc[0],
            alpha=0.4,
            **series.get("kwargs", {}),
        )
    self.finalize_chart()


def render_scatter_plot(self):
    """Render a scatter plot with the provided series data."""
    for series in self.series:
        sns.scatterplot(
            x=series["data"]["x"],
            y=series["data"]["y"],
            label=series["data"]["label"].iloc[0],
            **series.get("kwargs", {}),
        )
    self.finalize_chart()


def render_box_plot(self, x: str = None, y: str = None, **kwargs):
    """
    Render a box plot for visualizing distributions.

    Args:
        x (str): Column name for the X-axis.
        y (str): Column name for the Y-axis.
        **kwargs: Additional Seaborn boxplot parameters (e.g., hue).
    """
    sns.boxplot(data=self.data, x=x, y=y, **kwargs)
    self.finalize_chart()


def render_histogram(self, x: str, bins: int = 20, kde: bool = False, **kwargs):
    """
    Render a histogram for a single variable.

    Args:
        x (str): Column name for the variable.
        bins (int): Number of bins.
        kde (bool): Whether to overlay a kernel density estimation (KDE).
        **kwargs: Additional Seaborn parameters (e.g., color).
    """
    sns.histplot(data=self.data, x=x, bins=bins, kde=kde, **kwargs)
    self.finalize_chart()


def render_pie_chart(self, values: list, labels: list, **kwargs):
    """
    Render a pie chart using Matplotlib.

    Args:
        values (list): List of values for the pie slices.
        labels (list): Corresponding labels for the slices.
        **kwargs: Additional matplotlib.pie parameters (e.g., colors, explode).
    """
    plt.pie(values, labels=labels, autopct="%1.1f%%", **kwargs)
    plt.title(self.title, fontsize=16)
    plt.show()


def render_heatmap(self, data: DataFrame, cmap="viridis", **kwargs):
    """
    Render a heatmap from a 2D data array.

    Args:
        data (DataFrame): 2-dimensional data for the heatmap.
        cmap (str): Color palette for the heatmap.
        **kwargs: Additional Seaborn heatmap parameters.
    """
    sns.heatmap(data, annot=True, cmap=cmap, **kwargs)
    self.finalize_chart()
def finalize_chart(self):
    """
    Finalize the chart by setting the title, axis labels, legends, and showing the plot.
    """

    plt.show()
# ===========================Code Source Examples================================||
"""
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
