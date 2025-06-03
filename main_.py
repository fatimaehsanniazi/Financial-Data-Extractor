import streamlit as st
import gemini__helper
import pandas as pd

st.set_page_config(page_title="Financial Data App", layout="centered")

st.markdown("""
<style>
.big-button {
    background-color: #1f77b4;  /* blue */
    color: white;
    font-size: 20px;
    padding: 15px 40px;
    margin: 10px 15px 30px 15px;
    border-radius: 12px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
    width: 250px;
    font-weight: 600;
}
.big-button:hover {
    background-color: #155d8b;
    color: #e0e0e0;
}
.big-button-green {
    background-color: #2ca02c;  /* green */
}
.big-button-green:hover {
    background-color: #1e7a1e;
    color: #e0e0e0;
}
.title {
    color: #0d1a35;
    font-weight: 700;
    font-size: 36px;
    margin-bottom: 0px;
}
.subtitle {
    color: #4a4a4a;
    font-size: 18px;
    margin-top: 0px;
    margin-bottom: 40px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">Financial Data Extraction & Live Data Tool</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Choose one of the options below to get started</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    extract_text_clicked = st.button("Extract from Financial Text", key="btn_text", help="Paste news/article text", 
                                    args=None, kwargs=None, type="primary", 
                                    on_click=None, use_container_width=True)
with col2:
    live_data_clicked = st.button("Get Live Financial Data", key="btn_live", help="Enter ticker symbol", 
                                 args=None, kwargs=None, type="primary",
                                 on_click=None, use_container_width=True)

if 'page' not in st.session_state:
    st.session_state.page = None

if extract_text_clicked:
    st.session_state.page = 'extract_text'

if live_data_clicked:
    st.session_state.page = 'live_data'

if not extract_text_clicked and not live_data_clicked and st.session_state.page is None:
    st.info("Please select an option above to proceed.")

if st.session_state.page == 'extract_text':
    st.header("Paste your financial news or article text below:")
    article = st.text_area("Financial Text", height=300)
    if st.button("Extract Financial Data"):
        if not article.strip():
            st.warning("Please enter some financial text to extract data.")
        else:
            df = gemini__helper.extract_financial_data(article)
            if df is not None and not df.empty:
                st.success("Financial data extracted from the article:")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No financial metrics found in the article.")
                ticker = st.text_input("Enter company ticker symbol to fetch live financials as fallback:")
                if ticker:
                    live_df = gemini__helper.get_live_financials(ticker)
                    st.info("Live financial data from Yahoo Finance:")
                    st.dataframe(live_df, use_container_width=True)

elif st.session_state.page == 'live_data':
    st.header("Enter a company ticker symbol:")
    ticker_input = st.text_input("Ticker Symbol")
    if st.button("Fetch Live Data"):
        if not ticker_input.strip():
            st.warning("Please enter a ticker symbol.")
        else:
            live_df = gemini__helper.get_live_financials(ticker_input.strip())
            st.dataframe(live_df, use_container_width=True)
            values = live_df.set_index("Measure")["Value"]
            company_name = values.get("Company Name", "")
            revenue = values.get("Revenue", "")
            net_income = values.get("Net Income", "")
            eps = values.get("EPS", "")

            if all([company_name, revenue, net_income, eps]):
                summary = gemini__helper.generate_insight(company_name, revenue, net_income, eps)
                st.markdown("Financial Summary:")
                st.markdown(f"<div style='background-color:#f1f1f1; padding:15px; border-radius:10px; color:#333;'>{summary}</div>", unsafe_allow_html=True)

               
