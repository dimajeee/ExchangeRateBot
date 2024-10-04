from db.models import User
from sqlalchemy.orm import Session

def save_user_name(telegram_id: int, name: str, db: Session):
    """Сохранение имени пользователя в базе данных."""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if user:
        user.name = name
    else:
        user = User(telegram_id=telegram_id, name=name)
        db.add(user)
    db.commit()

def get_user_name(telegram_id: int, db: Session):
    """Получение имени пользователя из базы данных."""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    return user.name if user else None
