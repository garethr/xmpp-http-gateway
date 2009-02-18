#!/usr/bin/python

"""
XMPP-HTTP-Gateway
=================

A simple bot which exposes HTTP verbs over XMPP. Currently only 
really useful for HTTP debugging as it returns the unmassaged contents of the
response and doesn't allow you to send data.

"""

from jabberbot import JabberBot
from rest_client import RestClient

# remember to setup your settings file
try:
    from settings import USERNAME, PASSWORD
except ImportError, error:
    print "You have to create a local settings file (Error: %s)" % error
    sys.exit(1)

class GatewayJabberBot(JabberBot):
    """
    A bot that provides the ability to make various types of HTTP 
    request via XMPP.
    """
    client = RestClient()
            
    def bot_get(self, mess, args):
        "Make a HTTP GET request of the passed URL"
        return self.client.get(args).content
        
    def bot_post(self, mess, args):
        "Make a HTTP POST request of the passed URL"
        return self.client.post(args).content

    def bot_put(self, mess, args):
        "Make a HTTP PUT request of the passed URL"
        return self.client.put(args).content

    def bot_delete(self, mess, args):
        "Make a HTTP DELETE request of the passed URL"
        return self.client.delete(args).content

    def bot_head(self, mess, args):
        "Make a HTTP HEAD request of the passed URL"
        return self.client.head(args).content

    def bot_options(self, mess, args):
        "Make a HTTP OPTIONS request of the passed URL"
        return self.client.options(args).content

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