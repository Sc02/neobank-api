from sqlalchemy.orm import Session
from models.transaction import Transaction
from models.account import Account
from models.user import User
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

def create_transfer(db: Session, source_account: Account, destination_user_id: int, amount: float, category: str = "transfer"):
    # Validate source account has sufficient balance
    if source_account.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    # Get destination user and their account
    destination_user = db.query(User).filter(User.id == destination_user_id).first()
    if not destination_user:
        raise HTTPException(status_code=404, detail="Destination user not found")
    
    destination_account = db.query(Account).filter(Account.user_id == destination_user_id).first()
    if not destination_account:
        raise HTTPException(status_code=404, detail="Destination user account not found")
    
    # Prevent self-transfer
    if source_account.id == destination_account.id:
        raise HTTPException(status_code=400, detail="Cannot transfer to your own account")
    
    try:
        # Debit source account
        source_account.balance -= amount
        
        # Credit destination account
        destination_account.balance += amount
        
        # Create transaction records for both accounts
        source_txn = Transaction(
            account_id=source_account.id,
            from_user=source_account.user_id,
            to_user=destination_user_id,
            amount=amount,
            type="transfer",
            category=category
        )
        
        destination_txn = Transaction(
            account_id=destination_account.id,
            from_user=source_account.user_id,
            to_user=destination_user_id,
            amount=amount,
            type="transfer",
            category=category
        )
        
        db.add(source_txn)
        db.add(destination_txn)
        db.commit()
        db.refresh(source_txn)
        
        return source_txn
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Transfer failed. Please try again.")
