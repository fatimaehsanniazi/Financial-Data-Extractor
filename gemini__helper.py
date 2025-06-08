import google.generativeai as genai
import json
import pandas as pd
import yfinance as yf
from key import skey

api_key = skey
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.0-flash')

prompt_financial = """
Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
from the following news article. If you can't find the information from this article 
then return "". Do not make things up.    
Then retrieve a stock symbol corresponding to that company. For this you can use
your general knowledge (it doesn't have to be from this article). Always return your
response as a valid JSON string. The format of that string should be this:
{
    "Company Name": "Walmart",
    "Stock Symbol": "WMT",
    "Revenue": "12.34 million",
    "Net Income": "34.78 million",
    "EPS": "2.1 $"
}
News Article:
============
"""

def extract_financial_data(request):
    try:
        prompt_final=prompt_financial+request
        response=model.generate_content(prompt_final)
        # cleaning the reponse to remove extra characters
        response_text=response.text.strip().strip("```json").strip("```").strip()
        reponse_df=json.loads(response_text)
        df=pd.DataFrame(list(reponse_df.items()), columns=["Measures", "Values"])
        return df
    except (json.JSONDecodeError, IndexError, AttributeError):
        return pd.DataFrame(columns=["Measures", "Values"])

    
def get_live_financials(ticker):
    try:
        stock=yf.Ticker(ticker)
        info=stock.info
        company_name = info.get("longName", "")
        revenue = info.get("totalRevenue", "")
        net_income = info.get("netIncomeToCommon", "")
        eps = info.get("trailingEps", "")

        return pd.DataFrame({
            "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
            "Value": [
                company_name,
                ticker.upper(),
                format_money(revenue),
                format_money(net_income),
                f"${eps:.2f}" if eps else ""
            ]
        })

    except Exception as e:
        print("Error fetching from yfinance:", e)
        return pd.DataFrame({
            "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
            "Value": ["", "", "", "", ""]
        })

def generate_insight(company, revenue, income, eps):
    prompt = f"""
    Given the financials of {company}:
    Revenue: {revenue}
    Net Income: {income}
    EPS: {eps}
    
    Write a short analysis on the company's financial performance. Avoid made-up numbers.
    For example, 
    Given the financials of Apple Inc.:
    Revenue: $394.33B  
    Net Income: $99.80B  
    EPS: $6.11  
     
    Expected respose format: Apple Inc. has demonstrated strong financial performance. With a revenue of $394.33 billion and a net income of $99.80 billion, the company maintains a high profit margin, indicating effective cost management. An EPS of $6.11 reflects solid earnings per share, signaling good value generation for investors. These figures point to Apple’s continued dominance and financial stability in the tech sector.

    For example, 
    Given the financials of Bed Bath & Beyond Inc.:
    Revenue: $5.18B  
    Net Income: -$1.12B  
    EPS: -$13.44
     
    Expected Response format: Bed Bath & Beyond Inc. is facing significant financial difficulties. The company reported a revenue of $5.18 billion but a net loss of $1.12 billion, indicating severe profitability issues. The negative EPS of -$13.44 reflects substantial losses per share, raising concerns for investors. These figures suggest poor cost control and declining performance, potentially impacting long-term sustainability

    """
    response = model.generate_content(prompt)
    return response.text.strip()

def format_money(val):
    try:
        val = float(val)
        if val >= 1e9:
            return f"${val / 1e9:.2f}B"
        elif val >= 1e6:
            return f"${val / 1e6:.2f}M"
        return f"${val:.2f}"
    except (ValueError, TypeError):
        return ""
    
if __name__ == "__main__":
    article_text = input("Paste a financial news article:\n")
    df = extract_financial_data(article_text)
    if df is not None:
        print("\nExtracted financial data from article:")
        print(df)
    else:
        ticker = input("Enter company ticker symbol to fetch live financials: ")
        live_df = get_live_financials(ticker)
        print("\nLive financial data from Yahoo Finance:")
        print(live_df)
        values = live_df.set_index("Measure")["Value"]
        company_name = values["Company Name"]
        revenue = values["Revenue"]
        net_income = values["Net Income"]
        eps = values["EPS"]

        short_analysis=generate_insight(company_name, revenue, net_income, eps)
        print(short_analysis)
