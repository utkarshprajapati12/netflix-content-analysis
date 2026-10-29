import pandas as pd
import streamlit as st

st.set_page_config(page_title="Netflix Content Analysis", layout="wide")


@st.cache_data
def load_data(path="netflix_titles.csv"):
    df = pd.read_csv(path)

    # Cleaning
    df = df.drop_duplicates()
    df["country"] = df["country"].fillna("Unknown")
    df["listed_in"] = df["listed_in"].fillna("Unknown")
    df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
    df["year_added"] = df["date_added"].dt.year

    # Use the first country and first genre listed for each title
    df["first_country"] = df["country"].str.split(",").str[0].str.strip()
    df["first_genre"] = df["listed_in"].str.split(",").str[0].str.strip()

    # Duration like "90 min" -> 90 (only for movies)
    df["minutes"] = df["duration"].str.extract(r"(\d+)")[0].astype(float)
    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error("netflix_titles.csv file nahi mili. Ise app.py ke same folder mein rakho.")
    st.stop()

st.title("Netflix Content Analysis")
st.caption("Dataset: Kaggle Netflix Movies and TV Shows (public dataset)")

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")
all_types = sorted(df["type"].dropna().unique())
selected_types = st.sidebar.multiselect("Type", all_types, default=all_types)

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())
year_range = st.sidebar.slider("Release year", min_year, max_year, (min_year, max_year))

filtered = df[
    df["type"].isin(selected_types)
    & df["release_year"].between(year_range[0], year_range[1])
]

if filtered.empty:
    st.warning("Is filter mein koi data nahi hai. Filters badal kar dekho.")
    st.stop()

# ---------- KPIs ----------
movies = filtered[filtered["type"] == "Movie"]
shows = filtered[filtered["type"] == "TV Show"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total titles", f"{len(filtered):,}")
c2.metric("Movies", f"{len(movies):,}")
c3.metric("TV Shows", f"{len(shows):,}")
c4.metric("Countries (first listed)", f"{filtered['first_country'].nunique():,}")

st.divider()

# ---------- Charts ----------
left, right = st.columns(2)

with left:
    st.subheader("Titles added to Netflix each year")
    per_year = (
        filtered.dropna(subset=["year_added"])
        .groupby("year_added")
        .size()
        .rename("titles")
    )
    st.line_chart(per_year)

with right:
    st.subheader("Top 10 countries by content")
    top_countries = (
        filtered[filtered["first_country"] != "Unknown"]["first_country"]
        .value_counts()
        .head(10)
    )
    st.bar_chart(top_countries)

left2, right2 = st.columns(2)

with left2:
    st.subheader("Top 10 genres")
    top_genres = filtered["first_genre"].value_counts().head(10)
    st.bar_chart(top_genres)

with right2:
    st.subheader("Movies vs TV Shows by release year")
    by_type = (
        filtered.groupby(["release_year", "type"])
        .size()
        .unstack(fill_value=0)
        .sort_index()
    )
    st.area_chart(by_type)

st.divider()

# ---------- Movie duration ----------
st.subheader("Movie duration")
avg_minutes = movies["minutes"].mean()
if pd.notna(avg_minutes):
    st.metric("Average movie length", f"{avg_minutes:.0f} min")

# ---------- Raw data ----------
with st.expander("Filtered data dekho"):
    st.dataframe(filtered, use_container_width=True)
