__author__ = 'paul'

import os
import random
import sys
import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

import helpers
import QuotePersistenceManager
import Quote

class MyTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_quote_count_non_existant(self):
        qpm = QuotePersistenceManager.QuotePersistenceManager()
        self.assertEqual(0, qpm.get_quote_count(helpers.some_string()))

    def test_create_quote(self):
        qpm = QuotePersistenceManager.QuotePersistenceManager()
        group = helpers.some_string()
        quote_string = helpers.some_string()
        author = helpers.some_string()
        contributor = helpers.some_string()
        qpm.create_quote(group, quote_string, author, contributor)

        # Now fetch the quote group from the datastore.
        quote_group_key = ndb.Key("QuoteGroup", group)
        quote_group = quote_group_key.get()
        self.assertIsNotNone(quote_group)
        self.assertEqual(1, quote_group.quote_count)

        # And also fetch and check the quote itself.
        quote_key = ndb.Key(Quote.Quote, "0",
                            parent=quote_group_key)
        quote = quote_key.get()
        self.assertIsNotNone(quote)
        self.assertEqual(quote_string, quote.quote_string)
        self.assertEqual(author, quote.author)
        self.assertEqual(contributor, quote.contributor)

    def test_get_quote(self):
        qpm = QuotePersistenceManager.QuotePersistenceManager()
        group = helpers.some_string()
        quote_string = helpers.some_string()
        author = helpers.some_string()
        contributor = helpers.some_string()
        quote_id = random.randint(0, 10)

        # Create a quote and put it in the datastore
        quote_key = ndb.Key("QuoteGroup", group,
                            Quote.Quote, str(quote_id))
        quote = Quote.Quote(
            key=quote_key,
            quote_string=quote_string,
            author=author,
            contributor=contributor,
        )
        quote.put()

        # Now fetch the quote group from the datastore.
        actual_quote = qpm.get_quote(group, quote_id)
        self.assertIsNotNone(actual_quote)
        self.assertEqual(quote.quote_string, actual_quote.quote_string)
        self.assertEqual(quote.author, actual_quote.author)
        self.assertEqual(quote.contributor, actual_quote.contributor)

    def test_get_random_quote(self):
        qpm = QuotePersistenceManager.QuotePersistenceManager()
        group = helpers.some_string()
        quote_string = helpers.some_string()
        author = helpers.some_string()
        contributor = helpers.some_string()
        qpm.create_quote(group, quote_string, author, contributor)

        # Now fetch a random quote, it should be the one added above.
        actual_quote = qpm.get_random_quote(group)
        self.assertIsNotNone(actual_quote)
        self.assertEqual(quote_string, actual_quote.quote_string)
        self.assertEqual(author, actual_quote.author)
        self.assertEqual(contributor, actual_quote.contributor)

if __name__ == '__main__':
    unittest.main()
