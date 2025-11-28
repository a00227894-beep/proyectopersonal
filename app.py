
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Color

# Estilos CSS personalizados
st.markdown("""
<style>
/* Estilo del Sidebar */
[data-testid="stSidebar"] {
background-color: #3054BF;
}
/* Estilo de los textos del Sidebar */
[data-testid="stSidebar"] * {
color: white !important;
}
/* Color de fondo para la barra superior que esta arriba de la pagina
principal */
div[data-testid="stToolbar"] {
background-color: #cfcfcf;
}
/* Estilo de la página principal */
.main {
background-color: #cfcfcf;
}
/* Todo el texto de la página principal será en blanco */
.main * {
color: white !important;
}
/* Estilo de las métricas */
[data-testid="stMetricValue"] {
color: white !important;
}
/* Estilo de las etiquetas de las métricas */
[data-testid="stMetricLabel"] {
color: #172140 !important;
}
/* Encabezados */
h1, h2, h3, h4, h5, h6 {
color: #033866 !important;
}
/* Estilo del Selectbox */
.stSelectbox label {
color: white !important;
}
/* Estilo de la sección principal */
.stApp {
background-color:#cfcfcf;
}
</style>
""", unsafe_allow_html=True)

# Configuración de la página
st.set_page_config(page_title="2024 LoL Championship Player Stats & Swiss Stage", layout="wide",
  initial_sidebar_state="expanded")
# Título principal
st.title("Dashboard - 2024 LoL Championship Player Stats & Swiss Stage")

# Cargar datos con caché
@st.cache_data
def load_data():
  lol = pd.read_csv('player_statistics_cleaned_final.csv', encoding='latin-1')
  return lol

# Cargar datos
try:
  lol = load_data()
  st.badge(f"Data uploaded: {len(lol)} ",
  icon=":material/check:", color="green")
except Exception as e:
  st.error(f"Error uploading data: {e}")
  st.stop()

# Sidebar filters
st.sidebar.header("Filters")

  #1
team_select_filter = st.sidebar.multiselect("Select Team: ", lol["TeamName"].unique(), default= lol["TeamName"].unique())

  #2
win_rate_min_val = float(lol["Win rate"].min())
win_rate_max_val = float(lol["Win rate"].max())
win_rate_slider = st.sidebar.slider("Select Win Rate: ", win_rate_min_val, win_rate_max_val, (win_rate_min_val, win_rate_max_val))

  #3
if "Country" in lol.columns:
    countries = st.sidebar.multiselect(
        "Country",
        options=sorted(lol["Country"].dropna().unique()),
        default= lol["Country"].dropna().unique()
    )
else:
    countries = []

filtered_lol_df = lol[(lol["TeamName"].isin(team_select_filter)) & (lol["Win rate"].between(win_rate_slider[0], win_rate_slider[1])) & (lol["Country"].isin(countries)) ]

# Check filters
if filtered_lol_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# Metrics
st.header('Most important Metrics')
met_col1, met_col2, met_col3, met_col4, met_col5 = st.columns(5)

with met_col1:
  total_avgk = filtered_lol_df['Avg kills'].mean()
  st.metric('Avg kills', f'{total_avgk:,.2f}')

with met_col2:
  total_avgd = filtered_lol_df['Avg deaths'].mean()
  st.metric('Avg deaths', f'{total_avgd:,.2f}')

with met_col3:
  total_avga = filtered_lol_df['Avg assists'].mean()
  st.metric('Avg assists', f'{total_avga:,.2f}')

with met_col4:
  total_avgt = filtered_lol_df['TeamName'].nunique()
  st.metric('Teams', f'{total_avgt:,}')

with met_col5:
  total_avgw = filtered_lol_df['Win rate'].mean() * 100
  st.metric('Avg Win rate %', f'{total_avgw:,.1f}%')

# Columns definition
def get_column_definitions() -> pd.DataFrame:
    data = [
        {
            "Column": "TeamName",
            "Description": "The player’s team (e.g., Top Esports, Dplus KIA).",
            "Type": "string",
        },
        {
            "Column": "PlayerName",
            "Description": "The player’s in-game name.",
            "Type": "string",
        },
        {
            "Column": "Games",
            "Description": "Total games played.",
            "Type": "integer",
        },
        {
            "Column": "Win Rate",
            "Description": "Player’s win rate in percentage.",
            "Type": "float (percentage)",
        },
        {
            "Column": "KDA",
            "Description": "Kill-Death-Assist ratio, indicating performance balance.",
            "Type": "float",
        },
        {
            "Column": "Avg Kills",
            "Description": "Average kills per game.",
            "Type": "float",
        },
        {
            "Column": "Avg Deaths",
            "Description": "Average deaths per game.",
            "Type": "float",
        },
        {
            "Column": "Avg Assists",
            "Description": "Average assists per game.",
            "Type": "float",
        },
        {
            "Column": "CSM",
            "Description": "Creep Score per Minute: average minions/creeps killed per minute.",
            "Type": "float",
        },
        {
            "Column": "GPM",
            "Description": "Gold Per Minute: average gold earned per minute.",
            "Type": "float",
        },
        {
            "Column": "KP%",
            "Description": "Kill Participation: percentage of team kills in which the player participated.",
            "Type": "float (percentage)",
        },
        {
            "Column": "DMG%",
            "Description": "Damage Percentage: percentage of team damage dealt by the player.",
            "Type": "float (percentage)",
        },
        {
            "Column": "DPM",
            "Description": "Damage Per Minute: average damage dealt per minute.",
            "Type": "float",
        },
        {
            "Column": "VSPM",
            "Description": "Vision Score Per Minute: vision score representing map awareness, calculated per minute.",
            "Type": "float",
        },
        {
            "Column": "Avg WPM",
            "Description": "Average number of wards placed per minute.",
            "Type": "float",
        },
        {
            "Column": "Avg WCPM",
            "Description": "Average number of enemy wards cleared per minute.",
            "Type": "float",
        },
        {
            "Column": "Avg VWPM",
            "Description": "Average number of vision wards placed per minute.",
            "Type": "float",
        },
        {
            "Column": "GD@15",
            "Description": "Gold Differential at 15 minutes: gold advantage or disadvantage at 15 minutes.",
            "Type": "float",
        },
        {
            "Column": "CSD@15",
            "Description": "Creep Score Differential at 15 minutes: creep score advantage or disadvantage at 15 minutes.",
            "Type": "float",
        },
        {
            "Column": "XPD@15",
            "Description": "Experience Differential at 15 minutes: XP advantage or disadvantage at 15 minutes.",
            "Type": "float",
        },
        {
            "Column": "FB %",
            "Description": "First Blood Percentage: percentage chance of achieving first blood in a match.",
            "Type": "float (percentage)",
        },
        {
            "Column": "FB Victim",
            "Description": "Percentage chance of the player being the victim of first blood.",
            "Type": "float (percentage)",
        },
        {
            "Column": "Penta Kills",
            "Description": "Number of pentakills (five kills in quick succession) by the player.",
            "Type": "integer",
        },
        {
            "Column": "Solo Kills",
            "Description": "Number of solo kills by the player.",
            "Type": "integer",
        },
        {
            "Column": "Country",
            "Description": "Player's region or country of representation.",
            "Type": "string",
        },
        {
            "Column": "FlashKeybind",
            "Description": "Flash key preference for the player (D or F).",
            "Type": "string (categorical)",
        },
    ]

    return pd.DataFrame(data, columns=["Column", "Description", "Type"])

# Tabs
tab4, tab0, tab1, tab2, tab3 = st.tabs(['Column Definitions', 'EDA', 'Team Data', 'Team Combat Analysis', 'Performance Evolution'])

with tab4:
    st.subheader("Column Definitions")
    df_columns = get_column_definitions()
    st.dataframe(df_columns, use_container_width=True)

with tab0:
    st.subheader("Filtered Data Overview")
    st.dataframe(filtered_lol_df.head())
    st.title("Dataframe Describe: ")
    st.dataframe(filtered_lol_df.describe())
    st.title("Dataframe Dtypes: ")
    st.write(filtered_lol_df.dtypes)

    st.title("KDA vs Win Rate: ")

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.scatterplot(x="Win rate", y="KDA", data=filtered_lol_df, color="red", ax=ax)
    sns.regplot(x="Win rate", y="KDA", data=filtered_lol_df, scatter=False, color="blue", ax=ax)
    st.pyplot(fig)
    plt.close(fig)

with tab1:
#1st graph
  st.subheader("Team Data")

  gra1_col1, gra1_col2 = st.columns(2)

  with gra1_col1:
      group_col = st.selectbox('Group by: ', ['TeamName', 'PlayerName', 'Position'], key='tab1_group_col')
  with gra1_col2:
      metric_col = st.selectbox('Metric: ', ['KDA', 'GoldPerMin'], key='tab1_metric_col')

  grouped = (
      filtered_lol_df
      .groupby(group_col, as_index=False)[metric_col]
      .mean()
  )

  top_m = grouped.nlargest(10, metric_col)
  fig = px.bar(
      top_m,
      x=group_col,
      y=metric_col,
      color=group_col,
      title=f"Top 10 {group_col} by {metric_col}",
      text=metric_col,
  )

  fig.update_traces(
      texttemplate='%{text:.2f}',
      textposition='outside',
      width=0.8
  )

  fig.update_layout(
      bargap=0.05,
      xaxis_title=group_col,
      yaxis_title=metric_col
  )

  st.plotly_chart(fig, use_container_width=True)

with tab2:

#2nd graph
  st.subheader("Team Combat Analysis")

  gra2_col1, gra2_col2 = st.columns(2)

  with gra2_col1:
      top_n_teams = st.slider("Select top N teams to show", 3, 20, 10, key='tab2_top_n_teams')
  with gra2_col2:
      team_metric = st.selectbox(
          "Order by",
          ["Avg kills", "Avg deaths", "Avg assists", "KDA", "GoldPerMin", "DamagePercent", "DPM", "XPD@15", "Win rate"],
          key='tab2_team_metric'
      )

  df_teams = (
      filtered_lol_df.groupby("TeamName").agg({
          "Avg kills": "mean",
          "Avg deaths": "mean",
          "Avg assists": "mean",
          "KDA": "mean",
          "GoldPerMin": "mean",
          "DamagePercent": "mean",
          "DPM": "mean",
          "XPD@15": "mean",
          "Win rate": "mean"
      })
      .reset_index()
      .sort_values(team_metric, ascending=False)
      .head(top_n_teams)
  )

  fig_teams = px.bar(
      df_teams,
      y="TeamName",
      x=team_metric,
      orientation="h",
      title=f"Top {top_n_teams} Teams by {team_metric}",
      color=team_metric,
      color_continuous_scale="Sunset"
  )

  fig_teams.update_layout(
      yaxis={'categoryorder': 'total ascending'},
      xaxis_title=team_metric,
      yaxis_title="Team"
  )

  st.plotly_chart(fig_teams, use_container_width=True)

with tab3:
#3rd graph
  st.subheader("Performance Evolution by Role / Team")

  gra1_col1, gra1_col2 = st.columns(2)

  with gra1_col1:
      group_dim = st.selectbox(
          "Group by",
          ["TeamName", "Position"],
          key='tab3_group_dim'
      )
  with gra1_col2:
      metric_type = st.selectbox(
          "Select the KPI",
          ["Avg kills", "Avg deaths", "Avg assists", "Win rate"],
          key='tab3_metric_type'
      )

  df_time = (
      filtered_lol_df.groupby(group_dim).agg({
          "Avg kills": "mean",
          "Avg deaths": "mean",
          "Avg assists": "mean",
          "Win rate": "mean"
      })
      .reset_index()
      .sort_values(metric_type, ascending=False)
  )

  fig_time = px.line(
      df_time,
      x=group_dim,
      y=metric_type,
      title=f"Performance of {metric_type} by {group_dim}",
      markers=True
  )

  fig_time.update_traces(line_color='#1f77b4', line_width=3)
  fig_time.update_layout(hovermode='x unified')

  st.plotly_chart(fig_time, use_container_width=True)
