# -*- coding: utf-8 -*-

from google.appengine.api import memcache
from google.appengine.ext import ndb
from protorpc import messages

from endpoints_proto_datastore.ndb.model import EndpointsModel, \
    EndpointsAliasProperty


class Redirect(EndpointsModel):
    _message_fields_schema = ('source', 'destination',)

    destination = ndb.StringProperty(required=True, indexed=False)
    permanent = ndb.BooleanProperty(default=True, indexed=False)

    def source_setter(self, value):
        key = ndb.Key(Redirect, value)
        self.UpdateFromKey(key)

    @EndpointsAliasProperty(setter=source_setter,
                            property_type=messages.StringField)
    def source(self):
        return self.key.id()

    @classmethod
    def get_by_source(cls, source):
        result = memcache.get('redirect_%s' % source)
        if result is None:
            result = cls.get_by_id(source)
            if result:
                memcache.add('redirect_%s' % source, result)
        return result
