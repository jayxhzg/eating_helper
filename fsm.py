from transitions.extensions import GraphMachine
from datetime import datetime

from utils import *
from linebot.models import (
    MessageTemplateAction,
    LocationMessage
)

class TocMachine(GraphMachine):
    search_keyword = {}
    search_data = {}
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_menu(self, event):
        if not isinstance(event.message, TextMessage):
            return False
        instruction = ["menu", "主選單"]
        text = event.message.text
        return text.lower() in instruction
    
    def is_going_to_description(self, event):
        if not isinstance(event.message, TextMessage):
            return False
        instruction = ["description", "使用說明"]
        text = event.message.text
        return text.lower() in instruction

    def is_going_to_select_type(self, event):
        if not isinstance(event.message, TextMessage):
            return False
        text = event.message.text
        return text == "開始使用"
    
    def is_going_to_select_location(self, event):
        if not isinstance(event.message, TextMessage):
            return False
        text = event.message.text       
        if self.state == "menu" and text == "餐廳":
            self.search_keyword["type"] = "restaurant"
            return True
        elif self.state == "select_type":
            self.search_keyword["type"] = text
            return True
        return False

    def is_going_to_show_result(self, event):        
        return isinstance(event.message, LocationMessage)

    def is_going_to_select_detail(self, event):
        text = event.message.text
        try:
            num = int(text)
            return 1 <= num <= len(self.search_data["results"])
        except:
            return False

    def on_enter_description(self, event):
        print("state : description")
        msg = "我是你的吃貨小幫手😊\n讓我來幫你決定吃什麼吧~\n依序告訴我\n食物的類型、你所在的位置\n我就能找到周圍3公里的餐廳🍽️\n最多只會顯示20筆資料\n目前打烊的店家我會過濾掉喔~\n輸入menu或是主選單\n可隨時返回主選單重新設定"
        msg = TextSendMessage(msg)
        act = TemplateSendMessage(
            alt_text = "返回主選單",
            template = ButtonsTemplate(
                title = "返回主選單",
                text = "點選按鈕返回主選單",
                actions=  [MessageTemplateAction(
                    label="返回主選單",
                    text="主選單",
                    ),
                ]
            )
        )
        arr = [msg, act]
        reply_token = event.reply_token
        send_message(reply_token, arr)

    def on_enter_menu(self, event):
        print("state : description")
        action = [
            MessageTemplateAction(
                label="使用說明",
                text="使用說明",
            ),
            MessageTemplateAction(
                label="開始使用",
                text="開始使用",
            ),
            MessageTemplateAction(
                label="可以吃就好",
                text="餐廳",
            ),
        ]
        msg = button_template_message("吃貨小幫手說明", "吃飯GOGO", "按下\"開始使用\"即可選擇餐點種類\n按下\"可以吃就好\"則不限定種類\n", action)
        reply_token = event.reply_token
        send_message(reply_token, msg)

    def on_enter_select_type(self, event):
        print("state : select type")
        text = "你想吃什麼?\n可點選以下的按鈕或自行輸入"
        text = TextSendMessage(text)
        action = [
            MessageTemplateAction(
                label="便當",
                text="便當",
            ),
            MessageTemplateAction(
                label="漢堡",
                text="漢堡",
            ),
            MessageTemplateAction(
                label="飲料",
                text="飲料",
            ),
            MessageTemplateAction(
                label="甜點",
                text="甜點",
            ),
        ]
        msg = [text, button_template_message("餐點種類", "餐點種類", "點選以下的選項或是自行輸入", action)]
        reply_token = event.reply_token
        send_message(reply_token, msg)

    def on_enter_select_location(self, event):
        print("state : select location")
        reply_token = event.reply_token
        text = "請使用左下角的\"+\"號告訴我你的位置"
        text = TextSendMessage(text)
        send_message(reply_token, text)

    def on_enter_show_result(self, event):
        print("state : show result")
        self.search_keyword["location"] = [event.message.latitude, event.message.longitude]        
        print(f"search_keyword : {self.search_keyword}")
        self.search_data = search_info(self.search_keyword["location"], self.search_keyword["type"])
        data = self.search_data["results"]
        if self.search_data["status"] == "OK":
            msg = f"共有{len(data)}間餐廳(輸入編號查看詳細資料):"          
            for index, result in enumerate(data):
                msg = msg + f"\n{index + 1}. {result['name']}" 
            msg = TextSendMessage(msg)         
        else:# no result 
            msg = button_template_message("找不到結果", "找不到結果", "返回主選單重新搜尋", [MessageTemplateAction(label="返回主選單", text="主選單",)])             
        reply_token = event.reply_token
        send_message(reply_token, msg)
    
    def on_enter_select_detail(self, event):
        print("state : select detail")
        index = int(event.message.text) - 1
        data = self.search_data["results"][index] #店家的簡短資料
        # 搜尋店家的詳細資料
        place_id = data["place_id"]
        detail = get_detail_info(place_id)["result"] # 店家的詳細資料
        photo_reference = detail["photos"][0]["photo_reference"]
        name = data["name"] if len(data["name"]) <= 35 else (data["name"][:35] + "...")
        text = f"⭐:{detail['rating']}\n🕛:{detail['opening_hours']['weekday_text'][datetime.today().weekday()]}"
        # 搜尋的結果
        location = carousel_column(get_photo(photo_reference), name, text, "吃這間", detail["url"])
        result_msg = carousel_template_message("搜尋結果", [location])        
        # 可選擇別間的說明
        button_msg = button_template_message("決定好了嗎?", "決定好了嗎?", "返回主選單或是輸入編號查看其他店家", [MessageTemplateAction(label="返回主選單", text="主選單",)])
        msg = [result_msg, button_msg]
        reply_token = event.reply_token
        send_message(reply_token, msg)
