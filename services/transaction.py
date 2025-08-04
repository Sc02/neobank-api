from sqlalchemy.orm import Session
from models.transaction import Transaction
from models.account import Account
from fastapi import HTTPException

def create_transaction(db: Session, account: Account, amount: float, type: str, category: str):
    if type == "withdrawal" and account.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    if type == "deposit":
        account.balance += amount
    elif type == "withdrawal":
        account.balance -= amount
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    txn = Transaction(
        account_id=account.id,
        amount=amount,
        type=type,
        category=category
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn
