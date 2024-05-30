import streamlit as st
import plotly.express as px
import polars as pl
import duckdb

# General page info
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

# Duckdb connection and data loading
path = "data/duckdb/db.duckdb"
con = duckdb.connect(path, read_only=True)


def load_data(con, table: str):

    if table == "baseswide":
        return con.sql(
            f"""
            SELECT
                {table}.name
                , {table}.hp
                , {table}.power
                , {table}.skill
                , {table}.speed
                , {table}.luck
                , {table}.defense
                , {table}.resistance
                , c.campaign
            FROM {table}
            LEFT JOIN campaigns c
            ON {table}.campaignid = c.id
            """
        ).pl()

    return con.sql(f"SELECT * FROM {table}").pl()


# Setup character selection for filtering
characters = load_data(con, "characters")

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

# Create tabs for bases and growths and plots/tables for each.
base_tab, growth_tab = st.tabs(["Bases", "Growths"])
with base_tab:
    bases = load_data(con, "baseswide")
    bases = bases.filter(pl.col("Name").is_in(char_select))

    bases_long = bases.melt(id_vars=["Name", "Campaign"])
    base_fig = px.bar(
        bases_long, y="variable", x="value", color="Name", barmode="group",
        labels={"value": "Base Value", "variable": ""}
    )
    st.dataframe(bases)
    st.plotly_chart(base_fig, key="comp_bar_bases", on_select="rerun")

with growth_tab:
    growths = load_data(con, "growthswide")
    growths = (
        growths
        .filter(pl.col("Name").is_in(char_select))
        .drop("Game")
    )

    growths_long = growths.melt(id_vars=["Name"])
    growth_fig = px.bar(
        growths_long, y="variable", x="value", color="Name", barmode="group",
        labels={"value": "Growth Rate (%)", "variable": ""}
    )

    st.dataframe(growths)
    st.plotly_chart(growth_fig, key="comp_bar_growths", on_select="rerun")
