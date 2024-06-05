import streamlit as st
from src.true_hit import displayed_to_true_hit, create_cdf_plots, create_pmf_plots
import polars as pl
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
table = pl.read_csv("data/true_hit_data/cumulative_hit_rate_table.csv")
table = table.rename({"displayed": "Displayed Hit Rate", "true": "True Hit Rate"})
st.dataframe(table, use_container_width=True)

st.markdown(
    """
    ## Info and Background
    This page is for converting from the hit rates the game displays to the genuine hit rates going on under the hood.

    Let's examine a basic battle forecast shall we?
    """
)

st.image("images/fe6_battle_forecast.png", caption="Source: Mekkah - FE6 HM Iron Man - Part 4")

st.markdown(
    """
    Here we've got a fight between Rutger and a boss named Henning.
    
    According to the battle forecast our boy Rutger here has a displayed hit of 70. Intuitively you'd think
    that means he has a 70% chance to hit right?

    However, the GBA Fire Emblem games use what's called a 2RN system. They actually roll two different dice and
    take their average. This changes the math a lot. Rutger really has a *true hit rate* of 82.3% because of this.
    Really, all you need to know is that the further from 50 a displayed hit gets, the more off the real chance is.
    Hit rates well above 50 hit more than they should and hit rates below 50 a whole lot less.

    My calculator is there to save you time on figuring out what the real values are.
    
    ## Why do the games do this?
    
    People are, almost by nature, extremely bad at gauging probability. This is compounded with a game like
    Fire Emblem where that thing we're bad at is directly tied into formulating strategies and assessing risk.
    Going for a $95\%$ chance to hit feels like an extremely safe move right? However, in the old FE games
    there's a $1/20$ chance you miss. That's honestly very likely over a gaming session and, for most players,
    this feels bad. Same with getting hit by a $20\%$. $1/5$ of those will land but strategically it *feels*
    like it should be a reliable play. 
    
    The 2RN system is there to make probabilities feel like they *should feel*. An $85\%$ feels like it should be pretty
    reliable and so it's been cranked up to around $95\%$. It's also in the players favor! Most of the time
    the player will be working with hit rates above $50\%$ so the player benefits from the boost. Meanwhile the enemies will
    often be below $50\%$ and taking a penalty. 
    
    Whether you like this system or not is up to preference. Personally I enjoy the punishing nature of the brutally honest
    1RN system, but there's a reason 2RN exists. It's honestly very clever!
    """
)

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

    The true hit resources I've found online never really dive into the math because it can get a little complicated.
    However, I think it's actually really fun to understand what's going on under the hood and I want to provide that to anyone interested!
    
    In the section below we properly dive into the topic and I hope it helps provide some insight into these games.
    This is gonna be a long one so I apologize in advance!
    
    ### Disclaimer
    
    This is a mathematical explanation but I want to keep it easy to understand for everyone. 
    There may be some jargon here or there but I will be sure to explain all of it and I expect no mathematical background coming into this.
    There's a lot of text though so be prepared to read.
    """
)

math = st.toggle("View the Mathematical Explanation")

if math:
    with open("markdown_files/true_hit_explanation.md") as f:
        explanation = f.read()

    with open("markdown_files/true_hit_explanation_pt2.md") as f:
        explanation_pt2 = f.read()

    st.markdown(explanation)

    # PMF Plots

    uniform_data = pl.read_csv("data/true_hit_data/uniform_data.csv")
    sum_tab, average_tab = st.tabs(["Sum: $X+Y$", "Average: $\\frac{X+Y}{2}$"])
    with sum_tab:
        data = pl.read_csv("data/true_hit_data/sum_pmf.csv")
        fig = create_pmf_plots(data, uniform_data, xaxis_title="X+Y")
        st.write(fig)

    with average_tab:
        data = pl.read_csv("data/true_hit_data/avg_pmf.csv")
        fig = create_pmf_plots(data, uniform_data, xaxis_title="(X+Y)/2")
        st.write(fig)

    st.markdown(
        """
        The ranges on this plot might initially be a bit confusing. Why is it going from $[0,198]$ with the sum????
        Remember, each dice goes from $[0,99]$, so our max value is $99+99 = 198$. 
        You'll also notice how the average one looks identical outside of the x axis being on a different range.
        That'll be useful for us later!
        """
    )

    st.markdown(explanation_pt2)

    # CDF Plots
    bar_tab, line_tab = st.tabs(["Bar Plot", "Line Plot"])
    with bar_tab:
        fig = create_cdf_plots(table, plot_type="bar")
        st.write(fig)

    with line_tab:
        fig = create_cdf_plots(table,plot_type="line")
        st.write(fig)

