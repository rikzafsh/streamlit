import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. Judul Aplikasi
st.title('Uber pickups in NYC')

# 2. Konstanta
DATE_COLUMN = 'date/time'
DATA_URL = 'https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz'

# 3. Fungsi Load Data dengan Progress Bar
@st.cache_data
def load_data(nrows):
    # Membuat Progress Bar dan Status Text
    progress_text = st.empty()
    progress_bar = st.progress(0)
    
    progress_text.text("Menghubungkan ke server...")
    progress_bar.progress(20)
    time.sleep(0.2) # Menyimulasikan tahapan loading
    
    # Memuat data
    progress_text.text("Mengunduh data...")
    data = pd.read_csv(DATA_URL, nrows=nrows)
    progress_bar.progress(60)
    time.sleep(0.2)
    
    # Mengubah nama kolom menjadi lowercase
    progress_text.text("Memproses kolom data...")
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    
    # Mengubah format kolom date/time
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    progress_bar.progress(100)
    time.sleep(0.2)
    
    # Membersihkan tampilan progress bar setelah selesai
    progress_text.empty()
    progress_bar.empty()
    
    return data

# Memuat Data
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

# 4. Menampilkan / Menyembunyikan Raw Data Menggunakan Checkbox
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# 5. Menambahkan Histogram / Bar Chart Jumlah Pickup Berdasarkan Jam
st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# 6. Menampilkan Peta Lokasi Pickup dengan Filter Slider Jam
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)