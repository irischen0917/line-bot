#架設服務器連結Line app

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('v2G2S6qVQq5kpjcp8xVQBjtpgIq8cRPsh/GkIJxk+ofQDJbXqo7yTTceopbOPjDnpuskr4lPqzCx0AmIryR7J1J5lXtUTpmhsbGQY+Y5N/uDuOrcC37CgU5NuMoedehn17UJ4kJx1j+PdBMeeBvWmwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('bcfe4ff3515f70b430880969a52a0db1')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()