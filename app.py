import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# from fsm import TocMachine
from machine import CreateFSM
from utils import send_text_message

load_dotenv()

machines = {}

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    for event in events:
        if event.source.user_id not in machines:
            machines[event.source.user_id] = CreateFSM()
        state = machines[event.source.user_id].state
        print(f"\nFSM STATE: {state}")
        print(f"REQUEST BODY: \n{body}")
        response = machines[event.source.user_id].advance(event)
        if response == False:
            if state == "user":
                send_text_message(event.reply_token, "請先輸入\"menu\"或\"主選單\"進入主選單")
            elif state == "select_location":
                send_text_message(event.reply_token, "請告訴我你的位置")
            elif state == "show_result" or state == "select_detail":
                send_text_message(event.reply_token, "請輸入正確的編號喔~")
            else:
                send_text_message(event.reply_token, "請依照我的指示喔~")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine = CreateFSM()
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", None)
    app.run(host="0.0.0.0", port=port, debug=True)
