from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from database import Base
from sqlalchemy.orm import relationship

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    account_id = Column(Integer, ForeignKey("accounts.id"))  # NEW: Link to account
    from_user = Column(Integer, ForeignKey("users.id"), nullable=True)
    to_user = Column(Integer, ForeignKey("users.id"), nullable=True)

    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # 'deposit', 'withdrawal', 'transfer'
    category = Column(String, default="general")
    timestamp = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", backref="transactions")
