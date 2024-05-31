import scipy
import statistics

def true_hit_simulation(hit_rate, lower, upper):
    """
    Brute force simulation. Slow but fantastic for sanity checking new mathematical solutions.
    It's never exactly right, but its accurate enough.
    """

    successes = []
    trials = 10000
    for i in range(trials):
        uni_rvs = scipy.stats.randint(lower, upper + 1).rvs(2)
        sample_mean = statistics.mean(uni_rvs)

        if sample_mean < hit_rate:
            successes.append(1)
        else:
            successes.append(0)

    return sum(successes) / trials


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


# Tinkering with everything
displayed_hit = 50
hit = true_hit_simulation(displayed_hit, 0, 99)
print(hit)

hit = true_hit_solution(displayed_hit)
print(hit)
