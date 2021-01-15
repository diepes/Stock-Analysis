#!env/bin/python3
''' Cobus Smit 2021
    started from
    https://www.mattbutton.com/2019/01/24/how-to-scrape-yahoo-finance-and-extract-fundamental-stock-market-data-using-python-lxml-and-pandas/

'''
from datetime import datetime
import time
import lxml
from lxml import html
import requests
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import lxml
from lxml import html
import requests
import numpy as np
import pandas as pd

def get_page(url):
    # Set up the request headers that we're going to use, to simulate
    # a request by the Chrome browser. Simulating a request from a browser
    # is generally good practice when building a scraper
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Pragma': 'no-cache',
        'Referrer': 'https://google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    return requests.get(url, headers=headers)


def parse_rows(table_rows):
    parsed_rows = []

    for table_row in table_rows:
        parsed_row = []
        el = table_row.xpath("./div")

        none_count = 0

        for rs in el:
            try:
                (text,) = rs.xpath('.//span/text()[1]')
                parsed_row.append(text)
            except ValueError:
                parsed_row.append(np.NaN)
                none_count += 1

        if (none_count < 4):
            parsed_rows.append(parsed_row)

    return pd.DataFrame(parsed_rows)

def clean_data(df):
    df = df.set_index(0) # Set the index to the first column: 'Period Ending'.
    df = df.transpose() # Transpose the DataFrame, so that our header contains the account names

    # Rename the "Breakdown" column to "Date"
    cols = list(df.columns)
    cols[0] = 'Date'
    df = df.set_axis(cols, axis='columns', inplace=False)

    numeric_columns = list(df.columns)[1::] # Take all columns, except the first (which is the 'Date' column)

    for column_index in range(1, len(df.columns)): # Take all columns, except the first (which is the 'Date' column)
        df.iloc[:,column_index] = df.iloc[:,column_index].str.replace(',', '') # Remove the thousands separator
        df.iloc[:,column_index] = df.iloc[:,column_index].astype(np.float64) # Convert the column to float64

    return df

def scrape_table(url):
    # Fetch the page that we're going to parse
    # Parse the page with LXML, so that we can start doing some XPATH queries
    # to extract the data that we want

    ## tree = html.fromstring( get_page(url).content )

    # Replace get_page[request] above with get_page_webdriver
    tree = html.fromstring( get_page_webdriver(url) )

    # Fetch all div elements which have class 'D(tbr)'
    table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")

    # Ensure that some table rows are found; if none are found, then it's possible
    # that Yahoo Finance has changed their page layout, or have detected
    # that you're scraping the page.
    assert len(table_rows) > 0

    df = parse_rows(table_rows)
    df = clean_data(df)

    return df


def get_page_webdriver(url):
    # browser = webdriver.Chrome(executable_path = "C:\\Users\Killer\Desktop\Phyton\\chromedriver.exe")
    browser = webdriver.Chrome(executable_path = "/usr/local/bin/chromedriver")
    print(f"DebugWD - loading page {url}")
    browser.get(url)
    print(f"DebugWD - scroll down")
    browser.execute_script("window.scrollTo(0,300)")
    time.sleep(1)
    print(f"DebugWD - click expand ...")
    click_expand = browser.find_element_by_xpath('//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button')
    click_expand.click()

    # Fetch the page that we're going to parse, using the request headers
    # defined above
    ## page = requests.get(url, headers)
    pageContent = browser.page_source
    return pageContent


symbol = 'SOL.JO'
symbol1 = 'KIO.JO'
# url = 'https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol

# pageContent = get_page_webdriver(url)
# print(f"We got pageContent {len(pageContent)}bytes")
# # Parse the page with LXML, so that we can start doing some XPATH queries
# # to extract the data that we want
# tree = html.fromstring(pageContent)
# print("lxml.html parsed page content", tree)
# # Smoke test that we fetched the page by fetching and displaying the H1 element
# tree.xpath("//h1/text()")
# table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")

# Ensure that some table rows are found; if none are found, then it's possible
# that Yahoo Finance has changed their page layout, or have detected
# that you're scraping the page.
# assert len(table_rows) > 0

# parsed_rows = []

# for table_row in table_rows:
#     parsed_row = []
#     el = table_row.xpath("./div")

#     none_count = 0

#     for rs in el:
#         try:
#             (text,) = rs.xpath('.//span/text()[1]')
#             parsed_row.append(text)
#         except ValueError:
#             parsed_row.append(np.NaN)
#             none_count += 1

#     if (none_count < 4):
#         parsed_rows.append(parsed_row)

# df = pd.DataFrame(parsed_rows)
# df

# df = pd.DataFrame(parsed_rows)
# df = df.set_index(0) # Set the index to the first column: 'Period Ending'.
# df = df.transpose() # Transpose the DataFrame, so that our header contains the account names

# # Rename the "Breakdown" column to "Date"
# cols = list(df.columns)
# cols[0] = 'Date'
# df = df.set_axis(cols, axis='columns', inplace=False)

# df

# df.dtypes

# numeric_columns = list(df.columns)[1::] # Take all columns, except the first (which is the 'Date' column)

# for column_name in numeric_columns:
#     df[column_name] = df[column_name].str.replace(',', '') # Remove the thousands separator
#     df[column_name] = df[column_name].astype(np.float64) # Convert the column to float64

# df.dtypes

# df

# #Debug
# print(df.to_markdown())
# print("Debug start next  scrape_table")

df_balance_sheet = scrape_table('https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol)

scrape_table('https://finance.yahoo.com/quote/' + symbol + '/financials?p=' + symbol)
scrape_table('https://finance.yahoo.com/quote/' + symbol + '/cash-flow?p=' + symbol)
#SCAPING MULTIPLE SYMBOLS

def scrape(symbol):
    print('Attempting to scrape data for ' + symbol)

    df_balance_sheet = scrape_table('https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol)
    df_balance_sheet = df_balance_sheet.set_index('Date')

    df_income_statement = scrape_table('https://finance.yahoo.com/quote/' + symbol + '/financials?p=' + symbol)
    df_income_statement = df_income_statement.set_index('Date')

    df_cash_flow = scrape_table('https://finance.yahoo.com/quote/' + symbol + '/cash-flow?p=' + symbol)
    df_cash_flow = df_cash_flow.set_index('Date')

    df_joined = df_balance_sheet \
        .join(df_income_statement, on='Date', how='outer', rsuffix=' - Income Statement') \
        .join(df_cash_flow, on='Date', how='outer', rsuffix=' - Cash Flow') \
        .dropna(axis=1, how='all') \
        .reset_index()

    df_joined.insert(1, 'Symbol', symbol)

    return df_joined
def scrape_multi(symbols):
    return pd.concat([scrape(symbol) for symbol in symbols], sort=False)
symbols = ['KIO.JO', 'SOL.JO']
df_combined = scrape_multi(symbols)
df_combined

date = datetime.today().strftime('%Y-%m-%d')
writer = pd.ExcelWriter('Yahoo-Finance-Scrape2-' + date + '.xlsx')
df_combined.to_excel(writer)
writer.save()