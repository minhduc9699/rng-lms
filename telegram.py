import requests
import datetime

def post(text, chat_id=-325010757, mode=None):
  url = "https://api.telegram.org/bot1181085197:AAEzkEZF8DNckOZZrxdHzZqh8w_xrnsu-JQ/sendMessage"
  data = {
    "chat_id": chat_id,
    "text": text,
    "parse_mode": mode if mode is not None else "Markdown",
  }
  return requests.post(url, json=data)

if __name__ == "__main__":
  r = post("Hello from *tk-police*, now is {0}".format(datetime.datetime.now()))
  print(r)
