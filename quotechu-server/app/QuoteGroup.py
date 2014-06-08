__author__ = 'paul'

from google.appengine.ext import ndb

class QuoteGroup(ndb.Model):
    quote_count = ndb.IntegerProperty()
    creation_timestamp = ndb.DateTimeProperty(auto_now_add=True)
    last_modified_timestamp = ndb.DateTimeProperty(auto_now=True)