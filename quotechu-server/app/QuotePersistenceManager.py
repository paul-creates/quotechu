__author__ = 'paul'

import logging
import random

import Quote
import QuoteGroup

from google.appengine.ext import ndb

class QuotePersistenceManager(object):
    @ndb.transactional
    def create_quote(self, group, quote, author, contributor):
        quote_group_key = ndb.Key(QuoteGroup.QuoteGroup, group)
        quote_group = quote_group_key.get()
        if not quote_group:
            quote_group = QuoteGroup.QuoteGroup(
                key=quote_group_key,
                quote_count=0)

        quote_key = ndb.Key(Quote.Quote, str(quote_group.quote_count),
                            parent=quote_group_key)
        quote = Quote.Quote(
            key=quote_key,
            quote_string=quote,
            author=author,
            contributor=contributor,
        )

        # Increment the quote count by 1 for the new quote
        quote_group.quote_count += 1

        ndb.put_multi([quote_group, quote])

    def get_quote(self, group, id):
        key = ndb.Key(QuoteGroup.QuoteGroup, group,
                Quote.Quote, str(id))

        return key.get()

    def get_quote_count(self, group):
        key = ndb.Key(QuoteGroup.QuoteGroup, group)
        quote_group = key.get()

        if quote_group is None:
            logging.error("get_quote_count called for unknown group %s", group)
            return 0

        return quote_group.quote_count

    @ndb.transactional
    def get_random_quote(self, group):
        count = self.get_quote_count(group)

        if not count:
            logging.error("Tried to get random quote for %s group, but "
                            "count was 0.", group)
            return None

        quote_id = random.randrange(0, count)
        quote_key = ndb.Key(QuoteGroup.QuoteGroup, group,
                            Quote.Quote, str(quote_id))
        return quote_key.get()