__author__ = "Paul Marshall"

import webapp2

import RpcDispatcher
import WebHandler

class RpcServlet(webapp2.RequestHandler):
    def post(self, command=None):
        params = self.request.params
        RpcDispatcher.RpcDispatcher.handle(command, params)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.status = 200


class WebServlet(webapp2.RequestHandler):
    def get(self, quote_group=None, command=None):
        self.response.headers['Content-Type'] = 'text/plain'
        page = WebHandler.WebHandler().handle(quote_group, command)
        self.response.write(page)

application = webapp2.WSGIApplication([
    webapp2.Route('/rpc/<command>', RpcServlet),
    webapp2.Route('/<quote_group>/<command>', WebServlet),
    ])