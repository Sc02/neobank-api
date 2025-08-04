from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.account import create_account_for_user
from schemas.account import AccountResponse
from models.user import User
from routes.user import get_current_user  # your JWT auth dependency

router = APIRouter(prefix="/account", tags=["Account"])

@router.post("/", response_model=AccountResponse)
def create_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.account:
        raise HTTPException(status_code=400, detail="Account already exists.")
    return create_account_for_user(current_user, db)

@router.get("/", response_model=AccountResponse)
def get_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = current_user.account
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
    return account
