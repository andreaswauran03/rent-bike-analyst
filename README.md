---
jupyter:
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  language_info:
    codemirror_mode:
      name: ipython
      version: 3
    file_extension: .py
    mimetype: text/x-python
    name: python
    nbconvert_exporter: python
    pygments_lexer: ipython3
    version: 3.11.4
  nbformat: 4
  nbformat_minor: 5
---

## Rent Bike Analyst Project
```
Welcome to our journey to understand more about the relationship between customers and the factors that influence their rental decisions. In this project, we will explore the world of data and explore the various aspects involved in the growth process, including time of day, seasons, and the influence of the surrounding environment.
```

## What Will You Find Here
```
- Is there a relationship between the number of bicycle renters and environmental conditions such as temperature, perceived temperature, wind speed, and humidity?
- At what time does bike rental activity peak?
- In what month do most bicycle rentals occur?
- In what season is bicycle rental activity highest?
- Under what weather conditions does bicycle rental occur most often?
```

## Setup Installation
### Setup Environment

``` python
conda create --name main-ds python=3.11
conda activate main-ds
pip install numpy pandas matplotlib jupyter streamlit
```

### Run Steamlit App for Dashboard

``` python
streamlit run dashboard_rent_bike.py
```