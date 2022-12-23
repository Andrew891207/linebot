import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["start", "front", "left", "right", "back", 
            "front_door", "front_window", "front_door_open",
            "left_safe", "left_wall", "left_safe_open",
            "right_bag", "right_box", "right_bag_open", "right_box_open",
            "back_picture", "back_calendar", "back_book", "back_picture_open"],
    transitions=[
        # start->
        {
            "trigger": "advance",
            "source": "start",
            "dest": "front",
            "conditions": "is_going_to_front",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "start",
        },
        # front->
        {
            "trigger": "advance",
            "source": "front",
            "dest": "left",
            "conditions": "is_turning_to_left",
        },
        {
            "trigger": "advance",
            "source": "front",
            "dest": "right",
            "conditions": "is_turning_to_right",
        },
        {
            "trigger": "advance",
            "source": "front",
            "dest": "back",
            "conditions": "is_turning_to_back",
        },
        {
            "trigger": "advance",
            "source": "front",
            "dest": "front_door",
            "conditions": "is_going_to_front_door",
        },
        {
            "trigger": "advance",
            "source": "front",
            "dest": "front_window",
            "conditions": "is_going_to_front_window",
        },
        # ->front
        {
            "trigger": "advance",
            "source": "front_door",
            "dest": "front",
            "conditions": "is_going_back",
        },
        {
            "trigger": "advance",
            "source": "front_window",
            "dest": "front",
            "conditions": "is_going_back",
        },
        # left->
        {
            "trigger": "advance",
            "source": "left",
            "dest": "back",
            "conditions": "is_turning_to_left",
        },
        {
            "trigger": "advance",
            "source": "left",
            "dest": "front",
            "conditions": "is_turning_to_right",
        },
        {
            "trigger": "advance",
            "source": "left",
            "dest": "right",
            "conditions": "is_turning_to_back",
        },
        {
            "trigger": "advance",
            "source": "left",
            "dest": "left_safe",
            "conditions": "is_going_to_left_safe",
        },
        {
            "trigger": "advance",
            "source": "left",
            "dest": "left_wall",
            "conditions": "is_going_to_left_wall",
        },
        # ->left
        {
            "trigger": "advance",
            "source": "left_safe",
            "dest": "left",
            "conditions": "is_going_back",
        },
        {
            "trigger": "advance",
            "source": "left_wall",
            "dest": "left",
            "conditions": "is_going_back",
        },
        # right->
        {
            "trigger": "advance",
            "source": "right",
            "dest": "front",
            "conditions": "is_turning_to_left",
        },
        {
            "trigger": "advance",
            "source": "right",
            "dest": "back",
            "conditions": "is_turning_to_right",
        },
        {
            "trigger": "advance",
            "source": "right",
            "dest": "left",
            "conditions": "is_turning_to_back",
        },
        {
            "trigger": "advance",
            "source": "right",
            "dest": "right_bag",
            "conditions": "is_going_to_right_bag",
        },
        {
            "trigger": "advance",
            "source": "right",
            "dest": "right_box",
            "conditions": "is_going_to_right_box",
        },
        # ->right
        {
            "trigger": "advance",
            "source": "right_bag",
            "dest": "right",
            "conditions": "is_going_back",
        },
        {
            "trigger": "advance",
            "source": "right_box",
            "dest": "right",
            "conditions": "is_going_back",
        },
        # back->
        {
            "trigger": "advance",
            "source": "back",
            "dest": "right",
            "conditions": "is_turning_to_left",
        },
        {
            "trigger": "advance",
            "source": "back",
            "dest": "left",
            "conditions": "is_turning_to_right",
        },
        {
            "trigger": "advance",
            "source": "back",
            "dest": "front",
            "conditions": "is_turning_to_back",
        },
        {
            "trigger": "advance",
            "source": "back",
            "dest": "back_picture",
            "conditions": "is_going_to_back_picture",
        },
        {
            "trigger": "advance",
            "source": "back",
            "dest": "back_calendar",
            "conditions": "is_going_to_back_calendar",
        },
        {
            "trigger": "advance",
            "source": "back",
            "dest": "back_book",
            "conditions": "is_going_to_back_book",
        },
        # ->back
        {
            "trigger": "advance",
            "source": "back_picture",
            "dest": "back",
            "conditions": "is_going_back",
        },
        {
            "trigger": "advance",
            "source": "back_calendar",
            "dest": "back",
            "conditions": "is_going_back",
        },
        {
            "trigger": "advance",
            "source": "back_book",
            "dest": "back",
            "conditions": "is_going_back",
        },
        # restart
        {
            "trigger": "advance",
            "source": ["start", "front", "left", "right", "back", 
            "front_door", "front_window", "front_door_open",
            "left_safe", "left_wall", "left_safe_open"
            "right_bag", "right_box", "right_bag_open", "right_box_open",
            "back_picture", "back_calendar", "back_book", "back_picture_open"],  # 要改
            "dest": "start",
            "conditions": "is_restart",
        }
        # {"trigger": "go_back", "source": ["state1", "state2"], "dest": "start"},
    ],
    initial="start",
    auto_transitions=False,
    show_conditions=True,
)

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
#machine.get_graph().draw("fsm.png", prog="dot", format="png")
#send_file("fsm.png", mimetype="image/png")

# @app.route("/callback", methods=["POST"])
# def callback():
#     signature = request.headers["X-Line-Signature"]
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # parse webhook body
#     try:
#         events = parser.parse(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     # if event is MessageEvent and message is TextMessage, then echo text
#     for event in events:
#         if not isinstance(event, MessageEvent):
#             continue
#         if not isinstance(event.message, TextMessage):
#             continue

#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text=event.message.text)
#         )

#     return "OK"


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

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if machine.mode == 0:
                send_text_message(event.reply_token, "請按按鈕或正確的輸入")
            else:
                send_text_message(event.reply_token, "密碼錯誤")
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
