# -*- coding: utf-8 -*-
import logging
import urlparse

import webapp2
from google.appengine.ext import ereporter

import constants
from models import Redirect
from util import get_environment


class MainPage(webapp2.RequestHandler):
    def get(self, *args, **kwargs):

        if constants.WARM_UP_PATH in self.request.url:
            return self.response.out.write('Warming Up...')

        # TODO: Re construct the original URL
        _, netloc, _, _, _ = urlparse.urlsplit(self.request.url)
        # Discard any port number from the hostname
        netloc = netloc.split(':', 1)[0]

        redirect = Redirect.get_by_source(netloc)
        if not redirect:
            logging.error('Unable to redirect this url [%s]', self.request.url)
            self.abort(404)
        logging.info('Redirect successful from [%s] to [%s] permanent? [%s]',
                     self.request.url, redirect.destination, redirect.permanent)
        # TODO: Store permanent in Redirect model
        return self.redirect(str(redirect.destination), redirect.permanent)


app = webapp2.WSGIApplication([
    webapp2.Route(r'/<:.*>', handler=MainPage),
], debug=get_environment() != constants.ENV_PRODUCTION)

ereporter.register_logger()
