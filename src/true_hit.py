import scipy
import statistics
import polars as pl
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
    df.write_csv("../data/cumulative_hit_rate_table.csv")


def create_xy_pmf_hit_table(filename: str, sum: bool = True):
    x = {"min": 0, "max": 99}
    z = {
        "min": 2 * x["min"],
        "max": 2 * x["max"]
    }

    data = {
        "joint_X_Y": [],
        "percent": []
    }
    pmf, all_outcomes = populate_pmf_and_outcomes(x, z)

    for i, outcomes in pmf.items():
        prob = len(outcomes) / len(all_outcomes)
        percent = round(prob * 100, 4)

        if sum:
            data["joint_X_Y"].append(int(i))
        else:
            data["joint_X_Y"].append(int(i) / 2)
        data["percent"].append(percent)

    pl.DataFrame(data).write_csv(filename)


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


def create_cdf_plots(data: pl.DataFrame, plot_type: str = "bar", cdf: bool = True):

    fig = go.Figure()

    parameters = {
        "title": "Displayed Hit Rate Vs. Actual Probability",
        "xaxis_title": "Displayed Hit Rate (%)",
        "yaxis_title": "Actual Hit Rate (%)",
        "xaxis_column": "Displayed Hit Rate",
        "yaxis_column_2rn": "True Hit Rate",
        "yaxis_column_1rn": "Displayed Hit Rate"
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


def create_pmf_plots(
        data: pl.DataFrame,
        uniform_data: pl.DataFrame,
        xaxis_title: str = ""
):

    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(
        go.Bar(x=data["joint_X_Y"], y=data["percent"], name="2RN"),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(x=uniform_data["hit_rate"], y=uniform_data["percent"], name="1RN"),
        row=2, col=1
    )
    fig.update_yaxes(range=[0, 1.5], title_text="Percent (%)")
    fig.update_xaxes(title_text=xaxis_title, row=1, col=1)
    fig.update_xaxes(title_text="X", row=2, col=1)
    fig.update_layout(title="Probability Mass Functions")
    return fig
