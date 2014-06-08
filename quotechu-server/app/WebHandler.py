__author__ = 'paul'

import QuotePersistenceManager

class WebHandler(object):
    def handle(self, quote_group, unused_params):
        qpm = QuotePersistenceManager.QuotePersistenceManager()
        return qpm.get_random_quote(quote_group).quote_string