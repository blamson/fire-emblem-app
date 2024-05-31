import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import polars as pl
import duckdb

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
            , c.campaign
        FROM statscombined s
        LEFT JOIN baseswide b
        ON s.name = b.name
        LEFT JOIN campaigns c
        on b.campaignid = c.id
        """
    ).pl()

data = load_data(con)

characters = con.sql("select * from characters").pl()
names = (
    characters
    .select(pl.col("Name").unique())
    .to_series()
    .to_list()
)
names.sort()

st.subheader("Scatterplot of Character Stats")

stats = (
    data
    .select(pl.col("Attribute").unique())
    .to_series().to_list()
)
stats.sort()
stat = st.selectbox(
    label="Select a stat to plot",
    options=stats,
    index=stats.index("Power"),
    placeholder="Select a Stat to Plot"
)
data = (data.filter(pl.col("Attribute") == stat))

char_select = st.selectbox(
    label="Select character to highlight on the plot", options=names,
    index=names.index("Eirika"),
    placeholder="Select a Character to Highlight"
)

fig = px.scatter(
    data, x="BaseValue", y="GrowthValue", symbol="Campaign", color="Name",
    labels={"GrowthValue": f"{stat} Growth (%)", "BaseValue": f"Base {stat} Value"},
    title=f"{stat} Bases vs. Growth",
    color_discrete_sequence=px.colors.qualitative.Plotly,
    custom_data=["Name", "Campaign"]
)
# st.write("plotly express hovertemplate:", fig.data[0].hovertemplate)
fig.update_traces(
    marker_size=10,
    hovertemplate='''
        <br>Base: %{x} 
        <br>Growth: %{y}
    '''
)
fig.update_layout(showlegend=False, hovermode='x unified')

# Add x to specified character
char_row = data.filter(pl.col("Name") == char_select)

fig.add_trace(go.Scatter(
    x=char_row["BaseValue"], y=char_row["GrowthValue"],
    mode='markers',
    marker=dict(size=17, color='red', symbol='x'),
    hoverinfo='none'
))

st.plotly_chart(fig, key="stat_scatter", on_select="rerun")
st.dataframe(char_row, use_container_width=True)
