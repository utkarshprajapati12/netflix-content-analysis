# Netflix Content Analysis

Interactive Streamlit dashboard analysing Netflix movies and TV shows.

**Tools:** Python, pandas, Streamlit

## What it shows
- Total titles, movies and TV shows (KPIs)
- Titles added to Netflix each year
- Top 10 countries and genres
- Movies vs TV shows by release year
- Average movie length
- Sidebar filters for type and release year

## Dataset
Download `netflix_titles.csv` from Kaggle ("Netflix Movies and TV Shows" by shivamb) and place it in the same folder as `app.py`.

## How to run
```bash
pip install -r requirements.txt
streamlit run app.py
```
The app opens in your browser at http://localhost:8501

## Project files
```
app.py              # cleaning, filters, charts
requirements.txt    # libraries needed
netflix_titles.csv  # dataset (download from Kaggle)
```
