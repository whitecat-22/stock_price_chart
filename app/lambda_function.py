import csv
import datetime
import os
from os.path import join, dirname
import pandas as pd
import mplfinance as mpf
import pandas_datareader as data
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta

from notifiers import slack


# Load env variants
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
stock_code = os.environ.get("STOCK_CODE")

# Get today's date for getting the stock price and csv&image filename
today = datetime.date.today()

# tmp directory is present by default on Cloud Functions, so guard it
if not os.path.isdir('/tmp'):
    os.mkdir('/tmp')

FILENAME = '%s.csv' % str(today)


def generate_stock_chart_image():
    """
    Generate a six-month stock chart image with mplfinance
    """
    dataframe = pd.read_csv(
        f"/tmp/{str(today)}.csv", index_col=0, parse_dates=True)
    # The return value `Date` from stooq is sorted by asc, so change it to desc for plot
    dataframe = dataframe.sort_values('Date')
    mpf.plot(dataframe, type='candle', figratio=(12, 4),
             volume=True, mav=(5, 25), style='sas',
             savefig=f"/tmp/{str(today)}.png")


def generate_csv_with_datareader():
    """
    Generate a csv file of OHLCV with date with stooq API
    """
    # 株価推移の開始日を指定(6ヶ月を指定)
    start_date = today - relativedelta(months=6)

    # yahoofinanceのライブラリ経由でAPIを叩く(stock_codeは環境変数で株コードを指定)
    df = data.DataReader(stock_code, 'yahoo', start_date, today)
    df = df[['High', 'Low', 'Open', 'Close', 'Volume']]
    # df.tail()

    # APIで取得したデータを一旦CSVファイルにする
    df = df.sort_values(by='Date', ascending=False)
    df.to_csv(f"/tmp/{str(today)}.csv")
    # print(df)

def lambda_handler(event, context):
    """
    lambda_handler
    """
    print('event: {}'.format(event))
    print('context: {}'.format(context))
    """
    The main function that will be executed when this Python file is executed
    """
    generate_csv_with_datareader()
    generate_stock_chart_image()

    with open(f"/tmp/{str(today)}.csv", 'r', encoding="utf-8") as file:
        # Skip header row
        reader = csv.reader(file)
        header = next(reader)
        for i, row in enumerate(csv.DictReader(file, header)):
            # Send only the most recent data to Slack notification
            if i == 0:
                slack.Slack(today, row).post()

    return {
        'status_code': 200
    }

if __name__ == "__main__":
    print(lambda_handler(event=None, context=None))
