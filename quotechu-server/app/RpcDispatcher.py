__author__ = 'paul'

import logging

import AddQuoteHandler

class RpcDispatcher(object):

    @classmethod
    def handle(cls, command, params):
        logging.info("Handling RPC: %s with params: %s", command, params)
        handler = cls._COMMAND_MAP[command]
        return handler.handle(params)

    _COMMAND_MAP = {
        "addquote": AddQuoteHandler.AddQuoteHandler(),
    }