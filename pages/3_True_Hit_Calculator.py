import streamlit as st
from scipy.stats import randint
from statistics import mean
from math import sqrt
from src.true_hit import true_hit_simulation, true_hit_solution
import polars as pl


# Page Config and Writeup
st.set_page_config(
    page_title="True Hit Calculator",
    page_icon="🗡"
)

st.markdown("# True Hit Calculator")

st.warning(
    '''
    This feature is a proof of concept. The math isn't quite sorted out yet. 
    
    Hit Rates < 50 are solid, but Hit Rates >= 50 are off.
    ''',
    icon="⚠️"
)

displayed_hit = st.number_input(
    label="Enter your displayed hit. This number should be a positive value between 0 and 100.",
    min_value=0,
    max_value=100,
    value=None,
    placeholder="Enter a value between 0 and 100."
)

# Second condition required because displayed_hit evals to False when user inputs 0.
if displayed_hit or (displayed_hit == 0):
    # true_hit = round(true_hit_simulation(displayed_hit, 0, 99) * 100, 2)
    true_hit = round(true_hit_solution(displayed_hit) * 100, 2)

    st.markdown(
        f"""
        |Displayed Hit|True Hit|
        |---|---|
        |{displayed_hit}|{true_hit}|
        """
    )

st.markdown(
    """
    ## Info
    This page is for converting from the hit rates the game displays to the genuine hit rates going on under the hood.

    Intuitively you'd think a hit rate of, say, 75, means that the game rolls a 100 sided die and 
    so 75 of those rolls mean we hit and 25 of them miss. 

    However, the GBA Fire Emblem games use what's called a 2RN system. They actually roll two different dice and
    take their average. This changes the math a lot. All you need to know is that the further away from 50 the 
    displayed hit rate gets, the more extreme the real value is. High hit rates hit more than they should and
    low hit rates hit less.

    My calculator is there to save you time on figuring out what the real values are.
    """
)

st.markdown("# Hit Rate Table")
table = pl.read_csv("data/hit_rate_table.csv")
st.dataframe(table)

st.markdown(
    """
    ## Resources
    Serenes Forest, as always, helped a lot. I use their tables as a reference for troubleshooting. 
    [Link](https://serenesforest.net/general/true-hit/)
    """
)

st.markdown(
    """
    ## Mathematical Explanation
    
    The true hit resources I've found online never really dive into the math because it gets very ugly.
    In this section I'll solve this little probability problem and show you how to compute this yourself!
    """
)

st.warning(
    '''
    Mathematical explanation still in progress.
    ''',
    icon="🚧️"
)