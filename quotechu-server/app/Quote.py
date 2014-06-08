__author__ = 'paul'

from google.appengine.ext import ndb

class Quote(ndb.Model):
    quote_string = ndb.StringProperty()
    author = ndb.StringProperty()
    contributor = ndb.StringProperty()
    creation_timestamp = ndb.DateTimeProperty(auto_now_add=True)