import streamlit as st
import plotly.express as px
import polars as pl
import duckdb
from duckdb import sql

# Page Config and Writeup
st.set_page_config(
    page_title="Stat Distribution Plots",
    page_icon="🗡"
)
st.write(
    """
    # Game Wide Stat Plots

    This page allows you to see the distribution for specific stats across the entire cast of character!
    
    Curious how a specific character stacks up against everyone else? This page is to help you get a high level overview of exactly that!
    """
)

path = "data/duckdb/db.duckdb"
con = duckdb.connect(path, read_only=True)

def load_data(con):

    return con.sql(
        f"""
        SELECT 
            s.name
            , s.attribute
            , s.basevalue
            , s.growthvalue
            , b.campaignid
        FROM statscombined s
        LEFT JOIN baseswide b
        ON s.name = b.name
        """
    ).pl()

data = load_data(con)

stats = (
    data
    .select(pl.col("Attribute").unique())
    .to_series().to_list()
)
stats.sort()
stat = st.selectbox(
    label="Stat Selection", options=stats, index=stats.index("Power")
)
data = data.filter(pl.col("Attribute") == stat)

st.subheader("Scatterplot of character stats")
fig = px.scatter(
    data, x="BaseValue", y="GrowthValue", color="Name", symbol="CampaignID",
    labels={"GrowthValue": f"{stat} Growth (%)", "BaseValue": f"Base {stat} Value"},
    title=f"{stat} Bases vs. Growth"
)
fig.update_traces(marker_size=7)
fig.update_layout(showlegend=False)

event = st.plotly_chart(fig, key="stat_scatter", on_select="rerun")
st.dataframe(data)

st.write(event)

