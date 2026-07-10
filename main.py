from playwright.sync_api import sync_playwright
import os
import requests
import traceback


TOKEN=os.environ["TELEGRAM_TOKEN"]
CHAT_ID=os.environ["TELEGRAM_CHAT_ID"]


def send(msg):

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id":CHAT_ID,
            "text":msg[:4000]
       
