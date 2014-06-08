__author__ = 'paul'

import QuotePersistenceManager
import RpcHandler


class AddQuoteHandler(RpcHandler.RpcHandler):
    def __init__(self):
        self._qpm = QuotePersistenceManager.QuotePersistenceManager()

    def handle(self, params):
        self._qpm.create_quote(
            params["group"],
            params["quote"],
            params["author"],
            params["contributor"],
            )