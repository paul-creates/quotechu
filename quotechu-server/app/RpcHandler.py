__author__ = 'paul'

import abc

class RpcHandler(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self, params):
        """Handle the RPC."""