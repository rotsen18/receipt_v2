import bcrypt
from sqlalchemy.orm import Session

from apps.auth import models, schemas


def hash_password(password: str):
    """Generates a hashed version of the provided password."""
    pw = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    return db_user
