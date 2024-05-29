import streamlit as st
import plotly.express as px
import polars as pl
import duckdb
from duckdb import sql

st.title("Wowzers UwU")

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

data_load_state = st.text("Loading Data")
data = load_data(con)
data_load_state.text("Done! (using st.cache_data)")

stats = (
    data
    .select(pl.col("Attribute").unique())
    .to_series().to_list()
)
stats.sort()
stat = st.selectbox(
    label="Stat Filter $\\alpha = 52$", options=stats, index=stats.index("Power")
)
data = data.filter(pl.col("Attribute") == stat)

st.subheader("Scatterplot of character stats")
fig = px.scatter(
    data, x="BaseValue", y="GrowthValue", color="Name", symbol="CampaignID",
    labels={"GrowthValue": f"{stat} Growth (%)", "BaseValue": f"Base {stat} Value"},
    title=f"Sacred Stones {stat} Bases vs. Growth Scatterplot",
    hover_data=["Name"]
)
fig.update_traces(marker_size=7)
fig.update_layout(template="plotly_dark")

event = st.plotly_chart(fig, key="comp_bar", on_select="rerun")
st.dataframe(data)

event