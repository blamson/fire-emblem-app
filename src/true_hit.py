import scipy
import statistics
import numpy as np
import polars as pl
import plotly.graph_objects as go
from scipy.stats import triang
import streamlit as st


def true_hit_simulation(hit_rate, lower=0, upper=99, ntrials=10000):
    """
    Brute force simulation. Slow but fantastic for sanity checking new mathematical solutions.
    It's never exactly right, but its accurate enough.
    """

    successes = []
    for i in range(ntrials):
        uni_rvs = scipy.stats.randint(lower, upper + 1).rvs(2)
        sample_mean = statistics.mean(uni_rvs)

        if sample_mean < hit_rate:
            successes.append(1)
        else:
            successes.append(0)

    return sum(successes) / ntrials


def create_cdf_hit_table():
    data = {
        "displayed": [],
        "true": []
    }
    for i in range(0, 100 + 1, 1):
        data["displayed"].append(i)
        true = displayed_to_true_hit(i)
        data["true"].append(true)

    print(data)
    df = pl.DataFrame(data)
    df.write_csv("../data/hit_rate_table.csv")


def create_pmf_hit_table():
    data = {
        "hit_rate": [],
        "2rn": []
    }

    for i in range(0, 100 + 1, 1):
        data["hit_rate"].append(i)
        cdf_i = displayed_to_true_hit(i)
        if i == 0:
            data["2rn"].append(cdf_i)
            continue

        cdf_prev_i = displayed_to_true_hit(i-1)
        prob = round(cdf_i - cdf_prev_i, 2)
        data["2rn"].append(prob)

    df = pl.DataFrame(data)
    df.write_csv("../data/hit_rate_pmf_table.csv")


def create_simulated_hit_rate_table():
    aggregated_hit_rates = {
        "DisplayedHit": [],
        "TrueHit": []
    }
    for displayed_hit in range(0, 100+1, 1):
        print(f"Simulating Displayed Hit = {displayed_hit}")
        simulated_true_hit = round(true_hit_simulation(hit_rate=displayed_hit, ntrials=100000) * 100, 2)
        aggregated_hit_rates["DisplayedHit"].append(displayed_hit)
        aggregated_hit_rates["TrueHit"].append(simulated_true_hit)

    df = pl.DataFrame(aggregated_hit_rates)
    df.write_csv("../data/simulated_hit_rate_table.csv")


# All functions below this comment are for use in tandem with one another
# These functions are for the correct discrete solution
def sum_to_n(n, x: dict, z: dict):
    combinations = []
    if not (z["min"] <= n <= z["max"]):
        return
    for a in range(x["min"], x["max"]+1):
        b = n - a
        if x["min"] <= b <= x["max"]:
            combinations.append((a, b))

    return combinations


def populate_pmf_and_outcomes(x: dict, z: dict):

    pmf = {}
    all_outcomes = []
    n = 0
    while n <= (z["max"]):

        outcomes = sum_to_n(n, x, z)
        if outcomes:
            pmf[str(n)] = outcomes
            all_outcomes += outcomes
        n += 1

    return pmf, all_outcomes


def calculate_cdf(pmf: dict, all_outcomes: list, c: int = 50):
    cdf = 0
    for i in range((2 * c)):
        outcomes = pmf[str(i)]
        prob = len(outcomes) / len(all_outcomes)
        cdf += prob

    return cdf


def displayed_to_true_hit(displayed_hit: int):
    if displayed_hit == 100:
        return 100

    x = {"min": 0, "max": 99}
    z = {
        "min": 2 * x["min"],
        "max": 2 * x["max"]
    }

    pmf, all_outcomes = populate_pmf_and_outcomes(x, z)

    cdf = calculate_cdf(pmf, all_outcomes, c=displayed_hit)
    cdf = round(cdf * 100, 2)

    return cdf


def create_plots(data: pl.DataFrame, plot_type: str = "bar", cdf: bool = True):

    fig = go.Figure()

    if cdf:
        parameters = {
            "title": "Displayed Hit Rate Vs. Actual Probability",
            "xaxis_title": "Displayed Hit Rate (%)",
            "yaxis_title": "Actual Hit Rate (%)",
            "xaxis_column": "Displayed Hit Rate",
            "yaxis_column_2rn": "True Hit Rate",
            "yaxis_column_1rn": "Displayed Hit Rate"
        }

    else:
        parameters = {
            "title": "1RN vs. 2RN Probability Mass Functions",
            "xaxis_title": "Hit Rate (%)",
            "yaxis_title": "Percent Chance (%)",
            "xaxis_column": "hit_rate",
            "yaxis_column_2rn": "2rn",
            "yaxis_column_1rn": "1rn"
        }

    if plot_type == "line":
        fig.add_trace(go.Scatter(
            x=data[parameters["xaxis_column"]], y=data[parameters["yaxis_column_2rn"]], mode="lines", name="2RN"
        ))
        fig.add_trace(go.Scatter(
            x=data[parameters["xaxis_column"]], y=data[parameters["yaxis_column_1rn"]], mode="lines", name="1RN"
        ))
    else:
        fig.add_trace(go.Bar(
            x=data[parameters["xaxis_column"]], y=data[parameters["yaxis_column_2rn"]], name="2RN"
        ))
        fig.add_trace(go.Bar(
            x=data[parameters["xaxis_column"]], y=data[parameters["yaxis_column_1rn"]], name="1RN"
        ))

    fig.update_layout(
        hovermode="x unified",
        title=parameters["title"],
        xaxis_title=parameters["xaxis_title"],
        yaxis_title=parameters["yaxis_title"]
    )

    return fig
