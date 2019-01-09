from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import datetime

import firebase
import telegram

sched = BlockingScheduler(timezone="Asia/Ho_Chi_Minh")

@sched.scheduled_job('interval', minutes=3)
def timed_job():
  print("Hello from *tk-police*, now is {0}".format(datetime.datetime.now()))

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=14)
def scheduled_job():
  telegram.post(firebase.sprint_message())

if __name__ == "__main__":
  sched.start()