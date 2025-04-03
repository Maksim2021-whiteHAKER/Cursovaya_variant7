from sqlalchemy.orm import Session
from models.log import Log

def log_action(db: Session, user_id: int, action: str):
    """
    Записывает действие пользователя в лог.

    :param db: SQLAlchemy сессия.
    :param user_id: ID пользователя, выполнившего действие.
    :param action: Описание действия.
    """
    try:
        log_entry = Log(user_id=user_id, action=action)
        db.add(log_entry)
        db.commit()
        print(f"Лог записан: user_id={user_id}, action={action}")
    except Exception as e:
        db.rollback()
        print(f"Ошибка при записи лога: {e}")