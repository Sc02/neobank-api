from fastapi import FastAPI
from database import engine, Base
from models import user
from routes import auth, user
from dotenv import load_dotenv
from routes import account  # import the new route file
from routes import transaction


load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(account.router)
app.include_router(transaction.router)

@app.get("/")
def root():
    return {"message": "NeoBank API is alive!"}
