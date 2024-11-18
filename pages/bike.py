import streamlit as st
import pandas as pd

if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]
with st.sidebar:
    st.caption(f'{ID}님 접속중')
data = pd.read_csv("공공자전거.csv")

st.title('공공자전거 어디있지?')


data = data.copy().fillna(0)
data.loc[:,'size'] = 5*(data['LCD']+data['QR'])
data


color = {'QR':'#37eb91',
         'LCD':'#ebbb37'}
data.loc[:,'color'] = data.copy().loc[:,'운영방식'].map(color)


st.map(data, latitude="위도",
       longitude="경도",
       size="size",
       color="color")
