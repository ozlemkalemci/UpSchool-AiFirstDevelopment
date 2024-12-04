import streamlit as st

def file_uploader():
    st.subheader("Dosya Yükleme")
    uploaded_file = st.file_uploader("Lütfen 'Timestamp' ve 'Energy_Consumption' sütunlarını içeren iki kolonlu bir csv dosyası yükleyin.", type=["csv"])
    if uploaded_file:
        return uploaded_file
