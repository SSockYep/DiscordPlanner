import requests
from DiscordPlanner.constants import *


def exchange_code(code, redirect_uri):
    print(redirect_uri)
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'scope': 'identify guilds'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' %
                      API_ENDPOINT, data=data, headers=headers)
    r.raise_for_status()
    return r.json()


def get_guild_info(token_type, token):
    headers = {
        'Authorization': token_type + ' ' + token
    }
    r = requests.get('%s/users/@me/guilds' % (API_ENDPOINT), headers=headers)
    r.raise_for_status()
    return r.json()


def get_user_info(token_type, token):
    headers = {
        'Authorization': token_type + ' ' + token
    }
    r = requests.get('%s/users/@me' % (API_ENDPOINT), headers=headers)
    r.raise_for_status()
    return r.json()
