def check_device_thresholds(db):
    try:
        devices = db.query(AquaState).filter(AquaState.type != 'switch').all()
        
        for device in devices:
            notifications = db.query(NotificationSettings).filter(
                NotificationSettings.device_id == device.id,
                NotificationSettings.threshold <= device.value
            ).all()
            
            for notify in notifications:
                message = f"Устройство {device.name}: значение {device.value} превысило порог {notify.threshold}"
                if notify.email:
                    send_email(notify.email, "Метеостанция: тревога!", message)
    except Exception as e:
        print(f"Ошибка проверки порогов: {str(e)}")