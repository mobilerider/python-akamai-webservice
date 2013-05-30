from utils import ServiceClient


class StreamingReportService(ServiceClient):
    SERVICE_NAME = 'StreamingReportService'

    def __init__(self, url_prefix, cp_codes=None, *args, **kwargs):
        self.service_url = url_prefix + self.SERVICE_NAME
        self.cp_codes = cp_codes if cp_codes else []

        super(ServiceClient, self).__init__(self.service_url, *args, **kwargs)

    def get_cp_codes(self):
        return self.service.getCPCodes()

    def get_live_stream_traffic_for_cp_code(self, start_date, end_date):
        """
        Retrieves an traffic report for a live stream cp code
        @param start_date: Start date for report filtering
        @param end_date: End date for report filtering
        @return:
        """
        return self.service.getLiveStreamTrafficForCPCodeV2(self.cp_codes, start_date, end_date, self.TIME_ZONE, None)

    def get_vod_stream_traffic_for_cp_code(self, start_date, end_date):
        """
        Retrieves an traffic report for vod stream cp code
        @param start_date: Start date for report filtering
        @param end_date: End date for report filtering
        @return: string
        """
        return self.service.getLiveStreamTrafficForCPCodeV2(self.cp_codes, start_date, end_date, self.TIME_ZONE, None)