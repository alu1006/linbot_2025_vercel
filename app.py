from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# LINE Bot 的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('kfJMMdCmuF0SVe+QB4UwNBRU/hBd7MlF1vkhBC0udOaXF2hyGoRXyATWECXCm7aOrAYCtGYe3HwrhhfsvDZteVs22+qt91VAp5JvbEzXoD8fEYqTVKCKCaMxMLgn5dB1nAqKDOEiVhw5Oj7h9OxgnQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('20bef6564c18cfea7977c25f6fb041d7')

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 X-Line-Signature 標頭值
    signature = request.headers['X-Line-Signature']

    # 獲取請求正文
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 處理 webhook 主體
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回覆與使用者相同的訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()
