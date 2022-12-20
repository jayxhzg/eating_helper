import os
import json
import requests
from dotenv import load_dotenv

from linebot import LineBotApi, WebhookParser
from linebot.models import (
    MessageEvent, 
    TextMessage, 
    TextSendMessage, 
    LocationSendMessage, 
    TemplateSendMessage,
    ButtonsTemplate,
    CarouselColumn,
    CarouselTemplate,
    URITemplateAction
)

import googlemaps

load_dotenv()

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
google_api_key = os.getenv("GOOGLE_API_KEY", None)
line_bot_api = LineBotApi(channel_access_token)
gmaps = googlemaps.Client(key = google_api_key)

def send_text_message(reply_token, text):    
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
    return "OK"

def button_template_message(info, title, msg, action):
    message = TemplateSendMessage(
        alt_text = info,
        template = ButtonsTemplate(
            title = title,
            text = msg,
            actions= action
        )
    )
    return message

def carousel_column(image_url, title, text, label, uri):
    msg = CarouselColumn(
        thumbnail_image_url= image_url,
        title = title,
        text = text,
        actions=[
            URITemplateAction(
                label = label,
                uri = uri
            )
        ]
    )
    return msg

def carousel_template_message(info, columns):
    message = TemplateSendMessage(
        alt_text = info,
        template = CarouselTemplate(
            columns= columns
        )
    )
    return message

def send_message(reply_token, arr):    
    line_bot_api.reply_message(reply_token, arr)
    return "OK"

# 取得店家照片
def get_photo(photo_reference):
    url = f"https://maps.googleapis.com/maps/api/place/photo?photo_reference={photo_reference}&maxheight=200&key={google_api_key}"
    # response = requests.get(url)
    return url

# 取得店家的詳細資訊(在google maps的網址)
def get_detail_info(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&language=zh-TW&key={google_api_key}"
    response = requests.get(url).json()
    return response

# 搜尋附近的店家
def search_info(location, keyword):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location[0]},{location[1]}&keyword={keyword}&radius=3000&opennow=true&language=zh-TW&key={google_api_key}"
    response = requests.get(url).json()
    return response