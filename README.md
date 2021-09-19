# Trend Analysis with Financial Data Correlation Coefficient
The Django Rest Framework API application works with TweleData API to provide Correlation Coefficient as well as Percentage Change and and HLOC data for Trend Analysis.
The App hopes to use Machine Learning to perform Trend Analysis. A frontend is coming soon after I learn react.

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


