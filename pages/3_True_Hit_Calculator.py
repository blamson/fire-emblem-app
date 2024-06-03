import streamlit as st
from scipy.stats import randint
from statistics import mean
from math import sqrt
from src.true_hit import displayed_to_true_hit
import polars as pl


# Page Config and Writeup
st.set_page_config(
    page_title="True Hit Calculator",
    page_icon="🗡"
)

st.markdown(
    """
    # True Hit Calculator
    """
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
    true_hit = displayed_to_true_hit(displayed_hit)
    st.markdown(
        f"""
        |Displayed Hit|True Hit|
        |---|---|
        |{displayed_hit}|{true_hit}|
        """
    )

st.markdown('## Hit Rate Table')
table = pl.read_csv("data/hit_rate_table.csv")
table = table.rename({"displayed": "Displayed Hit Rate", "true": "True Hit Rate"})
st.dataframe(table, use_container_width=True)

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

st.markdown(
    """
    ## Resources
    Serenes Forest, as always, helped a lot. I use their tables as a reference for troubleshooting. 
    [Link](https://serenesforest.net/general/true-hit/)
    """
)

# st.markdown(
#     """
#     ## Mathematical Explanation
#
#     The true hit resources I've found online never really dive into the math because it can get a little complicated.
#     However,
#     In this section I'll solve this little probability problem and show you how to compute this yourself!
#
#     ###
#     """
# )

st.markdown(
    """
    ## Mathematical Explanation

    The true hit resources I've found online never really dive into the math because it can get a little complicated.
    However, I think it's actually really fun to understand what's going on under the hood and I want to provide that to anyone interested!
    
    In this section I'll solve this little probability problem and help you gain some insight into the world of probability!
    
    This is gonna be a long one so I apologize in advance!
    
    ### Disclaimer
    
    This is a mathematical explanation but I want to keep it easy to understand for everyone. 
    There may be some jargon here or there but I will be sure to explain all of it and I expect no mathematical background coming into this.
    """
)

st.warning(
    '''
    Mathematical explanation still in progress. Might be a little dense currently.
    ''',
    icon="🚧️"
)

math = st.toggle("View the Mathematical Explanation")
if math:
    with open("markdown_files/true_hit_explanation.md") as f:
        explanation = f.read()

    st.markdown(explanation)
