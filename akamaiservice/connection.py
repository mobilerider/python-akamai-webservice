from suds.client import Client

from .constants import WSDL_BASE_URL
from .baseservice import BaseService


class Connection(object):
    username = None
    password = None

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __get_client(self, service_name):
        wsdl_url = '%s%s?wsdl' % (WSDL_BASE_URL, service_name)
        return Client(wsdl_url, username=self.username, password=self.password)

    def get_service(self, service_name, load_cp_codes=False):
        client = self.__get_client(service_name)
        return type(service_name, (BaseService,), dict())(client=client, load_cp_codes=load_cp_codes)
