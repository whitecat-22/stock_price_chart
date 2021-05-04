"""
json: Format the data to be sent by the SLack API into JSON
requests: HTTP client
"""
import os
from os.path import join, dirname
from dotenv import load_dotenv
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

dotenv_path = join(dirname(__file__), '.env')
#load_dotenv(dotenv_path)
load_dotenv(verbose=True)
# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
# ID of channel that you want to upload file to
load_dotenv(dotenv_path)
token = os.environ.get("SLACK_BOT_TOKEN")
channel_id = os.environ.get("SLACK_CHANNEL_ID")
stock_code = os.environ.get("STOCK_CODE")

class Slack():
    """
    Notification Class to configure the settings for the Slack API
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
        Create params data for sending Slack notification with API.
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
               f"*銘柄* {str(stock_code)}\n" \
               f"*日付* {str(ohlcv['Date'])}\n" \
               f"*始値* {float(ohlcv['Open'])}\n" \
			   f"*高値* {float(ohlcv['High'])}\n" \
			   f"*安値* {float(ohlcv['Low'])}\n" \
			   f"*終値* {float(ohlcv['Close'])}\n" \
			   f"*出来高* {int(ohlcv['Volume']):,d}"
        return text

    def post(self):
        """
        POST request to Slack file upload API
        API docs: https://slack.com/api/files.upload
        """
        # The name of the file you're going to upload
        file = open(f"/tmp/{str(self.date)}.png", 'rb')
        title = f"{str(self.date)}.png"
        # Call the files.upload method using the WebClient
        # Uploading files requires the `files:write` scope
        try:
            client.files_upload(
                channels=channel_id,
                initial_comment=self.text,
                file=file,
                title=title
            )
        except Exception as e:
            print(e)
