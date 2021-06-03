try:
    #from notifiers import unzip_requirements
    import unzip_requirements
except ImportError:
    print('Import Error - unzip_requirements')
    pass
except Exception as e:
    print(e)
    pass

import csv
import datetime
import os
from os.path import join, dirname
import mplfinance as mpf
from pandas_datareader import data
import pandas as pd
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta

import matplotlib.pyplot as plt
import talib as ta

from notifiers import slack
from notifiers import twitter

import json
import logging

# settins for logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
    # The return value `Date` from yahoofinance is sorted by asc, so change it to desc for plot
    dataframe = dataframe.sort_values('Date')
    date = dataframe.index

    # 基準線
    high = dataframe['High']
    low = dataframe['Low']

    max26 = high.rolling(window=26).max()
    min26 = low.rolling(window=26).min()

    dataframe['basic_line'] = (max26 + min26) / 2

    dataframe.tail()

    plt.figure(figsize=(16, 6))
    plt.plot(dataframe['basic_line'], label='basic')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    #plt.show()

    # 転換線
    high9 = high.rolling(window=9).max()
    low9 = low.rolling(window=9).min()

    dataframe['turn_line'] = (high9 + low9) / 2

    dataframe.tail()

    plt.figure(figsize=(16, 6))
    plt.plot(dataframe['basic_line'], label='basic')
    plt.plot(dataframe['turn_line'], label='turn')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    #plt.show()

    # 雲形
    dataframe['span1'] = (dataframe['basic_line'] + dataframe['turn_line']) / 2

    high52 = high.rolling(window=52).max()
    low52 = low.rolling(window=52).min()

    dataframe['span2'] = (high52 + low52) / 2

    dataframe.tail()

    plt.figure(figsize=(16, 6))
    plt.plot(dataframe['basic_line'], label='basic')
    plt.plot(dataframe['turn_line'], label='turn')
    plt.fill_between(date, dataframe['span1'], dataframe['span2'],
                     facecolor="gray", alpha=0.5, label="span")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    #plt.show()

    # 遅行線
    dataframe['slow_line'] = dataframe['Adj Close'].shift(-25)

    dataframe.head()

    plt.figure(figsize=(16, 6))
    plt.plot(dataframe['basic_line'], label='basic')
    plt.plot(dataframe['turn_line'], label='turn')
    plt.fill_between(date, dataframe['span1'], dataframe['span2'],
                     facecolor="gray", alpha=0.5, label="span")
    plt.plot(dataframe['slow_line'], label='slow')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    #plt.show()

    # ボリンジャーバンド用のdataframe追加
    dataframe["upper"], dataframe["middle"], dataframe["lower"] = ta.BBANDS(
        dataframe['Adj Close'], timeperiod=25, nbdevup=2, nbdevdn=2, matype=0)
    dataframe.tail()

    # ボリンジャーバンドプロット
    apds = [mpf.make_addplot(dataframe['upper'], color='g'),
            mpf.make_addplot(dataframe['middle'], color='b'),
            mpf.make_addplot(dataframe['lower'], color='r')
            ]

    # MACD用のdataframe追加
    dataframe['macd'], dataframe['macdsignal'], dataframe['macdhist'] = ta.MACD(
        dataframe['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    dataframe.tail()

    # RSIデータフレーム追加
    dataframe["RSI"] = ta.RSI(dataframe["Adj Close"], timeperiod=25)
    dataframe.tail()

    # 基準線、転換線、雲、遅行線の追加
    apds = [mpf.make_addplot(dataframe['upper'], color='g'),
            mpf.make_addplot(dataframe['middle'], color='b'),
            mpf.make_addplot(dataframe['lower'], color='r'),
            mpf.make_addplot(dataframe['macdhist'], type='bar',
                             width=1.0, panel=1, color='gray', alpha=0.5, ylabel='MACD'),
            mpf.make_addplot(dataframe['RSI'], panel=2,
                             type='line', ylabel='RSI'),
            mpf.make_addplot(dataframe['basic_line']),  # 基準線
            mpf.make_addplot(dataframe['turn_line']),  # 転換線
            mpf.make_addplot(dataframe['slow_line']),  # 遅行線
            ]

    # 保存
    mpf.plot(dataframe, type='candle', addplot=apds, figsize=(30, 10), style='sas',
             volume=True, volume_panel=3, panel_ratios=(5, 2, 2, 1), savefig=f"/tmp/{str(today)}.png")

    # ローソク足
    mpf.plot(dataframe, type='candle', figsize=(16, 6),
             style='sas', xrotation=0, volume=True, addplot=apds)

    """
    mplfinanceに凡例を追加する方法は現状これしかないようです(https://github.com/matplotlib/mplfinance/issues/181)
    mplfinanceのfill_between(https://github.com/matplotlib/mplfinance/blob/master/examples/plot_customizations.ipynb)
    """

    fig, ax = mpf.plot(dataframe, type='candle', figsize=(16, 9),
                       style='sas', xrotation=0, volume=True, addplot=apds, returnfig=True,
                       volume_panel=3, panel_ratios=(5, 2, 2, 1),
                       fill_between=dict(
                           y1=dataframe['span1'].values, y2=dataframe['span2'].values, alpha=0.5, color='gray'),
                       savefig=f"/tmp/{str(today)}.png"
                       )
    #plt.show()
    labels = ["basic", "turn", "slow", "span"]
    ax[0].legend(labels)
    """
    mpf.plot(dataframe, type='candle', figratio=(12, 4),
             volume=True, mav=(5, 25), style='sas',
             savefig=f"/tmp/{str(today)}.png")
    """

def generate_csv_with_datareader():
    """
    Generate a csv file of OHLCV with date with yahoofinance API
    """
    # 株価推移の開始日を指定(6ヶ月を指定)
    start_date = today - relativedelta(months=6)

    # yahoofinanceのライブラリ経由でAPIを叩く(stock_codeは環境変数で株コードを指定)
    df = data.DataReader(stock_code, 'yahoo', start_date, today)
    df = df[['High', 'Low', 'Open', 'Close', 'Adj Close', 'Volume']]
    df.tail()

    # APIで取得したデータを一旦CSVファイルにする
    df = df.sort_values(by='Date', ascending=False)
    df.to_csv(f"/tmp/{str(today)}.csv")
    # print(df)


def lambdahandler(event, context):
    """
    lambda_handler
    """
    logging.info(json.dumps(event))

    print('event: {}'.format(event))
    print('context: {}'.format(context))
    """
    The main function that will be executed when this Python file is executed
    """
    generate_csv_with_datareader()
    generate_stock_chart_image()

    #if "challenge" in event["body"]:
    #    return event["body"]["challenge"]

    with open(f"/tmp/{str(today)}.csv", 'r', encoding="utf-8") as file:
        # Skip header row
        reader = csv.reader(file)
        header = next(reader)
        for i, row in enumerate(csv.DictReader(file, header)):
            # Send only the most recent data to Slack notification
            if i == 0:
                slack.Slack(today, row).post()
                twitter.Twitter(today, row).post()

    return {
        'statusCode': 200,
        'body': 'ok'
    }


if __name__ == "__main__":
    print(lambdahandler(event=None, context=None))
