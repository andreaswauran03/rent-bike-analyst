import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

hours_df = pd.read_csv("hours_df.csv")
days_df = pd.read_csv("days_df.csv")

print(hours_df)

# Mengubah object datatype menjadi datetime
days_df["dteday"] = pd.to_datetime(days_df["dteday"])
hours_df["dteday"] = pd.to_datetime(hours_df["dteday"])

# Membuat dataframe monthly_cnt
def create_monthly_cnt_df(df):
    monthly_cnt_df = df.resample(rule='M', on='dteday').agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    })

    monthly_cnt_df.index = monthly_cnt_df.index.strftime('%B %Y') #mengubah format order date menjadi nama bulan
    monthly_cnt_df = monthly_cnt_df.reset_index()

    return monthly_cnt_df

# Membuat dataframe by_season
def create_by_season_df(df):
    by_season = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum"
    }).reset_index()

    season = {1: "Spring", 2: "Summer", 3: "Autumn", 4: "Winter"}
    by_season["season"] = by_season["season"].map(season)

    return by_season

# Membuat dataframe by_hour
def create_by_hour_df(df):
    by_hour = df.groupby("hr").agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    }).reset_index()

    return by_hour

# Membuat dataframe by_weathersit
def create_by_weathersit_df(df):
    by_weather = df.groupby("weathersit").agg({
        "cnt": "sum"
    }).reset_index()

    weather = {1: "Clear,Few clouds",
               2: "Mist+Cloudy",
               3: "Light Snow/Rain + Thunderstorm"}

    by_weather["weathersit"] = by_weather["weathersit"].map(weather)
    return by_weather

# Menentukan nilai maksimum dan minimum dari date dan hour
min_date = days_df["dteday"].min()
max_date = days_df["dteday"].max()
min_hour = hours_df["hr"].min()
max_hour = hours_df["hr"].max()

# Header pada web
st.write("<h1 style='text-align:justify;'>🏍️ Rent Bike Dashboard 🏍️</h1>", unsafe_allow_html=True)

# Date Input pada Web
start_date, end_date = st.date_input(
    label='Rentang Tanggal', min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date])

# Dataframe days yang digunakan
main_days_df = days_df[(days_df["dteday"] >= str(start_date)) &
                       (days_df["dteday"] <= str(end_date))]

# Metrik kolumn ke 1
col1, col2, col3 = st.columns(3)

with col1:
    total_customer = main_days_df.cnt.sum()
    st.metric("Total Customers", value=f"{total_customer} 👤")

with col2:
    casual_customer = main_days_df.casual.sum()
    st.metric("Casual Customers", value=f"{casual_customer} 🩳")

with col3:
    registered_customer = main_days_df.registered.sum()
    st.metric("Registered Customers", value=f"{registered_customer} 🎫")

# Metrik kolumn ke 2
col1, col2, col3, col4 = st.columns(4)

with col1:
    average_temp = main_days_df.temp.mean()
    st.metric("Avg Temperature", value=f"{round(average_temp, 2)} °C")

with col2:
    average_atemp = main_days_df.atemp.mean()
    st.metric("Avg Aprt Temperature", value=f"{round(average_atemp, 2)} °C")

with col3:
    average_windspeed = main_days_df.windspeed.mean()
    st.metric("Avg Windspeed", value=f"{round(average_windspeed, 2)} Knot")

with col4:
    average_hum = main_days_df.hum.mean()
    st.metric("Avg Humidity", value=f"{round(average_hum, 2)} RH")

# Write Days Chart
st.write("<h3 style={text-align: center;}'>Days Chart</h3>", unsafe_allow_html=True)

# Line Chart Monthly Customers
# Membuat function axis
def axis_par(ax, hexcolor, linewidth):
    ax.set_facecolor(hexcolor)
    ax.spines['left'].set_linewidth(linewidth)
    ax.spines['bottom'].set_linewidth(linewidth)
    ax.spines['top'].set_linewidth(linewidth)
    ax.spines['right'].set_linewidth(linewidth)


# Memanggil dataframe
monthly_cnt_df = create_monthly_cnt_df(main_days_df)

fig, ax = plt.subplots(figsize=(20, 15),
                       facecolor="#222831")
ax.plot(
    monthly_cnt_df["dteday"],
    monthly_cnt_df["cnt"],
    label="Total Order",
    linewidth=8,
    marker='o',
    markersize=16,
    color="#08D9D6"
)

ax.plot(
    monthly_cnt_df["dteday"],
    monthly_cnt_df["registered"],
    label="Registered Customer",
    linewidth=8,
    marker='o',
    markersize=16,
    color="#8DDFCB"
)

ax.plot(
    monthly_cnt_df["dteday"],
    monthly_cnt_df["casual"],
    label="Casual Customer",
    linewidth=8,
    marker='o',
    markersize=16,
    color="#CDFAD5"
)
# Mengubah Ketebalan pada garis axis
axis_par(ax, "#222831", 5)
# Mengatur Legend
ax.legend(fontsize=20, title_fontsize=20, facecolor="#393E46")
# Mengatur parameter pada Axis
ax.set_title("Number of Orders per Month", loc="center", fontsize=50, fontweight="bold")
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=15, rotation=25)
ax.set_xlabel('Month', fontsize=30, fontweight="bold")
ax.set_ylabel('Customer', fontsize=30, fontweight="bold")
# Ploting pada streamlit
st.pyplot(fig)

# Bar Chart Weather Situation dan Season
# Memanggil Dataframe by_weather
by_weather = create_by_weathersit_df(main_days_df)
# Setup Figure
fig, ax = plt.subplots(nrows=1,
                       ncols=2,
                       figsize=(50, 25),
                       facecolor="#222831")
ax[0].bar(
    x=by_weather["weathersit"],
    height=by_weather["cnt"],
    edgecolor="#903749",
    linewidth=5,
    color="#FF2E63"
)
# Mengubah Ketebalan pada garis axis
axis_par(ax[0], "#222831", 5)
# Mengatur parameter pada Axis
ax[0].set_title("Customer By Weather", loc="center", fontsize=50, fontweight="bold")
ax[0].tick_params(axis='y', labelsize=40)
ax[0].tick_params(axis='x', labelsize=40, rotation=5)
ax[0].set_xlabel('Weather Situation', fontsize=40, fontweight="bold")
ax[0].set_ylabel('Customer', fontsize=40, fontweight="bold")

# Memanggil Dataframe by_season
by_season = create_by_season_df(main_days_df)

ax[1].bar(
    by_season["season"],
    by_season["registered"],
    label="Registered Order",
    linewidth=5,
    color="#793FDF"
)
ax[1].bar(
    by_season["season"],
    by_season["casual"],
    label="Casual Order",
    linewidth=5,
    color="#D67BFF"
)
# Mengubah Ketebalan pada garis axis
axis_par(ax[1], "#222831", 5)
# Mengatur parameter legend
ax[1].legend(fontsize=40, title_fontsize=40, facecolor="#393E46")
# Mengatur parameter pada Axis
ax[1].set_title("Customer By Season",
                loc="center", fontsize=60, fontweight="bold")
ax[1].tick_params(axis='y', labelsize=40)
ax[1].tick_params(axis='x', labelsize=40, rotation=5)
ax[1].set_xlabel('Season', fontsize=40, fontweight="bold")
ax[1].set_ylabel('Customer', fontsize=40, fontweight="bold")

st.pyplot(fig)

# Write Hour Chart
st.write("<h3 style={text-align: center;}'>Hour Line Chart</h3>", unsafe_allow_html=True)

# Hour Line Chart
start_hour, end_hour = st.slider(
    label='Rentang Waktu (Jam)',
    min_value=min_hour,
    max_value=max_hour,
    value=(min_hour, max_hour))

main_hours_df = hours_df[(hours_df["hr"] >= start_hour) &
                         (hours_df["hr"] <= end_hour) &
                         (hours_df["dteday"] >= str(start_date)) &
                         (hours_df["dteday"] <= str(end_date))
                         ]

by_hour = create_by_hour_df(main_hours_df)

fig, ax = plt.subplots(figsize=(20, 15),
                       facecolor="#222831")
ax.plot(by_hour["hr"],
        by_hour["cnt"],
        linewidth=8,
        marker='o',
        markersize=16,
        color="#40128B",
        label="Total Order")
ax.plot(by_hour["hr"],
        by_hour["registered"],
        linewidth=8,
        marker='o',
        markersize=16,
        color="#79E0EE",
        label="Registered Order")
ax.plot(by_hour["hr"],
        by_hour["casual"],
        linewidth=8,
        marker='o',
        markersize=16,
        color="#FCFFB2",
        label="Casual Order")
# Mengubah Ketebalan pada garis axis
axis_par(ax, "#222831", 5)
# Mengatur Legend
ax.legend(fontsize=20, title_fontsize=20, facecolor="#393E46")
# Mengatur parameter pada axis
ax.set_title("Number of Orders per Hours", loc="center", fontsize=50, fontweight="bold")
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=25)
ax.set_xlabel('Hours', fontsize=35, fontweight="bold")
ax.set_ylabel('Customer', fontsize=35, fontweight="bold")

st.pyplot(fig)

# Write Correlation Chart
st.write("<h3 style={text-align: center;}'>Correlation Chart</h3>", unsafe_allow_html=True)

# Mengatur figure
fig, ax = plt.subplots(nrows=2,
                       ncols=2,
                       figsize=(60, 40),
                       facecolor="#222831")
ax[0, 0].scatter(
    main_days_df["cnt"],
    main_days_df["temp"],
    s=350,
    marker='o',
    color="#40128B"
)
axis_par(ax[0, 0], "#222831", 5)
ax[0, 0].set_title("Customer vs Temperature", loc="center", fontsize=80, fontweight="bold")
ax[0, 0].tick_params(axis='y', labelsize=45)
ax[0, 0].tick_params(axis='x', labelsize=45)
ax[0, 0].set_xlabel('Customer', fontsize=65, fontweight="bold")
ax[0, 0].set_ylabel('Temperature', fontsize=65, fontweight="bold")

ax[0, 1].scatter(
    main_days_df["cnt"],
    main_days_df["atemp"],
    s=350,
    marker='o',
    color='#D61355'
)
axis_par(ax[0, 1], "#222831", 5)
ax[0, 1].set_title("Customer vs Aprt Temperature", loc="center", fontsize=80, fontweight="bold")
ax[0, 1].tick_params(axis='y', labelsize=45)
ax[0, 1].tick_params(axis='x', labelsize=45)
ax[0, 1].set_xlabel('Customer', fontsize=65, fontweight="bold")
ax[0, 1].set_ylabel('Aprt Temperature', fontsize=65, fontweight="bold")

ax[1, 0].scatter(
    main_days_df["cnt"],
    main_days_df["hum"],
    s=250,
    marker='o',
    color='#B9F3E4'
)
# Mengatur garis pada Axis
axis_par(ax[1, 0], "#222831", 5)
ax[1, 0].set_title("Customer vs Humidity", loc="center", fontsize=80, fontweight="bold")
ax[1, 0].tick_params(axis='y', labelsize=45)
ax[1, 0].tick_params(axis='x', labelsize=45)
ax[1, 0].set_xlabel('Customer', fontsize=65, fontweight="bold")
ax[1, 0].set_ylabel('Humidity', fontsize=65, fontweight="bold")

ax[1, 1].scatter(
    main_days_df["cnt"],
    main_days_df["windspeed"],
    s=250,
    marker='o',
    color="#FFAACF"

)
axis_par(ax[1, 1], "#222831", 5)
ax[1, 1].set_title("Customer vs Windspeed", loc="center", fontsize=80, fontweight="bold")
ax[1, 1].tick_params(axis='y', labelsize=45)
ax[1, 1].tick_params(axis='x', labelsize=45)
ax[1, 1].set_xlabel('Customer', fontsize=65, fontweight="bold")
ax[1, 1].set_ylabel('Windspeed', fontsize=65, fontweight="bold")

st.pyplot(fig)