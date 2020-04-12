# Project Title: CryptoViZ
#### Team Members: Mohan Vashist (vashistm, 1004260514), Mrigank Mehta (mrigankmg, 1001309014)

## Project Proposal

### Tech Stack

- MongoDB Atlas - NoSQL database used to store and retrieve the latest crypto information, and user login information.
- Python - Creating CLI’s which are used for calculations, and data science processing.
- React - A frontend JS library used to maintain states. Used due to frequent changes in our app page(s).
- Express.js - Node.js web application framework which will be used for routing and middleware purposes.
- Node.js - Used for running, and scheduling CLI.
- Heroku - Used for web app deployment.

### Description

We would like to create an application similar to https://finviz.com/, but focuses on crypto currencies (since finviz has no data on crypto currencies). We will focus on one crypto currency exchange which will be Binance, due to the fact that it is the largest crypto currency exchange (in terms of volume traded per day). Our application will focus on performing technical analysis, specifically, calculating and displaying signals, technical indicators and top gainers/losers.

https://www.investopedia.com/terms/t/trade-signal.asp
https://www.investopedia.com/terms/t/technicalindicator.asp	

### Key Features that will be completed by the Beta version

- Integrating the Binance API to fetch historical and current market data
- Calculating Signals for each cryptocurrencies if they exist
  - Signals that should be channel up, channel down, trendline support and trendline resistance
- Calculate/find top gainers and losers 
- Automatic data retrieval and data processing for all crypto currencies (one trading pair per crypto currency only) listed     in Binance in the background 

### Key features that will be complete by the Final version

- User will be able to save crypto currencies to their watchlist - allowing for users to easily monitor specific crypto currencies 
- Calculating technical indicators
- Technical indicators that will be calculated are RSI, EMA, SMA, Bollinger bands, ADX
- Graphs which are able to display crypto currency price, volume, technical indicators, and signals(if they exists) for         crypto currencies listed on Binance

### Top 5 technical challenges

- Learning React
- Displaying interactive graphs 
- Application deployment
- Integrating python scripts with Node.js.
- Finding efficient ways to concurrently run processes to retrieve and update data 
- Calculating Signals for crypto currencies  

## REST API Documentation

### Authentication API

#### Create

- description: sign up a new user
- request: `POST /api/users/register`
    - content-type: `application/json`
    - body: object
      - email: (string) email for new user
      - password: (string) password for new user
      - first_name: (string) first name for new user
      - last_name: (string) last name for new user
- response: 201
    - content-type: `application/json`
    - body: object
      - id: (string) id for new user
      - email: (string) email for new user
      - is_active: (boolean) user active status
      - is_superuser: (boolean) is user a superuser
      - watchlist: (list) new user's crypto watchlist
      - first_name: (string) first name for new user
      - last_name: (string) last name for new user
- response: 400
    - content-type: `application/json`
    - body: object
      - detail: (string) REGISTER_USER_ALREADY_EXISTS
- response: 422
    - content-type: `application/json`
    - body: object
      - detail: (list of objects)
        - loc: (string) location of error in request body
        - msg: (string) error message
        - type: (string) error type

``` 
$ curl -X POST 
       -H "accept: application/json"
       -H "Content-Type: application/json"
       -d '{"email":"example@example.com","password":"password","first_name":"example","last_name":"example"}'
       localhost:8000/api/users/register
```

- description: sign in a user
- request: `POST /api/users/login/cookie`
    - content-type: `application/x-www-form-urlencoded`
    - body: string
      - username=username&password=password
- response: 200
- response: 400
    - content-type: `application/json`
    - body: object
      - detail: (string) LOGIN_BAD_CREDENTIALS
- response: 422
    - content-type: `application/json`
    - body: object
      - detail: (list of objects)
        - loc: (string) location of error in request body
        - msg: (string) error message
        - type: (string) error type

``` 
$ curl -X POST 
       -c cookie.txt
       -H "accept: application/json"
       -H "Content-Type: application/x-www-form-urlencoded"
       -d "username=example@example.com&password=password"
       localhost:8000/api/users/login/cookie
```

- description: sign out a user
- request: `POST /api/users/logout/cookie`
- response: 200
- response: 401
    - content-type: `application/json`
    - body: object
      - detail: (string) Unauthorized

``` 
$ curl -X POST 
       -b cookie.txt
       -c cookie.txt
       localhost:8000/api/users/logout/cookie
```

#### Read

- description: get logged in user information
- request: `GET /api/users/me`
- response: 200
    - content-type: `application/json`
    - body: object
      - id: (string) id for logged in user
      - email: (string) email for logged in user
      - is_active: (boolean) logged in user active status
      - is_superuser: (boolean) is logged in user a superuser
      - watchlist: (list) logged in user's crypto watchlist
      - first_name: (string) first name for logged in user
      - last_name: (string) last name for logged in user
- response: 401
    - content-type: `application/json`
    - body: object
      - detail: (string) Unauthorized

``` 
$ curl -b cookie.txt
       localhost:8000/api/users/me/
```

#### Update

- description: update logged in user
- request: `PATCH /api/users/me`
    - content-type: `application/json`
    - body: object
      - id: (string) new id for logged in user
      - email: (string) new email for logged in user
      - is_active: (boolean) logged in user new active status
      - is_superuser: (boolean) logged in user new superuser status
      - watchlist: (list) logged in user's new crypto watchlist
      - first_name: (string) new first name for logged in user
      - last_name: (string) new last name for logged in user
- response: 200
    - body: object
      - id: (string) id for new user
      - email: (string) email for new user
      - is_active: (boolean) user active status
      - is_superuser: (boolean) is user a superuser
      - watchlist: (list) new user's crypto watchlist
      - first_name: (string) first name for new user
      - last_name: (string) last name for new user
- response: 401
    - content-type: `application/json`
    - body: object
      - detail: (string) Unauthorized
- response: 422
    - content-type: `application/json`
    - body: object
      - detail: (list of objects)
        - loc: (string) location of error in request body
        - msg: (string) error message
        - type: (string) error type

``` 
$ curl -X PATCH
       -H "Content-Type: application/json"
       -b cookie.txt
       -d '{"first_name": "example"}'
       localhost:8000/api/users/me/
```

### Crypto API

#### Read

- description: get top (max 10) gainers
- request: `GET /api/gainers/[?time=1]`
- response: 200
    - content-type: `application/json`
    - body: (object)
      - gainers: (list of objects)
        - symbol: crypto symbol
        - rank: crypto rank
        - market_cap: market cap of crypto
        - price: price of crypto
        - volume: crypto volume
        - percent: crypto gain percentage
- response: 400
    - content-type: `application/json`
    - body: Invalid time.
- response: 422
    - content-type: `application/json`
    - body: object
      - detail: (list of objects)
        - loc: (string) location of error in request body
        - msg: (string) error message
        - type: (string) error type

``` 
$ curl -H "Content-Type: application/json"
       localhost:8000/api/gainers/
```

- description: get top (max 10) losers
- request: `GET /api/losers/[?time=1]`
- response: 200
    - content-type: `application/json`
    - body: (object)
      - gainers: (list of objects)
        - symbol: crypto symbol
        - rank: crypto rank
        - market_cap: market cap of crypto
        - price: price of crypto
        - volume: crypto volume
        - percent: crypto loss percentage
- response: 400
    - content-type: `application/json`
    - body: Invalid time.
- response: 422
    - content-type: `application/json`
    - body: object
      - detail: (list of objects)
        - loc: (string) location of error in request body
        - msg: (string) error message
        - type: (string) error type

``` 
$ curl -H "Content-Type: application/json"
       localhost:8000/api/losers/
```

- description: get top (max 10) losers
- request: `GET /api/crypto/tickerInfo/{ticker}`
  - path parameter: ticker
    - The ticker of the crypto currency you would like to retrieve more info from
- response: 200
    - content-type: `application/json`
    - body: (object)
      - fullName: full name of the crypto currency  (e.g for /api/crypto/tickerInfo/BTCUSDT, fullName would be Bitcoin)
- response: 404
    - content-type: `application/json`
    - detail: "Ticker not found"


``` 
curl --location --request GET 'localhost:8000/api/crypto/tickerInfo/BTCUSDT'
```

- description: retrieve current UTC time
- request: `GET /time`
- response: 200
    - content-type: `text/plain`
    - body: (str)
      - currentUTCTime


``` 
curl --location --request GET 'localhost:8000/time'
```


- description: get top (max 10) losers
- request: `GET /api/crypto/tickerInfo/{ticker}`
  - path parameter: ticker
    - The ticker of the crypto currency you would like to retrieve more info from
- response: 200
    - content-type: `application/json`
    - body: (object)
      - fullName: full name of the crypto currency  (e.g for /api/crypto/tickerInfo/BTCUSDT, fullName would be Bitcoin)
- response: 404
    - content-type: `application/json`
    - detail: "Ticker not found"

``` 
curl --location --request GET 'localhost:8000/time'
```
