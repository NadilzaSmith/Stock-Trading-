import requests
from twilio.rest import Client
import os

STOCK_NAME = "AMC"
COMPANY_NAME = "AMC Entertainment Holdings Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

api_key = "YCMQ6DKJEP1G08KL"
api_key_news = "cf3a27fe88354733a780c5d7ff162fc7"

parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": api_key
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
y_data = data_list[0]
close_price = y_data["4. close"]


day_before_y = data_list[1]
close_price_before_yesterday = day_before_y["4. close"]


gain_loss = (float(close_price) - float(close_price_before_yesterday))
money = None
if gain_loss > 0:
    money = "🤑"
else:
    money = "😭"


gain_loss_percent = round(gain_loss / float(close_price)) * 100


if abs(gain_loss_percent) > 2:
    parameters_news = {
        "apiKey": api_key_news,
        "qInTitle":COMPANY_NAME,

    }
    response_news = requests.get(NEWS_ENDPOINT, params=parameters_news)
    data_news = response_news.json()["articles"]
    slice_data = data_news[:3]
    print(slice_data)

    menssage = [f"{STOCK_NAME}: {money}{gain_loss_percent}%\nHeadline:{data_news['title']}.\nBrief: {data_news['description']}" for data_news in slice_data]


    account_sid = "ACc0cbc801fafef3f9ab2b77635b20d350"
    auth_token = "8bb217050192d37b3c73c3a84bdb9705"
    client = Client(account_sid, auth_token)

    for articles in menssage:
        message = client.messages.create(
          body=articles,
          from_="+12562557703",
          to="+17707907932"
        )

