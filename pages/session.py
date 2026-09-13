import streamlit as st

# Definisi fungsi Callback
def form_callback():
    st.write("Slider value:", st.session_state.my_slider)
    st.write("Checkbox value:", st.session_state.my_checkbox)

# Membuat Form
with st.form(key='my_form'):
    slider_input = st.slider('My slider', 0, 10, 5, key='my_slider')
    checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
    
    # Tombol submit memanggil callback function saat diklik
    submit_button = st.form_submit_button(label='Submit', on_click=form_callback)