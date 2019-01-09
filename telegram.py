import requests
import datetime

def post(text):
  url = "https://api.telegram.org/bot776713603:AAETUPFQV52_tQl0KVSxeYGETro4f8mpUps/sendMessage"
  data = {
    "chat_id": -373819266,
    "text": text,
    "parse_mode": "Markdown",
  }
  return requests.post(url, json=data)

if __name__ == "__main__":
  r = post("Hello from *tk-police*, now is {0}".format(datetime.datetime.now()))
  print(r)