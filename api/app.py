from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os


app = Flask(__name__)

# # 環境變數（Vercel 會自動讀取）
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
line_handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/")
def home():
    return f"LINE Bot is running on Vercel!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    app.logger.info("Request body: " + body)

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """回覆與使用者相同的訊息"""
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

# if __name__ == "__main__":
#     app.run(port=8080)
