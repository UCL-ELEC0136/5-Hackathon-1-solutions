"""
This module contains methods to create, show and save useful plots to visualise and explore data.
"""

import os
import matplotlib.pyplot as plt
from typing import Tuple, List, Any

def histogram(data: List[int]) -> Tuple[Any, Any]:
    """
    Create a histogram plot.

    Args:
        data (List[int]): The data to be plotted.

    Returns:
        Tuple[Any, Any]: The figure and axis of the plot.
    """
    fig, ax = plt.subplots()
    ax.hist(data, bins=20)
    ax.set_title(
        "Number of commits per repo in the https://github.com/google organisation"
    )
    ax.set_xlabel("Repository index")
    ax.set_ylabel("Number of commits")
    return fig, ax

def boxplot(mean: float, min_val: float, max_val: float, percentile_5: float, percentile_95: float) -> Tuple[Any, Any]:
    """
    Create a boxplot.

    Args:
        mean (float): The mean value.
        min_val (float): The minimum value.
        max_val (float): The maximum value.
        percentile_5 (float): The 5th percentile value.
        percentile_95 (float): The 95th percentile value.

    Returns:
        Tuple[Any, Any]: The figure and axis of the plot.
    """
    fig, ax = plt.subplots()
    boxes = [
        {
            "label": "Aggregated statistics for the commits in each google repository",
            "whislo": min_val,
            "q1": percentile_5,
            "med": mean,
            "q3": percentile_95,
            "whishi": max_val,
            "fliers": [],
        }
    ]
    ax.bxp(boxes, showfliers=False)
    ax.set_ylabel("cm")
    return fig, ax

def lineplot(x: List[Any], y: List[int]) -> Tuple[Any, Any]:
    """
    Create a line plot.

    Args:
        x (List[Any]): The x-axis data.
        y (List[int]): The y-axis data.

    Returns:
        Tuple[Any, Any]: The figure and axis of the plot.
    """
    fig, ax = plt.subplots()
    ax.plot(x, y)
    return fig, ax

def save_figure(fig: Any, filename: str) -> None:
    """
    Save a figure to a file.

    Args:
        fig (Any): The figure to be saved.
        filename (str): The name of the file.
    """
    folder = os.path.dirname(filename)
    if folder != "":
        os.makedirs(folder, exist_ok=True)
    fig.savefig(filename, dpi=200)
