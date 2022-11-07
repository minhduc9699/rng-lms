from apscheduler.schedulers.background import BackgroundScheduler
import telegram
from env.config import Config

sched = BackgroundScheduler(timezone='Asia/Ho_Chi_Minh')

@sched.scheduled_job('cron', day_of_week='0-4', hour='10')
def run():
  meeting_link = Config.get().meetingLink
  telegram.post(
    f'''Its time for scrum guys!
<a href='https://memegenerator.net/img/instances/76612783/oh-yes-its-meeting-time-.jpg'>&#8205</a>
link meeting: {meeting_link}''',
    chat_id=-466348665,
    mode='HTML'
  )
