from apscheduler.schedulers.background import BackgroundScheduler
import telegram

sched = BackgroundScheduler(timezone='Asia/Ho_Chi_Minh')

@sched.scheduled_job('cron', day_of_week='1-5', hour='10')
def run():
  telegram.post('Its time for scrum guys!', chat_id=-466348665)
