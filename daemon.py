#!/usr/bin/python

"""
XMPP-HTTP-Gateway
=================

A simple bot which exposes HTTP verbs over XMPP. Currently only 
really useful for HTTP debugging as it returns the unmassaged contents of the
response and doesn't allow you to send data.

"""

__author__ = 'Gareth Rushgrove <gareth@morethanseven.net>'
__version__ = '0.1'

import httplib2

from jabberbot import JabberBot
from restful_lib import Connection

# remember to setup your settings file
try:
    from settings import USERNAME, PASSWORD
except ImportError, error:
    print "You have to create a local settings file (Error: %s)" % error
    sys.exit(1)

CONNECTION_ERROR = "Unable to connect to %s"

class GatewayJabberBot(JabberBot):
    """
    A bot that can make various types of HTTP request over XMPP.
    """
    
    def _connect(self, args):
        list_of_args = args.split(" ")
        conn = Connection(list_of_args[0])
        return conn, list_of_args
            
    def bot_get(self, mess, args):
        "Make a HTTP GET request of the passed URL"
        try:
            conn, list_of_args = self._connect(args)
            return conn.request_get("/")
        except httplib2.ServerNotFoundError:
            return CONNECTION_ERROR % list_of_args[0]
        
    def bot_post(self, mess, args):
        "Make a HTTP POST request of the passed URL"
        try:
            conn, list_of_args = self._connect(args)
            return conn.request_post("/")
        except httplib2.ServerNotFoundError:
            return CONNECTION_ERROR % list_of_args[0]        

    def bot_put(self, mess, args):
        "Make a HTTP PUT request of the passed URL"
        try:
            conn, list_of_args = self._connect(args)
            return conn.request_put("/")
        except httplib2.ServerNotFoundError:
            return CONNECTION_ERROR % list_of_args[0]        

    def bot_delete(self, mess, args):
        "Make a HTTP DELETE request of the passed URL"
        try:
            conn, list_of_args = self._connect(args)
            return conn.request_delete("/")
        except httplib2.ServerNotFoundError:
            return CONNECTION_ERROR % list_of_args[0]

    def bot_head(self, mess, args):
        "Make a HTTP HEAD request of the passed URL"
        try:
            conn, list_of_args = self._connect(args)
            return conn.request_head("/")
        except httplib2.ServerNotFoundError:
            return CONNECTION_ERROR % list_of_args[0]
    
    # I'll have a nice error handler one day
    def unknown_command(self, mess, cmd, args):
        "If you call a command we don't regonise we output a nice message"
        return None

    # not sure I need this, but I want to have a closer look into
    # what use I can put it
    def bot_subscribe(self, mess, args):
        "Send the subscribe command to have me authorize your subscription to my presence"
        f = mess.getFrom()
        self.conn.Roster.Authorize(f)
        return 'Authorized.'

def main():
    "Connect to the server and run the bot forever"
    jabber_bot = GatewayJabberBot(USERNAME, PASSWORD)
    jabber_bot.serve_forever()

if __name__ == '__main__':
    # if we run the script rather than import it then start the bot 
    main()