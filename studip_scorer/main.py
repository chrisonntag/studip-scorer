import requests
from requests.auth import HTTPBasicAuth
import getpass

BASE_URL = 'https://studip.uni-passau.de/studip/api.php'
GET_PARAMS = '?again=yes&sso=shib'

username = input('Enter your username:')
password = getpass.getpass('Enter your password:')

response = requests.get(BASE_URL + '/user' + GET_PARAMS, auth=HTTPBasicAuth(username, password))

if response.status_code == 200:
    print(response.content)
else:
    print(response.content)

