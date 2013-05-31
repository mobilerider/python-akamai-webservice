from .exception import AkamaiServiceException
from cStringIO import StringIO
from csv import reader as csv_reader

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

    def invoke_method(self, name, *args):
        return self.parse(getattr(self, name)(*args))

    def parse(self, data):
        """
        Parses csv data into a list of dictionaries where every csv row
        represents an item on the list.
        @param data:
        @return:
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

