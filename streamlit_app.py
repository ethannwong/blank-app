import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.title("🎈 My Movielens dashboard")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

df=pd.read_csv("/workspaces/blank-app/movie_ratings.csv")
df.head()
genres=df["genres"].unique()
st.write("These are the genres")
st.write(genres)

st.write("These genres have the highest satisfaction ratings:")
st.write(df.groupby("genres")["rating"].mean())

st.write("This is a graph showing mean rating change over the years")
# st.line_chart(data=df,x="rating_year", y="rating")
df_genres = df.copy()
df_genres["genres"] = df_genres["genres"].str.split("|")
df_genres = df_genres.explode("genres")  # each genre gets its own row

# --- Group by rating_year and genre ---
avg_ratings_genre = (
    df_genres.groupby(["rating_year", "genres"])["rating"]
    .mean()
    .reset_index()
)


fig, ax = plt.subplots(figsize=(12, 6))

for genre, data in avg_ratings_genre.groupby("genres"):
    ax.plot(data["rating_year"], data["rating"], marker="o", label=genre)

ax.set_title("Average Rating Change Over Years by Genre", fontsize=16)
ax.set_xlabel("Rating Year", fontsize=12)
ax.set_ylabel("Average Rating", fontsize=12)
ax.legend(title="Genre", bbox_to_anchor=(1.05, 1), loc="upper left")
ax.grid(True)

# --- Show in Streamlit ---
st.pyplot(fig)

movie_stats = (
    df.groupby("movie_id")
    .agg(
        title=("title", "first"),
        n_ratings=("rating", "count"),
        avg_rating=("rating", "mean"),
    )
    .reset_index(drop=True)
)

top_5_50 = (
    movie_stats[movie_stats["n_ratings"] >= 50]
    .sort_values(by=["avg_rating", "n_ratings"], ascending=[False, False])
    .head(5)
)

# --- Top 5 movies with at least 150 ratings ---
top_5_150 = (
    movie_stats[movie_stats["n_ratings"] >= 150]
    .sort_values(by=["avg_rating", "n_ratings"], ascending=[False, False])
    .head(5)
)

st.write("5 best movies with 50 ratings:",top_5_50)
st.write("5 best movies with 150 ratings:",top_5_150)
