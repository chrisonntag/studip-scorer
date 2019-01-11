import re
import urllib.parse as urlparse
import warnings
from datetime import datetime
from typing import Optional

import attr
from bs4 import BeautifulSoup


def parse_login_form(html):
    soup = BeautifulSoup(html, 'lxml')

    for form in soup.find_all('form'):
        if 'action' in form.attrs:
            return form.attrs['action']
    raise ParserError("Could not find login form", soup)


def parse_saml_form(html):
    soup = BeautifulSoup(html, 'lxml')
    saml_fields = ['RelayState', 'SAMLResponse']
    form_data = {}
    p = soup.find('p')
    if 'class' in p.attrs and 'form-error' in p.attrs['class']:
        raise ParserError("Error in Request: '%s'" % p.text, soup)
    for input in soup.find_all('input'):
        if 'name' in input.attrs and 'value' in input.attrs and input.attrs['name'] in saml_fields:
            form_data[input.attrs['name']] = input.attrs['value']

    return form_data

def parse_user_points(html):
    soup = BeautifulSoup(html, 'lxml')
    for content in soup.find_all('a', title='Zur Rangliste'):
        if "Stud.IP-Punkte:" in content.text:
            scoreString = content.text.split()[1].replace('.', '')
            return int(scoreString)
    for content in soup.find_all('a', title='To the high score list'):
        if "Stud.IP-Score:" in content.text:
            scoreString = content.text.split()[1].replace('.', '')
            return int(scoreString)

    raise ParserError("Could not find user points", soup)

