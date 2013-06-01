import sys
import getopt
from datetime import datetime
from akamaiservice.connection import Connection


def print_help():
    print("Usage : <service> <method> [-c <codes> | --codes=<codes> ]")
    print("Gets report data from Akamai web services.")
    print("Report types: live | vod | storage | total_storage, ")
    print("   -c, --codes         list of CP codes separated by comma")
    print("   -u, --username      Akamai Luna Control Centerusername")
    print("   -p, --password      Akamai Luna Control Center password")
    print("   -s, --start         start date for report filtering, by default -1 day, format: mm/dd/yyyy-hh:mm")
    print("   -e, --end           end date for report filtering, by default now, format: mm/dd/yyyy-hh:mm")
    print("   -f, --format        media format for filtering, supported: all, flash, real, quickTime, windowsMedia")
    print("   -h, --help          display this help and exit")
    print("   -v                  verbose mode, output debug information")
    print("       --version       output version information and exit")


if __name__ == "__main__":
    try:
        if len(sys.argv) <= 3:
            raise Exception('Missing required parameters')

        opts, args = getopt.getopt(sys.argv[3:], "hc:u:p:s:e:f:m:",
                                   ["help,codes=,username=,password=,start=,end=,format=,media="])

        service_args = []
        service_kwargs = {'service_name': sys.argv[1], 'service_method': sys.argv[2]}

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print_help()
                sys.exit()
            elif opt in ('-c', '--codes'):
                service_args.append(arg.split(','))
            elif opt in ('-u', '--username'):
                service_kwargs['username'] = arg
            elif opt in ('-p', '--password'):
                service_kwargs['password'] = arg
            elif opt in ('-s', '--start'):
                service_args.append(datetime.strptime(arg, '%m/%d/%Y-%H:%M:%S'))
            elif opt in ('-e', '--end'):
                service_args.append(datetime.strptime(arg, '%m/%d/%Y-%H:%M:%S'))
                service_args.append('GMT')  #Default time zone
                service_args.append(None)  #Null for column array, not supported yet
            elif opt in ('-f', '--format'):
                f = service_kwargs.get('filter', {})
                f['format'] = arg
                service_kwargs['filter'] = f
                service_args.append(f)
            elif opt in ('-m', '--media'):
                service_args.append(arg.split(','))
            else:
                raise Exception('Argument unknown')

        connection = Connection(service_kwargs.get('username'), service_kwargs.get('password'))
        service = connection.get_service(service_kwargs['service_name'], True)

        print service.invoke_method(service_kwargs['service_method'], *service_args, all_cp_codes=True)

    except Exception as ex:
        print("Error: " + ex.msg if hasattr(ex, 'msg') else ex.message)
        print_help()

