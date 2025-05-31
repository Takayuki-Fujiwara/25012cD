import streamlit as st

# Streamlit Cloudの「Secrets」からAzure API keyとエンドポイントを取得
subscription_key = st.secrets.AzureAPI.api_key
endpoint = st.secrets.AzureAPI.endpoint

st.write("APIキー:", st.secrets.AzureAPI.api_key)
st.write("エンドポイント:", st.secrets.AzureAPI.endpoint)
