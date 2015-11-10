# -*- coding: utf-8 -*-
from getpass import getpass
import logging

from google.appengine.ext.remote_api import remote_api_stub

from models import Redirect


def add_redirect(source, destination, permanent=True):
    redirect_key = Redirect(
        id=source,
        destination=destination,
        permanent=permanent
    ).put()
    logging.info("Added redirect [%s]", redirect_key)


def auth_func():
    return raw_input('Username:'), getpass('Password:')

remote_api_stub.ConfigureRemoteApi(
    None, '/_ah/remote_api', auth_func,
    #'localhost:8080',
    'redirect-io.appspot.com'
)

add_redirect('redirect-io.appspot.com', 'https://github.com/dcifuen/redirect-io', True)
