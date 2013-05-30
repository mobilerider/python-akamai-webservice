from suds.client import Client

from .exception import AkamaiServiceException


class BaseService(object):
    client = None

    def __init__(self, client):
        self.client = client

    def __getattr__(self, name):
        try:
            return getattr(self.client.service, name)
        except KeyError:
            message = ('%s does not exist in service %s' %
                (name, self.__name__))
            raise AkamaiServiceException(message)
