# Trend Analysis with Financial Data
The Django Rest Framework API application works with TweleData API to provide Correlation Coefficient analysis as well as Daily Match Trend analysis using Percentage Change and HLOC data and finally Regression analysis.
The App hopes to use Machine Learning to perform Trend Analysis. A frontend is coming soon.

# Daily Match Trend
This section takes in a single ticker, Forex, Stock, Crypto, Index or Commodity and calculates the daily match trend with the HLOC, Percentage change/Actual Value Change and then returns the positive and negetive chang, along with the date and HLOC values.

The formula for the percentage change is:

Percentage change = last day - previous day / previous day * 100

e.g appl =  
0    154.07001
1    148.97000
2    149.55000
3    148.12000
4    149.09000
5    148.85001
6    146.06000

percentage change = 146.06000 - 148.85001 / 148.85001 * 100

Formula for change:

Change = percentage change * (user change / 100)

e.g user change = 5%

change = -1.87438 * (5/100)

positive change = change + percentage change
negative change = change - percentage change

## Requirements:
1. The Base Ticker = "ticker"
2. Number of Days specified by User = "numberOfDays"
3. The HLOC to be used for the analysis e.g OPEN, CLOSE, HIGH, LOW = "graphValue"
4. The percentage the User would like to use = "percentageChange"
5. The choice between Percentage Change or Actual Value change = "change_choice"

### Sample Request:
url: http://localhost:8000/v2/DMT 
Allow: GET
Content-Type: application/json

{
    "ticker": "EUR/NGN",
    "numberOfDays": 4,
    "graphValue": "open",
    "percentageChange": 20,
    "change_choice": "pctChange"
}

"graphValue": "open" or "close" or "high" or "low"

"change_choice": "pctChange" or "actChange"

### Expected Response Object: 

{
    "positive": [
        -0.4783135846461706,
        0.8316782694405411,
        -0.4452164234479472
    ],
    "negative": [
        -0.31887572309744705,
        0.5544521796270274,
        -0.29681094896529814
    ],
    "date": [
        {
            "datetime": "2021-09-17",
            "open": "484.76999",
            "high": "484.85999",
            "low": "484.76999",
            "close": "484.85999"
        },
        {
            "datetime": "2021-09-16",
            "open": "486.70999",
            "high": "486.70999",
            "low": "484.76999",
            "close": "484.76999"
        },
        {
            "datetime": "2021-09-15",
            "open": "483.35999",
            "high": "486.70999",
            "low": "483.35999",
            "close": "486.70999"
        },
        {
            "datetime": "2021-09-14",
            "open": "485.16000",
            "high": "485.16000",
            "low": "483.35999",
            "close": "483.35999"
        }
    ]
}

# Correlation Coefficient
This section takes in a single ticker, Forex, Stock, Crypto, Index or Commodity and compares it with all the others of the same type in the data base.
## Requirements:
1. The Base Ticker
2. The StartDate and EndDate
3. The HLOC to be used for the correlation e.g OPEN, CLOSE, HIGH, LOW
4. The Section to be correlalted with e.g Forex, Stock, Crypto, Index or Commodity NB This section might be deprecated.

### Sample Request:
url: http://localhost:8000/v1/stock 
Allow: GET
Content-Type: application/json

{
    "symbolValue": "aapl",
    "startdate": "2021-09-01",
    "enddate": "2021-09-15",
    "hloc": "close"
}

### Expected Response Object: 