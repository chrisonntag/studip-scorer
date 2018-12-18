import getpass
import asyncio
import logging
import os
import ssl
import time
from typing import List
from urllib.parse import urlencode
from weakref import WeakSet
from datetime import datetime

import aiohttp
from aiohttp import ClientError

from parsers import *


BASE_URL = 'https://studip.uni-passau.de/studip/api.php'


class StudIPError(Exception):
    pass


class LoginError(StudIPError):
    pass


class StudIPScoreSession:
    def __init__(self, user, password, loop):
        self.user = user
        self.password = password
        self._studip_base = 'https://studip.uni-passau.de'
        self._sso_base = 'https://sso.uni-passau.de'

        self._background_tasks = WeakSet()  # TODO better management of (failing of) background tasks
        if not loop:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop

        context = ssl._create_unverified_context()

        connector = aiohttp.TCPConnector(loop=self._loop, limit=10,
                                         keepalive_timeout=30,
                                         force_close=False,
                                         ssl=context)
        self.ahttp = aiohttp.ClientSession(connector=connector, loop=self._loop,
                                           read_timeout=30,
                                           conn_timeout=30)

    def _sso_url(self, url):
        return self._sso_base + url


    def _studip_url(self, url):
        return self._studip_base + url


    async def close(self):
        try:
            for task in self._background_tasks:
                task.cancel()
        finally:
            if self.ahttp:
                await self.ahttp.close()

    async def do_login(self):
        try:
            async with self.ahttp.get(self._studip_url("/studip/index.php?again=yes&sso=shib")) as r:
                post_url = parse_login_form(await r.text())
        except (ClientError, ParserError) as e:
            raise LoginError("Could not initialize Shibboleth SSO login") from e

        try:
            async with self.ahttp.post(
                    self._sso_url(post_url),
                    data={
                        "j_username": self.user,
                        "j_password": self.password,
                        "uApprove.consent-revocation": "",
                        "_eventId_proceed": ""
                    }) as r:
                form_data = parse_saml_form(await r.text())
        except (ClientError, ParserError) as e:
            raise LoginError("Shibboleth SSO login failed") from e

        try:
            async with self.ahttp.post(self._studip_url("/Shibboleth.sso/SAML2/POST"), data=form_data) as r:
                await r.text()
                if not r.url.path.startswith("/studip"):
                    raise LoginError("Invalid redirect after Shibboleth SSO login to %s" % r.url)
        except ClientError as e:
            raise LoginError("Could not complete Shibboleth SSO login") from e


    async def get_user_id(self):
        async with self.ahttp.get(self._studip_url("/studip/api.php/user")) as r:
            response = await r.json()
            return response['user_id']


    async def create_news(self):
        form_data = {
                "topic": "Ankündigung %s" % datetime.today(),
                "body": "Das ist eine automatisch generierte Ankündigung.",
                "expire": 86400, # 24hrs
                "allow_comments": 1
                }
        async with self.ahttp.post(self._studip_url("/studip/api.php/course/5d59c8f587ed7cfc1e01b35dab582e6e/news"), data=form_data) as r:
            await r.text()
            if r.status == 200:
                response_data = await r.text()
                print('Success')
                print(str(response_data))
                return True
            else:
                response_data = await r.text()
                print('Failure with HTTP Status Code %d' % r.status)
                print(r.request_info)
                print(str(response_data))
                return False


def main():
    with open('credentials.cfg', 'r') as file:
        username, password = file.readline().split('\n')

        event_loop = asyncio.get_event_loop()
        session = StudIPScoreSession(username, password, event_loop)

        try:
            coro = session.do_login()
            event_loop.run_until_complete(coro)
            event_loop.run_until_complete(session.create_news())
        finally:
            async def shutdown_session_async(session):
                await session.close()

            event_loop.run_until_complete(shutdown_session_async(session))


