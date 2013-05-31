from .exception import AkamaiServiceException
from cStringIO import StringIO
from csv import reader as csv_reader


class BaseService(object):
    client = None

    def __init__(self, client, load_cp_codes=False):
        self.client = client
        self.codes = None

        if load_cp_codes:
            self.get_cp_codes()

    def __getattr__(self, name):
        try:
            return getattr(self.client.service, name)
        except KeyError:
            message = ('%s does not exist in service %s' %
                       (name, self.__name__))
            raise AkamaiServiceException(message)

    def get_cp_codes(self):
        """
        Retrieves a list of CPCodeInfo instances from akamai current service.
        CPCodeInfo format: {cpcode = 123, description = "desc", service = "Service::Method"}
        The numeric cp codes are stored in this service instance
        @return: list
        """
        data = self.invoke_method('getCPCodes')
        self.codes = [x.cpcode for x in data]

        return data

    def invoke_method(self, name, *args):
        data = getattr(self, name)(*args)

        return self.parse(data) if isinstance(data, basestring) else data

    def parse(self, data):
        """
        Parses csv data into a list of dictionaries where every csv row
        represents an item on the list.
        @param data:
        @return: list
        """
        mem_file = StringIO(data)
        reader = csv_reader(mem_file, lineterminator='\n', strict=True)

        result = []
        keys = None

        for row in reader:
            if not keys and row[0].startswith('#') and len(row) > 1:
                keys = row
                continue
            elif row[0].startswith('#') and len(row) <= 1:
                continue

            if keys:
                item = {}
                for count, k in enumerate(keys):
                    item[k] = row[count]
            else:
                item = row

            result.append(item)

        return result

