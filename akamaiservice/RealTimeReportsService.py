from utils import ServiceClient


class RealTimeReportsService(ServiceClient):
    SERVICE_NAME = 'RealtimeReports'

    def __init__(self, *args, **kwargs):
        self.service_url = args[0] if len(args) else kwargs.get('url_prefix') + self.SERVICE_NAME
        self.cp_codes = args[1] if len(args) > 1 else kwargs.get('cp_codes', [])

        args = [self.service_url] + args.shift()

        super(ServiceClient, self).__init__(*args, **kwargs)

    def get_cp_codes(self):
        return self.service.getCPCodes()

    def get_content_storage_summary(self):
        return self.service.getContentStorageSummary(self.cp_codes)

    def get_content_storage_summary_by_cp_code(self):
        return self.service.getContentStorageSummaryByCPCode(self.cp_codes)