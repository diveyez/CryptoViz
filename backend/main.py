import time

from fastapi import FastAPI, HTTPException, Path, Query, WebSocket
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import motor.motor_asyncio
import sys
sys.path.insert(1, './scripts')
import Scheduler as sc
from fastapi import FastAPI
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase
from starlette.requests import Request
from fastapi import BackgroundTasks
from typing import Optional

from flask import escape
from lib import DataHandler 
from lib import CryptoData

app = FastAPI()
# app.add_middleware(HTTPSRedirectMiddleware)
dataHandler = DataHandler.BinanceWrapper()
cryptoList = dataHandler.getcryptoSymbols()
cryptoData = CryptoData.CryptoDataReader()
client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
db = client["cryptoviz"]
collection = db["users"]
user_db = MongoDBUserDatabase(UserDB, collection)

auth_backends = [
    JWTAuthentication(secret=SECRET, lifetime_seconds=3600),
]


fastapi_users = FastAPIUsers(
    user_db, auth_backends, User, UserCreate, UserUpdate, UserDB, SECRET,
)
app.include_router(fastapi_users.router, prefix="/users", tags=["users"])



origins = [
    "http://localhost:3000", "ws://localhost:8000/api/crypto/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/crypto/{ticker}")
async def getCryptoInfo(ticker: str = Path(..., title="The Ticker of the Crypto to get")):
    ticker = escape(ticker)
    if(len(ticker)>5 and len(ticker) < 10 and ticker in cryptoList):
        for tether in dataHandler.tethers:
            tickerTemp = ticker.replace(tether,"")
            fullName = cryptoData.extract_name(tickerTemp)
            if(fullName):
                return {"fullName":fullName}
    raise HTTPException(status_code=404, detail="Ticker not found")

@app.websocket("/api/crypto/")
async def websocket_crypto_endpoint(websocket: WebSocket):
    await websocket.accept()
    defaultIntervals = dataHandler.klines
    cryptoData = None
    # cryptoData = dataHandler.retrieveCryptoData(ticker,timeInterval)
    # cryptoData = cryptoData[(cryptoData['timestamp']>"2020-03-15 02:37:00") & (cryptoData['timestamp']<"2020-03-15 02:41:00")]
    # cryptoData = cryptoData[["timestamp", "close", "rsi","ema","sma","lbb","ubb","mbb"]]
    while True: 
        # data = data["2020-03-05":"2020-03-14"]
        # print(data
        data = await websocket.receive_json()
        print("data is ", data)
        if(data["action"] == 'Update'):
            if("minDate" in data.keys() and "maxDate" in data.keys() and "timeInterval" in data.keys() and escape(data['timeInterval']) in defaultIntervals and "ticker" in data.keys() and escape(data['ticker']) in cryptoList ):
                mindate = escape(data["minDate"])
                maxDate = escape(data["maxDate"])
                ticker = escape(data['ticker'])
                timeInterval = escape(data['timeInterval'])
                cryptoData = dataHandler.retrieveCryptoData(ticker,timeInterval)
                cryptoData = cryptoData[(cryptoData['timestamp']>mindate) & (cryptoData['timestamp']<maxDate)]
                cryptoData = cryptoData[["timestamp", "close", "rsi","ema","sma","lbb","ubb","mbb"]]
                await websocket.send_json(cryptoData.to_json(orient='records'))
            else:
                await websocket.close(code=1000)


background_tasks_running = False
DATABASE_URL = "mongodb+srv://admin:RERWw4ifyreSYuiG@cryptoviz-f2rwb.azure.mongodb.net/test?retryWrites=true&w=majority"
SECRET = "|X|Th!5iS@S3CR3t|X|"

class User(models.BaseUser):
    watchlist: Optional[list] = []

class UserCreate(User, models.BaseUserCreate):
    watchlist: list

class UserUpdate(User, models.BaseUserUpdate):
    watchlist: Optional[list]

class UserDB(User, models.BaseUserDB):
    watchlist: list



@fastapi_users.on_after_register()
def on_after_register(user: User, request: Request):
    print(f"User {user.id} has registered.")


@fastapi_users.on_after_forgot_password()
def on_after_forgot_password(user: User, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")

@app.get("/")
async def root(background_tasks: BackgroundTasks):
    global background_tasks_running
    if not background_tasks_running:
        background_tasks_running = True
        background_tasks.add_task(sc.schedule_tasks)
    return {"message": "Hello World"}
