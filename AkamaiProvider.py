import sys
from datetime import datetime, timedelta
from akamaiservice import *
from utils.StringUtils import lower_case_underscore_to_camel_case


class AkamaiProvider(object):
    __slots__ = ['services', 'cp_codes', 'start_date', 'end_date', 'username', 'password', #Internal vars
                 'real_time_reports_service', 'streaming_report_service'] #Reports

    URL_PREFIX = 'https://control.akamai.com/nmrws/services/'

    def __init__(self, *args, **kwargs):
        now = datetime.now()

        self.services = {}
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.cp_codes = args[0] if len(args) else []
        self.end_date = kwargs.get('end_date', now)
        self.start_date = kwargs.get('start_date', self.end_date - timedelta(1))


    def __getattr__(self, item):
        if not self.services.has_key(item):
            camelized_item = lower_case_underscore_to_camel_case(item)
            service_class = getattr(sys.modules['akamaiservice'], camelized_item)
            self.services[item] = service_class(self.URL_PREFIX, self.cp_codes, username=self.USERNAME,
                                                 password=self.PASSWORD)

        return self.services[item]

    def get_codes(self):
        return self.service.getCPCodes()

    def get_total_storage(self):
        return self.real_time_reports_service.get_content_storage_summary()

    def get_storage_by_codes(self):
        return self.real_time_reports_service.get_content_storage_summary_by_cp_code()

    def get_live_traffic(self):
        return self.streaming_report_service.get_live_stream_traffic_for_cp_code(self.start_date, self.end_date)

    def get_vod_traffic(self):
        return self.streaming_report_service.get_vod_stream_traffic_for_cp_code(self.start_date, self.end_date)

    def get_report(self, report):
        return {
            'live': self.get_live_traffic,
            'vod': self.get_vod_traffic,
            'storage': self.get_storage_by_codes,
            'total_storage': self.get_total_storage
        }[report]()


