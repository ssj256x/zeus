"""
Error Code -352 is defined twice with different error code.

Look under Common API Error Codes
https://myapi.fyers.in/docsv3#tag/Request-and-Response-Structure/paths/~1pet~1%7BpetId%7D/get
"""

TOKEN_EXPIRED = -8
INVALID_TOKEN = -15
TOKEN_AUTH_FAILED = -16
TOKEN_INVALID_OR_EXPIRED = -17
INVALID_PARAMETERS = -50
INVALID_ORDER_ID = -51
INVALID_POSITION_ID = -53
ORDER_REJECTED = -99
INVALID_SYMBOL = -300
INVALID_APP_ID = -352
NO_POSITION_TO_EXIT = -352
RATE_LIMIT_EXCEEDED = -429
INVALID_MULTI_LEG_INPUT = 400

ERROR_CODES = {
    -8: 'This error occurs when token is Expired',
    -15: 'This error occurs when Invalid token is provided',
    -16: 'This error occurs when server is unable to authenticate user token',
    -17: 'This error occurs when token is passed is either Invalid or Expired',
    -50: 'This error occurs when one or more invalid parameters are passed. The message field in the API response will include details about the specific invalid inputs.',
    -51: 'This error occurs when invalid Order ID is passed while fetching Orders or Order Modification',
    -53: 'This error occurs when invalid position ID is passed',
    -99: 'This error occurs when order placement get rejected with rejection message in the API response',
    -300: 'This error occurs when invalid symbol provided',
    -352: 'This error occurs when invalid App ID is provided',
    -429: 'This error occurs when the API rate limit is exceeded, either per second, minute, or day.',
    400: 'This error occurs in multi leg order placement when invalid input passed'
}
