from transitions.extensions import GraphMachine
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.mode = 0
        self.is_front_door_open = 0
        self.is_left_safe_open = 0
        self.is_right_bag_open = 0
        self.is_right_box_open = 0
        self.is_back_picture_open = 0
        self.number_of_turns = 0
        self.number_of_open = 0

    def is_open_door(self, event):
        text = event.message.text
        return text.lower() == "開門"

    def is_restart(self, event):
        text = event.message.text
        return text.lower() == "restart" or text.lower() == "重新開始"

    def is_going_to_front(self, event):
        text = event.message.text
        return text.lower() == "開始"
    
    def is_turning_to_left(self, event):
        text = event.message.text
        if text.lower() == "l":
            self.number_of_turns += 1
            return True
        return False

    def is_turning_to_right(self, event):
        text = event.message.text
        if text.lower() == "r":
            self.number_of_turns += 1
            return True
        return False
    
    def is_turning_to_back(self, event):
        text = event.message.text
        if text.lower() == "b":
            self.number_of_turns += 1
            return True
        return False

    def is_going_back(self, event):
        text = event.message.text
        return text.lower() == "返回"

    def is_going_to_front_door(self, event):
        text = event.message.text
        return text.lower() == "調查門"

    def is_going_to_front_window(self, event):
        text = event.message.text
        return text.lower() == "調查窗戶"

    def is_going_to_left_safe(self, event):
        text = event.message.text
        return text.lower() == "調查保險箱"

    def is_going_to_left_wall(self, event):
        text = event.message.text
        return text.lower() == "調查牆上的方塊"

    def is_going_to_right_bag(self, event):
        text = event.message.text
        return text.lower() == "調查黑色書包"

    def is_going_to_right_box(self, event):
        text = event.message.text
        return text.lower() == "調查橘色箱子"

    def is_going_to_back_picture(self, event):
        text = event.message.text
        return text.lower() == "調查畫"

    def is_going_to_back_calendar(self, event):
        text = event.message.text
        return text.lower() == "調查月曆"

    def is_going_to_back_book(self, event):
        text = event.message.text
        return text.lower() == "調查書"

    def is_front_door_correct(self, event):
        text = event.message.text
        if self.is_front_door_open == 1:
            return False
        self.number_of_open += 1
        if text.lower() == "3765":
            self.is_front_door_open = 1
            return True
        return False

    def is_left_safe_correct(self, event):
        text = event.message.text
        if self.is_left_safe_open == 1:
            return False
        self.number_of_open += 1
        if text.lower() == "3742":
            self.is_left_safe_open = 1
            return True
        return False

    def is_right_bag_correct(self, event):
        text = event.message.text
        if self.is_right_bag_open == 1:
            return False
        self.number_of_open += 1
        if text.lower() == "319":
            self.is_right_bag_open = 1
            return True
        return False

    def is_right_box_correct(self, event):
        text = event.message.text
        if self.is_right_box_open == 1:
            return False
        self.number_of_open += 1
        if text.lower() == "6928":
            self.is_right_box_open = 1
            return True
        return False

    def is_back_picture_correct(self, event):
        text = event.message.text
        if self.is_back_picture_open == 1:
            return False
        self.number_of_open += 1
        if text.lower() == "705":
            self.is_back_picture_open = 1
            return True
        return False

    def on_enter_start(self, event):
        # initial
        self.mode = 0
        self.is_front_door_open = 0
        self.is_left_safe_open = 0
        self.is_right_bag_open = 0
        self.is_right_box_open = 0
        self.is_back_picture_open = 0
        self.number_of_turns = 0

        print("I'm entering start")
        title = '密室逃脫'
        text = '醒來發現自己在教室當中...\n這個教室四四方方的...\n有什麼辦法可以出去呢...'
        btn = [
            MessageTemplateAction(
                label = '開始',
                text ='開始'
            )
        ]
        url = 'https://img.onl/sKJtb7'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_front(self, event):
        print("I'm entering front")
        title = '要做什麼？'
        text = '向右轉請輸入"r"\n向左轉請輸入"l"\n向後轉請輸入"b"'
        btn = [
            MessageTemplateAction(
                label = '調查門',
                text ='調查門'
            ),
            MessageTemplateAction(
                label = '調查窗戶',
                text = '調查窗戶'
            )
        ]
        url = 'https://img.onl/tGn9hu'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_front_door(self, event):
        self.mode = 1
        print("I'm entering front_door")
        title = '門鎖起來了，旁邊有密碼鎖。'
        text = '……教室以前有裝這種鎖嗎？\n請輸入密碼(4個數字)'
        btn = [
            MessageTemplateAction(
                label = '返回',
                text = '返回'
            )
        ]
        url = 'https://img.onl/qQi8w2'
        if(self.is_front_door_open == 1):
            self.mode = 0
            title = '門打開了。'
            text = '終於可以回家了！'
            url = 'https://img.onl/TKiloZ'
            btn = [
            MessageTemplateAction(
                label = '開門',
                text = '開門'
            )
        ]
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_front_window(self, event):
        print("I'm entering front_window")
        title = '窗戶打開了，仔細看外面是一面藍色的牆。'
        text = '……那為什麼要裝窗戶？'
        btn = [
            MessageTemplateAction(
                label = '返回',
                text = '返回'
            )
        ]
        url = 'https://img.onl/jVu5jp'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_left(self, event):
        print("I'm entering left")
        title = '要做什麼？'
        text = '向右轉請輸入"r"\n向左轉請輸入"l"\n向後轉請輸入"b"'
        btn = [
            MessageTemplateAction(
                label = '調查保險箱',
                text ='調查保險箱'
            ),
            MessageTemplateAction(
                label = '調查牆上的方塊',
                text = '調查牆上的方塊'
            )
        ]
        url = 'https://img.onl/U8LkZf'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_left_safe(self, event):
        self.mode = 1
        print("I'm entering left_safe")
        title = '鎖起來了。'
        text = '請輸入密碼(4個數字)'
        btn = [
            MessageTemplateAction(
                label = '返回',
                text ='返回'
            )
        ]
        url = 'https://img.onl/sgfyx'
        if(self.is_left_safe_open == 1):
            self.mode = 0
            title = '保險箱打開了'
            text = '裡面有一些鉛筆。'
            url = 'https://img.onl/A9Sm3'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_left_wall(self, event):
        print("I'm entering left_wall")
        title = '是誰畫的？'
        text = ' '
        btn = [
            MessageTemplateAction(
                label = '返回',
                text ='返回'
            )
        ]
        url = 'https://img.onl/SsR50h'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_right(self, event):
        print("I'm entering right")
        title = '要做什麼？'
        text = '向右轉請輸入"r"\n向左轉請輸入"l"\n向後轉請輸入"b"'
        btn = [
            MessageTemplateAction(
                label = '調查黑色書包',
                text ='調查黑色書包'
            ),
            MessageTemplateAction(
                label = '調查橘色箱子',
                text = '調查橘色箱子'
            )
        ]
        url = 'https://img.onl/0eaa4j'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_right_bag(self, event):
        self.mode = 1
        print("I'm entering right_bag")
        title = '鎖起來了。'
        text = '請輸入密碼(3個數字)'
        btn = [
            MessageTemplateAction(
                label = '返回',
                text ='返回'
            )
        ]
        url = 'https://img.onl/IbazTb'
        if(self.is_right_bag_open == 1):
            self.mode = 0
            title = '黑色書包打開了。'
            text = '裡面是一些鉛筆。\n……有必要上鎖嗎?'
            url = 'https://img.onl/DqgUl5'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_right_box(self, event):
        self.mode = 1
        print("I'm entering right_box")
        title = '箱子外好像貼著什麼。'
        text = '請輸入密碼(4個數字)'
        btn = [
            MessageTemplateAction(
                label = '返回',
                text ='返回'
            )
        ]
        url = 'https://img.onl/CjQw7'
        if(self.is_right_box_open == 1):
            self.mode = 0
            title = '橘色箱子打開了'
            text = '裡面有一些鉛筆。'
            url = 'https://img.onl/vvFJsr'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_back(self, event):
        print("I'm entering back")
        title = '要做什麼？'
        text = '向右轉請輸入"r"\n向左轉請輸入"l"\n向後轉請輸入"b"'
        btn = [
            MessageTemplateAction(
                label = '調查畫',
                text ='調查畫'
            ),
            MessageTemplateAction(
                label = '調查月曆',
                text = '調查月曆'
            ),
            MessageTemplateAction(
                label = '調查書',
                text = '調查書'
            )
        ]
        url = 'https://img.onl/mPjLR6'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_back_picture(self, event):
        self.mode = 1
        print("I'm entering back_picture")
        title = '畫往旁邊滑開，後面有一個洞和上鎖的盒子。'
        text = '請輸入密碼(3個數字)'
        btn = [
            MessageTemplateAction(
                label = '返回',
                text ='返回'
            )
        ]
        url = 'https://img.onl/ZwBAa9'
        if(self.is_back_picture_open == 1):
            self.mode = 0
            title = '牆裡的盒子打開了'
            text = '裡面是一些鉛筆。'
            url = 'https://img.onl/eqy9t'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_back_calendar(self, event):
        print("I'm entering back_calendar")
        title = '說起來，為什麼暑假我會來學校？'
        text = ' '
        btn = [
            MessageTemplateAction(
                label = '返回',
                text ='返回'
            )
        ]
        url = 'https://img.onl/iU0OmL'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_back_book(self, event):
        print("I'm entering back_book")
        title = '書好像破了。'
        text = ' '
        btn = [
            MessageTemplateAction(
                label = '返回',
                text ='返回'
            )
        ]
        url = 'https://img.onl/wi0Tab'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_clearance(self, event):
        print("I'm entering clearance")
        title = '離開學校啦！'
        text = '獲得成就:暈頭轉向\n(你總共轉了'+str(self.number_of_turns)+'次)\n獲得成就:解碼達人ˊ\n(你總共嘗試了'+str(self.number_of_open)+'次密碼)'
        btn = [
            MessageTemplateAction(
                label = '重新開始',
                text ='重新開始'
            )
        ]
        url = 'https://img.onl/ZKN0of'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_exit_start(self, event):
        print("Leaving start")

    def on_exit_front(self, event):
        print("Leaving front")
    
    def on_exit_front_door(self, event):
        self.mode = 0
        print("Leaving front_door")

    def on_exit_left(self, event):
        print("Leaving left")

    def on_exit_left_safe(self, event):
        self.mode = 0
        print("Leaving left_safe")
    
    def on_exit_right(self, event):
        print("Leaving right")

    def on_exit_right_bag(self, event):
        self.mode = 0
        print("Leaving right_bag")

    def on_exit_right_box(self, event):
        self.mode = 0
        print("Leaving right_box")

    def on_exit_back(self, event):
        print("Leaving back")

    def on_exit_back_picture(self, event):
        self.mode = 0
        print("Leaving back_picture")

    

    
    

