# Financial Data Extraction and Live Analysis Tool

This is a Streamlit-based web application that allows users to extract key financial metrics from pasted financial news articles or fetch live financial data using a company’s ticker symbol. It utilizes Google Gemini (Generative AI) for summarization and Yahoo Finance for real-time data retrieval.

## Features

- **Text-Based Financial Data Extraction**  
  Extract Revenue, Net Income, and EPS from any financial news article or report using AI.

- **Live Financial Data Retrieval**  
  Enter a company’s ticker symbol (e.g., MSFT, AAPL) to fetch real-time financial data.

- **AI-Powered Financial Summary**  
  Automatically generate performance insights using Google Gemini based on extracted or live data.

- **User-Friendly Interface**  
  Styled layout with responsive buttons and clear visuals using Streamlit.

## Technologies Used

- **Streamlit** – For building the interactive front end.
- **Pandas** – For data processing and display.
- **Google Gemini** – For financial summarization and insights.
- **yFinance** – For live financial data from Yahoo Finance.

## Getting Started

1. Clone the repository
2. Install dependencies (`pip install -r requirements.txt`)
3. Run the app with `streamlit run main_.py`

## Files

- `main_.py` – Main Streamlit application  
- `gemini__helper.py` – Helper functions for data extraction and Gemini interaction  
- `requirements.txt` – Required libraries
