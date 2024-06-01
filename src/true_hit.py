import scipy
import statistics
import numpy as np
import polars as pl
from scipy.stats import triang


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


def true_hit_solution(hit_rate):
    """
    Magic number hell I hate this. :(
    Will be a lot cleaner once I work out the math myself.
    """

    denominator = 9801
    if 0 <= hit_rate <= 49.5:
        return (
            (2 * hit_rate**2) / denominator
        )

    elif 49.5 < hit_rate <= 99:
        numerator = (396*hit_rate) - (2*(hit_rate**2)) - 14601.5
        return 0.5 + (numerator / denominator)

    elif hit_rate > 99:
        return 1

def create_true_hit_table():
    data = {
        "displayed": [],
        "true": []
    }
    for i in range(0, 100 + 1, 1):
        data["displayed"].append(i)
        true = true_hit_solution(i) * 100
        data["true"].append(round(true, 2))

    print(data)
    df = pl.DataFrame(data)
    df.write_csv("../data/hit_rate_table.csv")


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


def true_hit_with_scipy(x):
    if x == 100:
        return 1
    else:
        lower = 0
        upper = 99
        mode = (upper - lower) / 2
        c = (mode - lower) / (upper - lower)
        rv = triang(c, loc=lower, scale=upper - lower)
        return rv.cdf(x)
