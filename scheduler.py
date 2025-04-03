from apscheduler.schedulers.background import BackgroundScheduler
from services.checker_service import check_device_thresholds
from app_data.definitions import my_connect
from sqlalchemy.orm import Session

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    def check_job():
        with Session(bind=my_connect) as db:
            check_device_thresholds(db)
    
    scheduler.add_job(check_job, 'interval', minutes=5)
    scheduler.start()
    