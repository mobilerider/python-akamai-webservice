from cStringIO import StringIO
from csv import reader as csv_reader

from suds import WebFault

from .exception import AkamaiServiceException


class BaseService(object):
    client = None

    def __init__(self, client, load_cp_codes=False):
        self.client = client
        self.codes = None
        self.invalid_codes = None

        if load_cp_codes:
            self.get_cp_codes()

    def __getattr__(self, name):
        try:
            return getattr(self.client.service, name)
        except KeyError:
            message = ('%s does not exist in service %s' % (name, self.__name__))
            raise AkamaiServiceException(message)

    def get_cp_codes(self, force_refresh=False):
        """
        Retrieves a list of CPCodeInfo instances from akamai current service.
        CPCodeInfo format: {cpcode = 123 description = "desc" service = "Service::Method"}
        The numeric cp codes are stored in this service instance
        @param force_refresh: bool Forces retrieving of codes from remote service
        @return: list
        """
        if self.codes and not force_refresh:
            if self.invalid_codes:
                return [x for x in self.codes if x not in self.invalid_codes]
            else:
                return self.codes

        data = self.invoke_method('getCPCodes')
        self.codes = [x.cpcode for x in data]
        self.invalid_codes = []

        return data

    def invoke_method(self, name, *args, **kwargs):
        """
        Executes akamai service method given by name and returns a result.
        It parses result data if is of string type
        Use all_cp_codes=True to test for all codes allowed, if you use
        this option you may pass the cp codes param as empty list or None
        Use strict to force exception raising
        @param name: string
        @param args: list
        @param kwargs: dict
        @return: mixed
        """
        strict = kwargs.get('strict')
        all_cp_codes = kwargs.get('all_cp_codes')

        if all_cp_codes:
            args = list(args)
            args[0] = self.get_cp_codes()

        try:
            data = getattr(self, name)(*args)
        except WebFault as ex:
            if not strict:
                if 'The following cpcodes are invalid for you' in ex.message:
                    self.invalid_codes = [int(x.strip()) for x in ex.message[:-2].split(':')[-1].split(',')]
                else:
                    raise ex

                # Protects against infinite loop
                kwargs['strict'] = False
                # Call itself again
                return self.invoke_method(name, *args, **kwargs)
            else:
                raise ex

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
                keys[0] = keys[0].replace('#', '').strip()
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

