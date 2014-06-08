import helpers
import os
import sys
import unittest
import webtest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

import quotechu

from google.appengine.ext import testbed

class AppTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        app = quotechu.application
        # Wrap the app with WebTest's TestApp.
        self.testapp = webtest.TestApp(app)


    def tearDown(self):
        self.testbed.deactivate()

    def testBasicAddGetQuote(self):
        # Add a quote
        quote = helpers.some_string()
        group = helpers.some_string()
        author = helpers.some_string()
        contributor = helpers.some_string()
        params = [('quote', quote),
                  ('group', group),
                  ('author', author),
                  ('contributor', contributor),
                  ]
        add_response = self.testapp.post('/rpc/addquote', params)
        self.assertEqual(200, add_response.status_int)

        # Get the quote
        get_response = self.testapp.get('/%s/getquote' % (group))
        self.assertEqual(200, get_response.status_int, 200)
        self.assertEqual(quote, get_response.normal_body)
        self.assertEqual('text/plain', get_response.content_type)