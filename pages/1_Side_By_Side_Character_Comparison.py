import streamlit as st
import plotly.express as px
import polars as pl
import duckdb
from duckdb import sql

st.set_page_config(
    page_title="Character Comparison",
    page_icon="🗡"
)
st.write(
    """
    # Character Stat Comparisons
    
    On this page you can select up to 3 characters to compare stats directly!
    """
)

path = "data/duckdb/db.duckdb"
con = duckdb.connect(path, read_only=True)

def load_data(con, table: str):

    return con.sql(
        f"""
        SELECT *
        FROM {table}
        """
    ).pl()

# data_load_state = st.text("Loading Data")
characters = load_data(con, "characters")
# data_load_state.text("Data Loaded!")

names = (
    characters
    .select(pl.col("Name").unique())
    .to_series().to_list()
)
names.sort()
char_select = st.multiselect(
    label="Select Characters", options=names,
    default=["Eirika", "Ephraim"], max_selections=3,
    placeholder="Choose up to 3 Characters"
)

# ----- [Base Stat Section] -----
bases = load_data(con, "baseswide")
bases = bases.filter(pl.col("Name").is_in(char_select))

# st.dataframe(bases)

bases_long = bases.melt(id_vars=["Name", "CampaignID"])
base_fig = px.bar(
    bases_long, y="variable", x="value", color="Name", barmode="group",
    labels={"value": "Base Value", "variable": ""}#, title="Base Stat Value Comparison"
)

# event = st.plotly_chart(fig, key="comp_bar_bases", on_select="rerun")

# event

# ----- [Growths Rate Section] -----
growths = load_data(con, "growthswide")
growths = growths.filter(pl.col("Name").is_in(char_select))

# st.dataframe(growths)

growths_long = growths.melt(id_vars=["Name", "Game"])
growth_fig = px.bar(
    growths_long, y="variable", x="value", color="Name", barmode="group",
    labels={"value": "Growth Rate (%)", "variable": ""}#, title="Growth Rate Value Comparison"
)


# Show tabs for both plots and tables
# base_event = st.plotly_chart(fig, key="comp_bar_bases", on_select="rerun")
# growth_event = st.plotly_chart(fig, key="comp_bar_growths", on_select="rerun")

base_tab, growth_tab = st.tabs(["Bases", "Growths"])
with base_tab:
    st.dataframe(bases)
    st.plotly_chart(base_fig, key="comp_bar_bases", on_select="rerun")
with growth_tab:
    st.dataframe(growths)
    st.plotly_chart(growth_fig, key="comp_bar_growths", on_select="rerun")
