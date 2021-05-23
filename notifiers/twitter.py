"""
json: Format the data to be sent by the Twitter API into JSON
requests: HTTP client
"""
import os
from os.path import join, dirname
from dotenv import load_dotenv
import tweepy


dotenv_path = join(dirname(__file__), '.env')
#load_dotenv(dotenv_path)
load_dotenv(verbose=True)

load_dotenv(dotenv_path)
# 各種twitterのKeyをセット CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_KEY_SECRET
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_KEY_SECRET = os.environ.get('ACCESS_KEY_SECRET')

stock_code = os.environ.get("STOCK_CODE")

# tweepyの設定
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_KEY_SECRET)
api = tweepy.API(auth)


class Twitter():
    """
    Notification Class to configure the settings for the Twitter API
    """
    def __init__(self, date, ohlcv):
        self.__date = date
        self.text = self.__format_text(ohlcv)

    @property
    def date(self):
        """
        Property of date to be displayed in Slack text
        :return: Date
        """
        return self.__date

    def __format_text(self, ohlcv):
        """
        Create params data for sending Twitter notification with API.
        :param dict[str, str, str, str, str, str] ohlcv:
        :type ohlcv: {
            'Date': '2020-12-29',
            'Open': '7620',
            'High': '8070',
			'Low': '7610',
			'Close': '8060',
			'Volume': '823700'
        }
        :return: String
        """
        text = f"本日は{self.date.strftime('%Y年%m月%d日')}です。\n" \
               f"取得可能な最新日付の株価情報をお知らせします。 \n\n"\
               f"銘柄  {str(stock_code)}\n" \
               f"日付  {str(ohlcv['Date'])}\n" \
               f"始値  {float(ohlcv['Open'])}\n" \
			   f"高値  {float(ohlcv['High'])}\n" \
			   f"安値  {float(ohlcv['Low'])}\n" \
			   f"終値  {float(ohlcv['Close'])}\n" \
			   f"出来高  {int(ohlcv['Volume']):,d}"
        return text

    def post(self):
        """
        POST request to Twitter API
        API docs: https://developer.twitter.com/en/docs/twitter-api/api-reference-index
        """
        # The name of the file you're going to upload
        file = open(f"/tmp/{str(self.date)}.png", 'rb')
        title = f"{str(self.date)}.png"
        # Call the files.upload method using the WebClient
        # Uploading files requires the `files:write` scope
        try:
            file_names = ['/tmp/' + title, ]
            media_ids = []
            for filename in file_names:
                res = api.media_upload(filename)
                media_ids.append(res.media_id)
            # tweet with multiple images
            api.update_status(status= self.text + "\n\n" + title, media_ids=media_ids)
        except Exception as e:
            print(e)
