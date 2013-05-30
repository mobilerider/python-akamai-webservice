import sys
import getopt
from datetime import datetime

from AkamaiProvider import AkamaiProvider

def print_help():
    print("Usage : <report> [-c <codes> | --codes=<codes> ]")
    print("Gets report data from Akamai web services.")
    print("Report types: live | vod | storage | total_storage, ")
    print("   -c, --codes         list of CP codes separated by comma")
    print("   -u, --username      Akamai Luna Control Centerusername")
    print("   -p, --password      Akamai Luna Control Center password")
    print("   -s, --start         start date for report filtering, by default -1 day, format: mm/dd/yyyy-hh:mm")
    print("   -e, --end           end date for report filtering, by default now, format: mm/dd/yyyy-hh:mm")
    print("   -h, --help          display this help and exit")
    print("   -v                  verbose mode, output debug information")
    print("       --version       output version information and exit")

if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            raise Exception('Missing required parameters')

        opts, args = getopt.getopt(sys.argv[1:], "hc:u:p:s:e:", ["help,codes=,username=, password=, start=,end="])

        report = args[0]
        report_args = []
        report_kwargs = {}

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print_help()
                sys.exit()
            elif opt in ('-c', '--codes'):
                report_args.append(arg.split(','))
            elif opt in ('-u', '--username'):
                report_kwargs['username'] = arg
            elif opt in ('-p', '--password'):
                report_kwargs['password'] = arg
            elif opt in ('-s', '--start'):
                report_kwargs['start_date'] = datetime.strptime(arg, '%m/%d/%Y-%H:%M:%S')
            elif opt in ('-e', '--end'):
                report_kwargs['end_date'] = datetime.strptime(arg, '%m/%d/%Y-%H:%M:%S')
            else:
                raise Exception('Argument unknown')

        provider = AkamaiProvider(*report_args, **report_kwargs)

        print provider.get_report(report)

    except Exception as ex:
        print("Error: " + ex.msg if hasattr(ex, 'msg') else ex.message)
        print_help()

