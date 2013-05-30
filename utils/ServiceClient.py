from suds.client import Client


class ServiceClient(object):
    TIME_ZONE = 'GMT'

    def __init__(self, *args, **kwargs):
        self.wsdl_url = args[0] if len(args) else kwargs.get('url') + '?wsdl'

        #Authentication is provided by the (default) HttpAuthenticated Transport
        #class defined in the transport.https module
        self.client = Client(self.wsdl_url, username=kwargs.get('username'), password=kwargs.get('password'))
        self.service = self.client.service