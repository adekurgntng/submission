import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_dataset(df):
    dataset = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    dataset = dataset.reset_index()
    return dataset

def create_year_rentals(df):
    year_rentals = df.groupby(by="yr")["cnt"].sum().reset_index()
    year_rentals["yr_label"] = year_rentals["yr"].map({0: 2011, 1: 2012})
    return year_rentals

def create_month_rentals(df):
    month_rentals = df.groupby(by=["yr", "mnth"])["cnt"].sum().reset_index()
    month_rentals["yr_label"] = month_rentals["yr"].map({0: 2011, 1: 2012})
    month_rentals["mnth_label"] = month_rentals["mnth"].map({
    1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni',
    7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    })
    return month_rentals

def create_season_rentals(df):
    season_rentals = df.groupby(by="season").cnt.sum().reset_index()
    season_rentals["season_label"] = season_rentals["season"].map({1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    return season_rentals

def create_daily_season_rentals(df):
    daily_season_rentals = df.groupby(['season', 'weekday']).cnt.mean().reset_index()
    daily_season_rentals["season_label"] = daily_season_rentals["season"].map({1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    daily_season_rentals["weekday_label"] = daily_season_rentals["weekday"].map({
    0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
    })
    return daily_season_rentals

bs_day = pd.read_csv("day.csv")

datetime_columns = ["dteday"]
bs_day.sort_values(by="dteday", inplace=True)
bs_day.reset_index(inplace=True)

for column in datetime_columns:
    bs_day[column] = pd.to_datetime(bs_day[column])

min_date = pd.to_datetime(bs_day["dteday"].min())
max_date = pd.to_datetime(bs_day["dteday"].max())

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = bs_day[(bs_day["dteday"] >= str(start_date)) & 
                (bs_day["dteday"] <= str(end_date))]


dataset = create_dataset(main_df)
year_rentals = create_year_rentals(main_df)
month_rentals = create_month_rentals(main_df)
season_rentals = create_season_rentals(main_df)
daily_season_rentals = create_daily_season_rentals(main_df)

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Dataset')
 
col1, col2 = st.columns(2)
 
with col1:
    total_rentals = dataset.instant.sum()
    st.metric("Total Records", value=total_rentals)
 
with col2:
    total_count = format_currency(dataset.cnt.sum(), "AUD", locale='es_CO') 
    st.metric("Total Counts", value=total_count)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    dataset["dteday"],
    dataset["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=17)
st.pyplot(fig)


st.subheader('Performance from 2011 to 2012')

colors = ["#D3D3D3", "#72BCD4"]

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x="yr_label",
    y="cnt",
    data = year_rentals.sort_values(by = "yr_label", ascending = False),
    palette=colors,
    ax=ax
    )
ax.set_title("Number of Bike Sharing (Year)", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=23)
ax.tick_params(axis='x', labelsize=23)
st.pyplot(fig)


fig, ax = plt.subplots(figsize=(20, 10))
ax = sns.lineplot(
    x="mnth_label", 
    y="cnt", 
    hue="yr_label", 
    data=month_rentals, 
    marker='o', 
    linewidth=3,
    palette=["#D3D3D3", "#72BCD4"]
    )
ax.grid(False, axis='both')
ax.set_title("Bike Sharing Trend (Month)", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=23)
ax.tick_params(axis='x', rotation=45, labelsize=23)
ax.legend(title="Tahun")
st.pyplot(fig)


st.subheader('Bike Sharing by Season')

colorss = ["#72BCD4", "#F08080", "#32CD32", "#4682B4"]

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x='season_label',
    y='cnt',
    data=season_rentals.sort_values(by="season", ascending=True),
    palette=colorss,
    ax=ax
    )
ax.set_title("Number of Bike Sharing by Season", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=23)
ax.tick_params(axis='x', labelsize=23)
st.pyplot(fig)


fig, ax = plt.subplots(figsize=(20, 10))
ax = sns.lineplot(
    x='weekday_label',
    y='cnt',
    hue='season_label',
    data=daily_season_rentals,
    marker='o', 
    linewidth=3,
    palette=["#72BCD4", "#F08080", "#32CD32", "#4682B4"]
    )
ax.grid(False, axis='both')
ax.set_title("Daily Trends of Bike Sharing by Season", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=23)
ax.tick_params(axis='x', labelsize=23)
ax.legend(title="Musim")
st.pyplot(fig)

st.caption('Copyright (c) Dicoding 2024')