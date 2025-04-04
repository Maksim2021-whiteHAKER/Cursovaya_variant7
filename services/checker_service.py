from models.state import AquaState
from models.notification_settings import NotificationSettings
from services.email_sender import send_email

def check_device_thresholds(db):
    try:
        devices = db.query(AquaState).filter(AquaState.type != 'switch').all()
        
        for device in devices:
            notifications = db.query(NotificationSettings).filter(
                NotificationSettings.threshold.isnot(None),
                NotificationSettings.threshold <= device.value).all()

            
            for notify in notifications:
                message = f"Устройство {device.name}: значение {device.value} превысило порог {notify.threshold}"
                if notify.email: send_email(notify.email, "Метеостанция: тревога!", message)
    except Exception as e:
        print(f"Ошибка проверки порогов: {str(e)}")