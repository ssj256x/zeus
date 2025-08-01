import hashlib
import os
import webbrowser
from pathlib import Path
from typing import Literal

import requests
from dotenv import load_dotenv
from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws

from broker.fyers.api_error_codes import TOKEN_EXPIRED, INVALID_TOKEN, TOKEN_AUTH_FAILED, TOKEN_INVALID_OR_EXPIRED


def _get_token(token_type: Literal['access', 'refresh']):
    match token_type:
        case 'access':
            with open(f'{base}/access', 'r') as f:
                return f.read()
        case 'refresh':
            with open(f'{base}/refresh', 'r') as f:
                return f.read()
        case _:
            raise ValueError('Invalid token type')


def _save_token_to_file(token: str, token_type: Literal['access', 'refresh']):
    match token_type:
        case 'access':
            with open(f'{base}/access', 'w') as f:
                return f.write(token)
        case 'refresh':
            with open(f'{base}/refresh', 'w') as f:
                return f.write(token)
        case _:
            raise ValueError('Invalid token type')


def _is_token_valid(resp: dict) -> bool:
    return int(resp['code']) not in {TOKEN_EXPIRED, INVALID_TOKEN, TOKEN_AUTH_FAILED, TOKEN_INVALID_OR_EXPIRED}


def init_broker():
    # fetch profile and see if the response is a success
    global access_token
    access_token = _get_token('access')
    resp = get_fyers_model().get_profile()

    if _is_token_valid(resp):
        print('Token Valid!')
        return
    else:
        print('Token Invalid!')
        print(resp)

    # try with refresh token
    access_token = fetch_access_token_using_refresh_token()

    if access_token is not None:
        _save_token_to_file(access_token, 'access')
        print('Token Refreshed!')
        return

    # Generate new auth code and refresh token

    redirect_url = session.generate_authcode()
    webbrowser.open(redirect_url)

    input_auth_token = input('Enter Auth Token: ')

    session.set_token(input_auth_token)
    token_resp = session.generate_token()

    access_token = token_resp['access_token']
    refresh_token = token_resp['refresh_token']

    _save_token_to_file(access_token, 'access')
    _save_token_to_file(refresh_token, 'refresh')


def fetch_access_token_using_refresh_token() -> str | None:
    text = f"{os.getenv('CLIENT_ID')}:{os.getenv('SECRET_KEY')}"
    hash_str = hashlib.sha256(text.encode('utf-8')).hexdigest()

    req = {
        'grant_type': 'refresh_token',
        'appIdHash': hash_str,
        'refresh_token': _get_token('refresh'),
        'pin': os.getenv('PIN')
    }

    resp = requests.post(
        url='https://api-t1.fyers.in/api/v3/validate-refresh-token',
        json=req
    )

    if resp.status_code != 200:
        print('Refresh Token Failed!')
        print(resp)
        return None

    return resp.json()['access_token']


def get_fyers_data_socket(**kwargs):
    _instance = None

    def get_instance() -> data_ws.FyersDataSocket:
        nonlocal _instance

        if _instance is None:
            _instance = data_ws.FyersDataSocket(
                access_token=access_token,
                log_path=kwargs.get('log_path', './logs'),
                litemode=kwargs.get('litemode', False),
                write_to_file=kwargs.get('write_to_file', False),
                on_connect=kwargs['on_connect'],
                on_error=kwargs['on_error'],
                on_close=kwargs['on_close'],
                on_message=kwargs['on_message'],
            )
        return _instance

    return get_instance()


def get_fyers_model() -> fyersModel.FyersModel:
    _instance = None

    def get_instance() -> fyersModel.FyersModel:
        nonlocal _instance
        if _instance is None:
            _instance = fyersModel.FyersModel(
                token=access_token,
                is_async=False,
                client_id=os.getenv("CLIENT_ID"),
                log_path=f'{base}/logs'
            )

        return _instance

    return get_instance()


access_token = ''
load_dotenv()
base = Path(__file__).parent

session = fyersModel.SessionModel(
    client_id=os.getenv('CLIENT_ID'),
    redirect_uri='https://trade.fyers.in/api-login/redirect-uri/index.html',
    response_type='code',
    state='ssj256x',
    secret_key=os.getenv('SECRET_KEY'),
    grant_type='authorization_code'
)
