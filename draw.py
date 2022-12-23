import matplotlib.pyplot as plt
import networkx as nx
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
states = machine.get_state()
transitions = machine.transitions
# 建立圖形
G = nx.DiGraph()

# 將狀態加入圖形
G.add_nodes_from(machine.states)

# 將轉移加入圖形
for transition in machine.transitions:
    G.add_edge(transition["source"], transition["dest"], label=transition["trigger"])

# 繪製圖形
pos = nx.drawing.nx_agraph.pyplot_layout(G, prog="dot")
nx.draw(G, pos, with_labels=True, arrows=True)
edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# 顯示圖形
plt.show()