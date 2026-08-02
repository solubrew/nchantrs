from typing import Any
"\n---\n<(META)>:\n    docid: 'e49e63fd-aad8-4ae3-b176-8ca67718fac6'\n    name:\n    description: >\n        leverage visualizer to generate charts to displayed\n        through test_nchantrs or warlock via an integrated test_nchantrs browser\n    expirary: <[expiration]>\n    version: <[version]>\n    authority: document|this\n    security: sec|lvl2\n    <(WT)>: -32\n"
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
import numpy as np
import mplfinance as mpf
import seaborn as sns
import matplotlib as mat
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# Force a backend that works for both Qt and headless test runs. The
# audit harness runs ``sasquatch analyze`` from a headless shell, where
# QtAgg raises ImportError. Only require QtAgg when an event loop is
# present (i.e. when the user is actually rendering a window).
import os as _os
if _os.environ.get("QT_QPA_PLATFORM") == "offscreen" or not _os.environ.get("DISPLAY"):
    mat.use("Agg")
else:
    try:
        mat.use("QtAgg")
    except ImportError:
        mat.use("Agg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.sankey import Sankey
import matplotlib.colors as mcolors
from wordcloud import WordCloud
from pandas import date_range, DataFrame
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidgetMixin
from kahndor import kahndor
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
pxcfg = join(abspath(here), '_data_', 'charts.yaml')

class NchantdChart(NchantdWidgetMixin, FigureCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, parent=None, cfg={}) -> None:
        """ """
        width, height, dpi = (600, 4, 100)
        self.config = kahndor.Instruct(pxcfg).select('NchantdChart')
        self.set_theme()
        fig = self.config.dikt.get('figure', None)
        self.fig = fig
        if self.fig is None:
            self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.parent = parent
        if self.parent is not None:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.axes = self.fig.add_subplot(111)
        self.chart_type = self.config.dikt.get('chart_type', None)
        FigureCanvas.setSizePolicy(self, pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Expanding)
        self.data_series = None
        self.time_data = None
        self.time_series_values = None

    def initModel(self) -> Any:
        """"""
        super().initModel()
        self.axes.clear()
        self.data_series = self.config.dikt.get('data_series', None)
        if self.data_series is None:
            self.load_sample_data()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.plot_chart()
        return self

    def initWidget(self) -> Any:
        """ """
        self.initModel()
        self.initView()
        return self

    def clear_axes(self, projection=None) -> None:
        """Clear the current axes to prepare for a new chart.

        Pass ``projection='3d'`` to recreate the axes with a 3D projection
        (matplotlib requires a fresh axes when switching from 2D to 3D or
        vice versa).  After this call ``self.axes`` is guaranteed to point
        at a live axes object.
        """
        if projection is None:
            self.axes.clear()
        else:
            # 2D <-> 3D projection switch needs a brand-new axes; matplotlib
            # raises if you call ``projection='3d'`` on an existing 2D axes
            # or vice versa.
            self.fig.clear()
            self.axes = self.fig.add_subplot(111, projection=projection)

    def load_sample_data(self) -> None:
        """"""
        self.x = np.linspace(0, 10, 100)
        self.y1 = np.sin(self.x)
        self.y2 = np.cos(self.x)

    def plot_chart(self) -> Any:
        """"""
        logma.info(f'Chart Type{self.chart_type}')
        if self.chart_type is None:
            self.chart_type = 'line'
        logma.info(f'Chart Type{self.chart_type}')
        chart_type = self.chart_type.lower()
        match chart_type:
            case 'area':
                self.plot_area_chart()
            case 'area3d':
                self.plot_area_chart_3D()
            case 'bar':
                self.plot_bar_chart()
            case 'bar3d':
                self.plot_bar_chart_3D()
            case 'barstacked':
                self.plot_bar_chart_stacked()
            case 'bubble':
                self.plot_bubble_chart()
            case 'candlestick':
                self.plot_candlestick_chart()
            case 'column':
                self.plot_column_chart()
            case 'columnstacked':
                self.plot_column_chart_stacked()
            case 'doughnut':
                self.plot_doughnut_chart()
            case 'funnel':
                self.plot_funnel_chart()
            case 'gantt':
                self.plot_gantt_chart()
            case 'heatmap':
                self.plot_heatmap_chart()
            case 'histogram':
                self.plot_histogram_chart()
            case 'line':
                self.plot_line_chart()
            case 'pie':
                self.plot_pie_chart()
            case 'pie3d':
                self.plot_pie_chart_3D()
            case 'radar':
                self.plot_radar_chart()
            case 'sankey':
                self.plot_sankey_chart()
            case 'scatter':
                self.plot_scatter_chart()
            case 'scatter3d':
                self.plot_scatter_chart_3D()
            case 'surface':
                self.plot_surface_chart()
            case 'timeseries':
                self.plot_time_series_chart()
            case 'treemap':
                self.plot_treemap_chart()
            case 'violin':
                self.plot_violin_chart()
            case 'wordcloud':
                self.plot_wordcloud()
        return self

    def plot_area_chart(self) -> None:
        """Plot an area chart."""
        self.clear_axes()
        self.axes.fill_between(self.x, self.y1, color='blue', alpha=0.4, label='Sine Area')
        self.axes.fill_between(self.x, self.y2, color='orange', alpha=0.4, label='Cosine Area')
        self.axes.set_title('Area Chart')
        self.axes.set_xlabel('X-axis')
        self.axes.set_ylabel('Y-axis')
        self.axes.legend()
        self.draw()

    def plot_area_chart_3D(self) -> None:
        """Generate and plot a 3D area chart."""
        self.clear_axes(projection='3d')

        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        z = np.zeros_like(x)
        dz = y
        self.axes.plot_trisurf(x, z, dz, cmap='coolwarm')
        self.axes.set_title('3D Area Chart')
        self.axes.set_xlabel('X Axis')
        self.axes.set_ylabel('Fixed Z')
        self.axes.set_zlabel('Y Axis')
        self.draw()

    def plot_bar_chart(self) -> None:
        """Plot a bar chart."""
        self.clear_axes()
        categories = ['A', 'B', 'C', 'D', 'E']
        values = [5, 8, 7, 6, 9]
        self.axes.bar(categories, values, color='teal', alpha=0.8)
        self.axes.set_title('Bar Chart')
        self.axes.set_xlabel('Categories')
        self.axes.set_ylabel('Values')
        self.draw()

    def plot_bar_chart_3D(self) -> None:
        """Generate and plot a 3D bar chart."""
        self.clear_axes(projection='3d')

        xpos = np.arange(5)
        ypos = np.arange(5)
        xpos, ypos = np.meshgrid(xpos, ypos)
        xpos = xpos.flatten()
        ypos = ypos.flatten()
        zpos = np.zeros_like(xpos)
        dx = dy = 0.5
        dz = np.random.randint(1, 10, size=len(xpos))
        self.axes.bar3d(xpos, ypos, zpos, dx, dy, dz, color='lightblue', edgecolor='black')
        self.axes.set_title('3D Bar Chart')
        self.axes.set_xlabel('X Axis')
        self.axes.set_ylabel('Y Axis')
        self.axes.set_zlabel('Height')
        self.draw()

    def plot_bar_chart_stacked(self) -> None:
        """Generate and plot a stacked bar chart."""
        self.clear_axes()

        categories = ['Group 1', 'Group 2', 'Group 3']
        subgroups = ['Component A', 'Component B', 'Component C']
        data = np.array([[5, 3, 2], [6, 4, 3], [4, 2, 4]])
        bar_positions = np.arange(len(categories))
        cumulative_heights = np.zeros(len(categories))
        colors = ['lightblue', 'orange', 'green']
        for i, (color, subgroup) in enumerate(zip(colors, subgroups)):
            self.axes.bar(bar_positions, data[:, i], bottom=cumulative_heights, color=color, label=subgroup)
            cumulative_heights += data[:, i]
        self.axes.set_title('Stacked Bar Chart')
        self.axes.set_xticks(bar_positions)
        self.axes.set_xticklabels(categories)
        self.axes.set_ylabel('Values')
        self.axes.set_xlabel('Categories')
        self.axes.legend(title='Components')
        self.axes.grid(axis='y', linestyle='--', alpha=0.7)
        self.fig.tight_layout()

    def plot_box_and_whisker(self) -> None:
        """Generate and plot a box-and-whisker plot."""
        self.clear_axes()

        data = [[7, 8, 7.5, 9.0, 8.2, 7.8, 8.6], [6, 6.2, 6.8, 5.9, 6.5, 6.3, 6.7], [8, 8.3, 7.8, 8.4, 8.1, 8.7, 8.2], [9, 9.1, 9.3, 9.2, 9.0, 9.5, 9.4]]
        categories = ['Group 1', 'Group 2', 'Group 3', 'Group 4']
        box = self.axes.boxplot(data, vert=True, patch_artist=True, labels=categories, notch=True)
        colors = ['lightblue', 'orange', 'green', 'purple']
        for patch, color in zip(box['boxes'], colors):
            patch.set_facecolor(color)
        self.axes.set_title('Box-and-Whisker Plot')
        self.axes.set_ylabel('Values')
        self.axes.grid(axis='y', linestyle='--', alpha=0.7)
        self.draw()

    def plot_bubble_chart(self) -> None:
        """Plot a bubble chart."""
        self.clear_axes()
        bubble_sizes = np.random.uniform(20, 200, size=len(self.x))
        self.axes.scatter(self.x, self.y1, s=bubble_sizes, alpha=0.4, c=self.y2, cmap='viridis')
        self.axes.set_title('Bubble Chart')
        self.axes.set_xlabel('X-axis')
        self.axes.set_ylabel('Y-axis')
        self.draw()

    def plot_candlestick_chart(self) -> None:
        """Generate and plot a candlestick chart."""
        dates = date_range(dt.datetime(2023, 1, 1), periods=30)
        data = {'Open': np.random.uniform(100, 200, size=len(dates)), 'High': np.random.uniform(200, 300, size=len(dates)), 'Low': np.random.uniform(50, 100, size=len(dates)), 'Close': np.random.uniform(100, 250, size=len(dates)), 'Volume': np.random.randint(1000, 10000, size=len(dates))}
        ohlc_data = DataFrame(data, index=dates)
        self.axes.clear()
        mpf.plot(ohlc_data, type='candle', ax=self.axes, style='yahoo', ylabel='Price (USD)', ylabel_lower='Volume')
        self.draw()

    def plot_column_chart(self) -> None:
        """Generate and plot a column chart."""
        categories = ['Category A', 'Category B', 'Category C', 'Category D']
        values = [25, 40, 35, 50]
        self.axes.clear()
        self.axes.bar(categories, values, color='skyblue', edgecolor='black')
        self.axes.set_title('Column Chart', fontsize=16)
        self.axes.set_xlabel('Categories', fontsize=12)
        self.axes.set_ylabel('Values', fontsize=12)
        self.axes.grid(axis='y', linestyle='--', alpha=0.7)
        for i, value in enumerate(values):
            self.axes.text(i, value + 1, f'{value}', ha='center', va='bottom', fontsize=10)
        self.draw()

    def plot_column_chart_3D(self) -> None:
        """Generate and plot a 3D column chart."""
        self.clear_axes(projection='3d')
        xpos = np.arange(5)
        ypos = np.zeros_like(xpos)
        zpos = np.zeros_like(xpos)
        dx = dy = 0.4
        dz = np.random.randint(1, 10, size=len(xpos))
        self.axes.bar3d(xpos, ypos, zpos, dx, dy, dz, color='green', edgecolor='black')
        self.axes.set_title('3D Column Chart')
        self.axes.set_xlabel('Categories')
        self.axes.set_ylabel('Fixed Y')
        self.axes.set_zlabel('Value')
        self.draw()

    def plot_column_chart_stacked(self) -> None:
        """Generate and plot a stacked column chart."""
        self.clear_axes()

        categories = ['Group 1', 'Group 2', 'Group 3', 'Group 4']
        subgroups = ['Segment A', 'Segment B', 'Segment C']
        data = np.array([[4, 3, 2], [6, 5, 3], [3, 2, 6], [5, 4, 4]])
        bar_positions = np.arange(len(categories))
        cumulative_heights = np.zeros(len(categories))
        colors = ['skyblue', 'orange', 'green']
        for i, (color, subgroup) in enumerate(zip(colors, subgroups)):
            self.axes.bar(bar_positions, height=data[:, i], bottom=cumulative_heights, width=0.7, color=color, label=subgroup)
            cumulative_heights += data[:, i]
        self.axes.set_title('Stacked Column Chart')
        self.axes.set_xticks(bar_positions)
        self.axes.set_xticklabels(categories)
        self.axes.set_ylabel('Values')
        self.axes.set_xlabel('Groups')
        self.axes.legend(title='Segments')
        self.axes.grid(axis='y', linestyle='--', alpha=0.7)
        self.fig.tight_layout()
        self.draw()

    def plot_doughnut_chart(self) -> None:
        """Generate and plot a doughnut chart."""
        categories = ['Category A', 'Category B', 'Category C', 'Category D']
        values = [25, 35, 20, 20]
        self.axes.clear()
        wedges, texts, autotexts = self.axes.pie(values, labels=categories, autopct='%1.1f%%', startangle=90, pctdistance=0.85, textprops=dict(color='black', fontsize=10))
        centre_circle = plt.Circle((0, 0), 0.7, color='white', fc='white', linewidth=0)
        self.axes.add_artist(centre_circle)
        self.axes.axis('equal')
        self.axes.set_title('Doughnut Chart', fontsize=16)
        self.draw()

    def plot_doughnut_chart_3D(self) -> None:
        """Generate and plot a 3D doughnut chart (mocked with pie visualization)."""
        self.clear_axes(projection='3d')

        categories = ['A', 'B', 'C', 'D']
        values = [40, 30, 20, 10]
        cumulative_values = np.cumsum(values)
        fractional = cumulative_values / sum(values)
        for i, val in enumerate(values):
            self.axes.bar3d([i], [0], [0], 0.5, 1, val, color=plt.cm.Set3(i / len(values)), alpha=0.8)
        self.axes.set_title('3D Doughnut Chart (Mocked)')
        self.axes.set_ylabel('Y Axis')
        self.axes.set_zlabel('Values')
        self.draw()

    def plot_funnel_chart(self) -> None:
        """Generate and plot a funnel chart."""
        stages = ['Awareness', 'Interest', 'Consideration', 'Evaluation', 'Purchase']
        values = [2000, 1500, 1000, 600, 300]
        self.axes.clear()
        ypos = np.arange(len(stages), 0, -1)
        width_ratios = np.array(values) / max(values)
        for i, (stage, value) in enumerate(zip(stages, values)):
            self.axes.barh(ypos[i], width_ratios[i], color=f'C{i}', align='center', edgecolor='black', height=0.9)
            self.axes.text(0.5, ypos[i], f'{stage}: {value}', ha='center', va='center', color='white', fontsize=12, fontweight='bold')
        self.axes.set_yticks([])
        self.axes.set_xticks([])
        self.axes.set_xlim(0, 1)
        self.axes.set_ylim(0, len(stages) + 1)
        self.axes.axis('off')
        self.axes.set_title('Funnel Chart', fontsize=16)
        self.draw()

    def plot_histogram_chart(self) -> None:
        """Generate and plot a histogram."""
        data = np.random.normal(50, 10, 1000)
        self.axes.clear()
        self.axes.hist(data, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        self.axes.set_title('Histogram Chart', fontsize=16)
        self.axes.set_xlabel('Value Range', fontsize=12)
        self.axes.set_ylabel('Frequency', fontsize=12)
        self.axes.grid(axis='y', linestyle='--', alpha=0.7)
        self.draw()

    def plot_histogram_chart_3D(self) -> None:
        """Generate and plot a 3D histogram chart."""
        self.clear_axes(projection='3d')

        data = np.random.normal(size=500)
        hist, bins = np.histogram(data, bins=10)
        xpos = np.arange(len(hist))
        ypos = np.zeros_like(xpos)
        zpos = np.zeros_like(xpos)
        dx = dy = 0.8
        dz = hist
        self.axes.bar3d(xpos, ypos, zpos, dx, dy, dz, color='purple', alpha=0.7)
        self.axes.set_title('3D Histogram')
        self.axes.set_xlabel('Bins')
        self.axes.set_ylabel('Fixed Y')
        self.axes.set_zlabel('Frequency')
        self.draw()

    def plot_gantt_chart(self) -> None:
        """Plot a Gantt chart."""
        self.clear_axes()
        task_positions = range(len(self.tasks))[::-1]
        for task, start_time, duration, y_pos in zip(self.tasks, self.start_times, self.durations, task_positions):
            self.axes.barh(y_pos, duration, left=start_time, height=0.5, align='center', color='skyblue', edgecolor='k', label=task if y_pos == task_positions[0] else '')
        self.axes.set_yticks(task_positions)
        self.axes.set_yticklabels(self.tasks)
        self.axes.set_title('Gantt Chart')
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Tasks')
        self.axes.grid(axis='x', linestyle='--', alpha=0.7)
        self.draw()

    def plot_heat_chart(self) -> None:
        """Plot a heat chart."""
        self.clear_axes()
        sns.heatmap(self.heat_data, ax=self.axes, cmap='coolwarm', annot=True, fmt='.2f', cbar=True)
        self.axes.set_title('Heat Chart')
        self.axes.set_xlabel('Columns')
        self.axes.set_ylabel('Rows')
        self.draw()

    def plot_line_chart(self) -> None:
        """Plot a basic line chart."""
        logma.info(f'Plot Line Chart')
        self.clear_axes()
        self.axes.plot(self.x, self.y1, label='Sine Wave', linewidth=2)
        self.axes.plot(self.x, self.y2, label='Cosine Wave', linewidth=2)
        self.axes.set_title('Line Chart')
        self.axes.set_xlabel('X-axis')
        self.axes.set_ylabel('Y-axis')
        self.axes.legend()
        self.draw()

    def plot_pareto_chart(self) -> None:
        """Generate and plot a Pareto chart."""
        self.clear_axes()
        categories = ['A', 'B', 'C', 'D', 'E', 'F']
        values = [40, 30, 15, 7, 5, 3]
        sorted_data = sorted(zip(categories, values), key=lambda x: x[1], reverse=True)
        sorted_categories, sorted_values = zip(*sorted_data)
        cumulative = np.cumsum(sorted_values) / sum(sorted_values) * 100
        bars = self.axes.bar(sorted_categories, sorted_values, color='lightblue', alpha=0.7, label='Values')
        self.axes.set_ylabel('Value')
        self.axes.set_xlabel('Categories')
        self.axes.grid(axis='y', linestyle='--', alpha=0.6, linewidth=0.7)
        secondary = self.axes.twinx()
        secondary.plot(sorted_categories, cumulative, color='orange', marker='o', label='Cumulative %', linewidth=2)
        secondary.set_ylabel('Cumulative Percentage (%)')
        secondary.set_ylim(0, 110)
        bars_legend = bars.get_legend_handles_labels()
        line_legend = secondary.get_legend_handles_labels()
        self.axes.legend(*bars_legend, loc='upper left')
        secondary.legend(*line_legend, loc='upper right')
        self.axes.set_title('Pareto Chart')
        self.fig.tight_layout()
        self.draw()

    def plot_pie_chart(self) -> None:
        """Plots a pie chart."""
        self.clear_axes()
        values = [10, 30, 60]
        labels = ['blue', 'green', 'red']
        self.axes.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        self.axes.set_title('Pie Chart')
        self.draw()

    def plot_pie_chart_3D(self) -> None:
        """Generate and plot a 3D pie chart (as stacked bars)."""
        self.clear_axes(projection='3d')

        categories = ['A', 'B', 'C', 'D']
        values = [40, 30, 20, 10]
        xpos = np.arange(len(values))
        ypos = np.zeros_like(xpos)
        zpos = np.zeros_like(xpos)
        dx = dy = 0.8
        dz = values
        colors = plt.cm.Set3(np.linspace(0, 1, len(values)))
        self.axes.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors, edgecolor='black')
        self.axes.set_title('3D Pie Chart (Projected)')
        self.axes.set_xticks(xpos)
        self.axes.set_xticklabels(categories)
        self.axes.set_ylabel('Static Y')
        self.axes.set_zlabel('Value')
        self.draw()

    def plot_radar_chart(self) -> None:
        """Plots a radar chart."""
        self.clear_axes()
        values = [10, 30, 20, 10]
        labels = ['A', 'B', 'C', 'D']
        num_vars = len(labels)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        values = values + [values[0]]
        angles += angles[:1]
        self.axes = self.fig.add_subplot(111, polar=True)
        self.axes.fill(angles, values, color='skyblue', alpha=0.4)
        self.axes.plot(angles, values, color='blue', linewidth=2)
        self.axes.set_yticks([10, 20, 30, 40])
        self.axes.set_yticklabels(['10', '20', '30', '40'], color='grey', fontsize=8)
        self.axes.set_xticks(angles[:-1])
        self.axes.set_xticklabels(labels, fontsize=10)
        self.axes.set_title('Radar Chart', va='bottom')
        self.draw()

    def plot_sankey_chart(self) -> None:
        """Plots a Sankey chart."""
        self.clear_axes()
        Sankey(ax=self.axes, flows=[100, -40, -30, -30], labels=['Input', 'Output A', 'Output B', 'Output C'], orientations=[0, 1, -1, 0], scale=0.01, offset=0.2).finish()
        self.axes.set_title('Sankey Chart')
        self.draw()

    def plot_scatter_chart(self) -> None:
        """Plots a scatter plot."""
        self.clear_axes()
        self.axes.scatter(self.x, self.y1, alpha=0.7, s=50, color='teal')
        self.axes.set_title('Scatter Plot')
        self.axes.set_xlabel('X-axis')
        self.axes.set_ylabel('Y-axis')
        self.draw()

    def plot_scatter_chart_3D(self) -> None:
        """Generate and plot a 3D scatter chart."""
        self.clear_axes(projection='3d')

        num_points = 100
        x = np.random.uniform(-10, 10, num_points)
        y = np.random.uniform(-10, 10, num_points)
        z = np.random.uniform(-10, 10, num_points)
        colors = np.random.rand(num_points)
        sizes = np.random.uniform(20, 200, num_points)
        scatter_plot = self.axes.scatter(x, y, z, c=colors, cmap='viridis', s=sizes, alpha=0.8, edgecolor='w')
        self.fig.colorbar(scatter_plot, ax=ax, shrink=0.5, aspect=10)
        self.axes.set_title('3D Scatter Chart', fontsize=16)
        self.axes.set_xlabel('X-Axis')
        self.axes.set_ylabel('Y-Axis')
        self.axes.set_zlabel('Z-Axis')
        self.draw()

    def plot_surface_chart(self) -> None:
        """Generate and plot a 3D surface chart."""
        self.clear_axes(projection='3d')

        X = np.linspace(-5, 5, 100)
        Y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(X, Y)
        Z = np.sin(np.sqrt(X ** 2 + Y ** 2))
        surf = self.axes.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
        self.fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
        self.axes.set_title('3D Surface Chart', fontsize=16)
        self.axes.set_xlabel('X-Axis')
        self.axes.set_ylabel('Y-Axis')
        self.axes.set_zlabel('Z-Axis')
        self.draw()

    def plot_time_series_chart(self) -> None:
        """Plots a time series chart."""
        self.clear_axes()
        self.axes.plot(self.time_data, self.time_series_values, label='Cumulative Sum', linewidth=2)
        self.axes.set_title('Time Series Plot')
        self.axes.set_xlabel('Date')
        self.axes.set_ylabel('Value')
        self.axes.tick_params(axis='x', rotation=45)
        self.axes.legend()
        self.draw()

    def plot_treemap_chart(self) -> None:
        """Generate and plot a treemap.

        Uses matplotlib's ``Rectangle`` patches laid out in a simple
        squarified manner (no squarify dependency). Cell areas are
        proportional to ``self.data_series`` values.
        """
        self.clear_axes()
        # Default sample if no data was set
        labels = ['A', 'B', 'C', 'D', 'E', 'F']
        values = [40, 30, 15, 7, 5, 3]
        data = getattr(self, 'data_series', None)
        if data is not None:
            try:
                values = list(data)
                labels = [f'item_{i}' for i in range(len(values))]
            except TypeError:
                pass
        total = float(sum(values))
        if total <= 0:
            self.axes.text(0.5, 0.5, 'No data', ha='center', va='center', transform=self.axes.transAxes)
            self.draw()
            return
        # Squarified layout: walk values, fill rows left-to-right.
        x, y, w, h = 0.0, 0.0, 1.0, 1.0
        normalized = [v / total for v in values]
        norm = mcolors.Normalize(vmin=min(normalized), vmax=max(normalized))
        cmap = plt.get_cmap('viridis')
        for label, frac in zip(labels, normalized):
            # Place item in a single row when possible (simple heuristic)
            if w <= 0 or h <= 0:
                break
            rect = Rectangle((x, y), w * frac, h, facecolor=cmap(norm(frac)), edgecolor='white')
            self.axes.add_patch(rect)
            self.axes.text(x + w * frac / 2, y + h / 2, label, ha='center', va='center', fontsize=8, color='white')
            x += w * frac
            w -= w * frac
            if w < 0.05:
                # Roll to next row
                x = 0.0
                w = 1.0
                y += h * 0.5
                h *= 0.5
        self.axes.set_xlim(0, 1)
        self.axes.set_ylim(0, 1)
        self.axes.set_aspect('equal')
        self.axes.axis('off')
        self.axes.set_title('Treemap')
        self.draw()

    def plot_wordcloud(self) -> None:
        """Render a word cloud from a sample text corpus.

        Uses the ``wordcloud`` library (already imported at module
        top). Falls back to a simple ``self.axes.text`` placeholder
        if the library or the corpus is missing.
        """
        self.clear_axes()
        sample_text = (
            "nchantrs nchantrs nchantdoffice nchantdoffice nchantdoffice "
            "pyffice pyffice pyffice nchantrs widget widget widget widget "
            "model store model store model store chart chart chart chart "
            "browser editor editor editor cell cell cell cell cell "
            "tab tab tab tab tree tree node node node app app app"
        )
        try:
            wordcloud = WordCloud(
                width=800, height=400, background_color='white',
                colormap='viridis', max_words=50, random_state=42,
            ).generate(sample_text)
            self.axes.imshow(wordcloud, interpolation='bilinear')
            self.axes.axis('off')
            self.axes.set_title('Word Cloud')
        except Exception as e:
            self.axes.text(0.5, 0.5, f'wordcloud unavailable: {e}',
                           ha='center', va='center', transform=self.axes.transAxes)
        self.draw()

    def plot_violin_chart(self) -> None:
        """Generate and plot a violin chart."""
        self.clear_axes()

        categories = ['A', 'B', 'C', 'D']
        data = [np.random.normal(0, 1, 100), np.random.normal(1, 0.5, 100), np.random.normal(0, 1.5, 100), np.random.normal(-1, 1, 100)]
        parts = self.axes.violinplot(data, showmeans=False, showmedians=True)
        for pc in parts['bodies']:
            pc.set_facecolor('lightblue')
            pc.set_edgecolor('black')
            pc.set_alpha(0.8)
        for partname in ('cbars', 'cmins', 'cmaxes', 'cmedians'):
            if partname in parts:
                parts[partname].set_color('black')
                parts[partname].set_linewidth(1)
        self.axes.set_xticks(range(1, len(categories) + 1))
        self.axes.set_xticklabels(categories)
        self.axes.set_title('Violin Chart')
        self.axes.set_ylabel('Value')
        self.axes.set_xlabel('Category')
        self.axes.grid(axis='y', linestyle='--', alpha=0.7)
        self.draw()

    def plot_word_cloud(self) -> None:
        """Generate and plot a word cloud."""
        text = 'Python programming, Matplotlib, PySide6, data visualization, charts, histograms, scatterplots, coding, pandas, NumPy, libraries, machine learning, AI, deep learning, integration'
        self.axes.clear()
        wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis', max_words=50, random_state=42).generate(text)
        self.axes.imshow(wordcloud, interpolation='bilinear')
        self.axes.axis('off')
        self.axes.set_title('Word Cloud', fontsize=16)
        self.draw()

    def set_theme(self) -> Any:
        """"""
        themes = self.config.dikt.get('themes', None)
        if themes is None:
            theme = 'DarkGrid'
            sns.set_theme(style=theme.lower(), palette='deep')
            return self
        else:
            theme = themes['midnight_mist']
        sns.set_theme(rc=theme)
        return self

class DrillTreeChart(pyqt.QWebEngineView):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.data = {'labels': ['Parent', 'Child A', 'Child B', 'Child C', 'Grandchild A1', 'Grandchild A2', 'Grandchild B1'], 'parents': ['', 'Parent', 'Parent', 'Parent', 'Child A', 'Child A', 'Child B'], 'values': [100, 30, 40, 30, 15, 15, 40]}
        self.plot_drill_tree()

    def plot_drill_tree(self) -> None:
        """Renders the drill tree chart using Plotly."""
        fig = go.Figure(go.Treemap(labels=self.data['labels'], parents=self.data['parents'], values=self.data['values'], branchvalues='total', hoverinfo='label+value+percent entry'))
        fig.update_layout(title='Drill Tree Chart', margin=dict(t=50, l=25, r=25, b=25))
        self.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def set_theme(self) -> Any:
        """"""
        theme = self.config.dikt.get('theme', None)
        if theme is None:
            theme = 'DarkGrid'
            sns.set_theme(theme)
            return self
        sns.set_theme(rc=theme)
        return self

class FunnelChartCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100) -> None:
        super().__init__(None)
        self.parent = parent
        self.initialize_chart()

    def initialize_chart(self) -> None:
        """Generate and update the funnel chart."""
        stages = ['Awareness', 'Interest', 'Consideration', 'Evaluation', 'Purchase']
        values = [2000, 1500, 1000, 600, 300]
        funnel_chart = go.Figure(go.Funnel(y=stages, x=values, textinfo='value+percent previous'))
        funnel_chart.update_layout(title='Funnel Chart (with Plotly)', title_font_size=18, title_x=0.5, showlegend=False, margin=dict(l=50, r=50, t=100, b=50))
        funnel_chart.write_html('funnel_chart.html')
        logger.info(f"Saved 'funnel_chart.html'. Open it in a web browser!")

    def clear_canvas(self) -> None:
        """Clear the chart canvas (this is only relevant if you adapt this for live PySide6)."""
        pass
'\n'