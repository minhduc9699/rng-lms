import requests

def post(data):
  url = "https://hooks.slack.com/services/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"

  return requests.post(url, json=data)

if __name__ == "__main__":
  data = {
      "text": "Hello from *tk-progress*, now is {0}".format(datetime.datetime.now())
  }
  r = post(data)
  print(r)