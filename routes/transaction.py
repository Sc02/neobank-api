from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.transaction import Transaction
from models.account import Account
from routes.user import get_current_user
from schemas.transaction import TransactionCreate, TransactionResponse, TransferCreate
from services.transaction import create_transaction, create_transfer

from typing import List

router = APIRouter(prefix="/transaction", tags=["Transaction"])

@router.post("/transaction", response_model=TransactionResponse)
def make_transaction(
    txn: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = current_user.account
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
    return create_transaction(db, account, txn.amount, txn.type, txn.category)

@router.post("/transfer", response_model=TransactionResponse)
def make_transfer(
    transfer: TransferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = current_user.account
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
    return create_transfer(db, account, transfer.destination_user_id, transfer.amount, transfer.category)

@router.get("/transaction", response_model=List[TransactionResponse])
def get_transaction_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = db.query(Account).filter(Account.user_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")

    transactions = db.query(Transaction).filter(
        Transaction.account_id == account.id
    ).order_by(Transaction.timestamp.desc()).all()

    return transactions