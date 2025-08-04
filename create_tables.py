from database import engine, Base
from models import user, account, transaction

# Drop all tables
Base.metadata.drop_all(bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

print("Database tables recreated successfully!") 