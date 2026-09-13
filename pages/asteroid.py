import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. Judul Aplikasi
st.title('NASA Asteroid Impacts Analysis')

# 2. Konstanta
DATA_URL = 'impacts.csv'
YEAR_COLUMN = 'period start'

# 3. Fungsi Load Data dengan Progress Bar
@st.cache_data
def load_data(nrows=None):
    # Membuat Progress Bar dan Status Text
    progress_text = st.empty()
    progress_bar = st.progress(0)
    
    progress_text.text("Menghubungkan ke dataset...")
    progress_bar.progress(20)
    time.sleep(0.2) # Menyimulasikan tahapan loading
    
    # Memuat data
    progress_text.text("Mengunduh data asteroid...")
    data = pd.read_csv(DATA_URL, nrows=nrows)
    progress_bar.progress(60)
    time.sleep(0.2)
    
    # Mengubah nama kolom menjadi lowercase dan menghilangkan spasi berlebih
    progress_text.text("Memproses kolom data...")
    lowercase = lambda x: str(x).lower().strip()
    data.rename(lowercase, axis='columns', inplace=True)
    
    # Memastikan kolom tahun bertipe numerik
    if YEAR_COLUMN in data.columns:
        data[YEAR_COLUMN] = pd.to_numeric(data[YEAR_COLUMN], errors='coerce')
    
    progress_bar.progress(100)
    time.sleep(0.2)
    
    # Membersihkan tampilan progress bar setelah selesai
    progress_text.empty()
    progress_bar.empty()
    
    return data

# Memuat Data
data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache_data)")

# 4. Menampilkan / Menyembunyikan Raw Data Menggunakan Checkbox
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# 5. Menambahkan Bar Chart Jumlah Asteroid Berdasarkan Tahun Awal Potensi Impact
st.subheader('Number of potential asteroid impacts by start year')
valid_years = data[YEAR_COLUMN].dropna().astype(int)
counts = valid_years.value_counts().sort_index()
st.bar_chart(counts)

# 6. Menampilkan Filter Slider dan Data Terfilter
min_year = int(valid_years.min())
max_year = int(valid_years.max())

year_to_filter = st.slider('Period start year', min_year, max_year, min_year)
filtered_data = data[data[YEAR_COLUMN] == year_to_filter]

st.subheader(f'Asteroids with potential impact starting in {year_to_filter}')
st.write(f"Ditemukan **{len(filtered_data)}** asteroid untuk tahun awal **{year_to_filter}**:")

# Menampilkan tabel ringkasan data terfilter
cols_to_show = [
    'object name', 
    'possible impacts', 
    'asteroid velocity', 
    'asteroid diameter (km)', 
    'maximum torino scale'
]
available_cols = [c for c in cols_to_show if c in filtered_data.columns]
st.dataframe(filtered_data[available_cols])

# Visualisasi grafik titik (Scatter Chart) Kecepatan vs Diameter Asteroid
if not filtered_data.empty and 'asteroid diameter (km)' in filtered_data.columns and 'asteroid velocity' in filtered_data.columns:
    st.subheader('Asteroid Velocity vs Diameter (km)')
    st.scatter_chart(
        filtered_data, 
        x='asteroid diameter (km)', 
        y='asteroid velocity'
    )