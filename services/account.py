from sqlalchemy.orm import Session
from models.account import Account
from models.user import User

def create_account_for_user(user: User, db: Session):
    account = Account(user_id=user.id, balance=0.0)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account
