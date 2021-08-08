# stock_price_chart

指定した銘柄の株価（直近から6ヶ月前まで）を取得し、作成した株価と出来高のチャートをSlack/twitterへ定刻で通知します。  
データソースは、https://finance.yahoo.com/

　

[Python&Lambda(+ServerlessFramework)で指定した企業の株価データとチャート図を定期的にSlack通知する](https://zenn.dev/whitecat_22/articles/aa413e426246e5)

　

- ^N225 の直近6ヶ月間の株価と出来高の推移をチャートにしたもの

![https://github.com/whitecat-22/stock_price_chart/blob/main/%E4%B8%80%E7%9B%AE%E5%9D%87%E8%A1%A1%E8%A1%A8_20210808.png](https://github.com/whitecat-22/stock_price_chart/blob/main/%E4%B8%80%E7%9B%AE%E5%9D%87%E8%A1%A1%E8%A1%A8_20210808.png)

　

- Slackへ通知した結果

![https://github.com/whitecat-22/stock_price_chart/blob/main/Slack_20210621.PNG](https://github.com/whitecat-22/stock_price_chart/blob/main/Slack_20210621.PNG)

　

- twitterへ投稿した結果

![https://github.com/whitecat-22/stock_price_chart/blob/main/Twitter_20210621.PNG](https://github.com/whitecat-22/stock_price_chart/blob/main/Twitter_20210621.PNG)
