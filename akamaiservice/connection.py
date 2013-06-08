from email import message_from_string
import re
from xml.sax import SAXParseException
from lxml.etree import XMLParser, fromstring as xml_from_string, tostring as xml_to_string

from suds.client import Client
from suds.sax.parser import Parser
from suds.bindings.binding import Binding

from .constants import WSDL_BASE_URL
from .baseservice import BaseService


BOUNDARY_REGEX = re.compile('^-+=(?P<boundary_name>[^-]+)-*$')


def replyfilter(self, reply_string):
    try:
        Parser().parse(string=reply_string)
        return reply_string
    except SAXParseException:
        parts = []
        part = []
        for l in reply_string.splitlines():
            if not BOUNDARY_REGEX.match(l):
                part.append(l)
            else:
                parts.append('\n'.join(part))
                part = []
        parts = [
            message_from_string(_p).get_payload()
            for _p in parts
            if ''.join(_p.splitlines()).strip()
        ]
        xml = xml_from_string(parts[0], parser=XMLParser(
            attribute_defaults=False,
            dtd_validation=False,
            load_dtd=False,
            no_network=False,
            ns_clean=False,
            remove_blank_text=False,
            remove_comments=False,
            remove_pis=False,
            strip_cdata=False,
            compact=False,
            resolve_entities=False,

        ))
        xml.find('.//getLiveStreamTrafficForCPCodeV2Return').text = parts[1]
        return xml_to_string(xml)

Binding.replyfilter = replyfilter


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
