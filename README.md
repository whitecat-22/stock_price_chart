# stock_price_chart

**指定した銘柄の株価（直近から6ヶ月前まで）を pandas-datareader により取得し、作成した株価と出来高のチャートを平日の定刻(JST 15:30) ＜※但し、取引所休場日を除く※＞ にSlack/twitterへ定刻で通知します。**

- 銘柄：　　　　　日経平均株価([^N225](https://finance.yahoo.com/quote/%5EN225/history?p=%5EN225))　　　　　←環境変数にて設定

- データソース：　[https://finance.yahoo.com/](https://finance.yahoo.com/)　　　←株価情報の取得は [pandas-datareader](https://github.com/pydata/pandas-datareader)を利用  

　

[一目均衡表](https://ja.wikipedia.org/wiki/%E4%B8%80%E7%9B%AE%E5%9D%87%E8%A1%A1%E8%A1%A8)の作成には mplfinance のほか、TA-Lib を使用しています。  
⇒ TA-Lib のインストールについては、[コチラ](https://zenn.dev/whitecat_22/articles/9e30d88e31c3ec)を参照ください。  

　

## ◆執筆記事：　[日本発祥のテクニカル指標「一目均衡表」を通知してみた【Python】](https://zenn.dev/whitecat_22/articles/344d60b810b77b)

<a href="https://zenn.dev/whitecat_22/articles/344d60b810b77b">
  <img src="https://github.com/whitecat-22/stock_price_chart/blob/main/zenn.png">
</a>

　

### ◆使用技術：

- Python 3.9

- AWS
  - [Lambda](https://aws.amazon.com/jp/lambda/?nc2=h_ql_prod_serv_lbd)
  - ECR (Elastic Container Registry)
  - EventBridge
  - [SNS (Simple Notification Service)](https://aws.amazon.com/jp/sns/?whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc)
  - CloudTrailLogs

- Docker

　

### ◆主な利用ライブラリ：

- [numpy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)
- [pandas-datareader](https://github.com/pydata/pandas-datareader)
- [mplfinance](https://github.com/matplotlib/mplfinance)
- [TA-Lib](https://ta-lib.org/)
- [slack-sdk](https://slack.dev/python-slack-sdk/)
- [tweepy](https://www.tweepy.org/)
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

　

### ◆実行結果：

- ^N225(日経平均株価) の直近6ヶ月間の株価と出来高の推移をチャートにしたもの

![https://github.com/whitecat-22/stock_price_chart/blob/main/%E4%B8%80%E7%9B%AE%E5%9D%87%E8%A1%A1%E8%A1%A8_20210808.png](https://github.com/whitecat-22/stock_price_chart/blob/main/%E4%B8%80%E7%9B%AE%E5%9D%87%E8%A1%A1%E8%A1%A8_20210808.png)

　

- Slackへ通知した結果

![https://github.com/whitecat-22/stock_price_chart/blob/main/slack_20210808.PNG](https://github.com/whitecat-22/stock_price_chart/blob/main/slack_20210808.PNG)

　

- twitterへ投稿した結果

![https://github.com/whitecat-22/stock_price_chart/blob/main/twitter_20210808.PNG](https://github.com/whitecat-22/stock_price_chart/blob/main/twitter_20210808.PNG)
