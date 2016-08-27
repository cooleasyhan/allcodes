import tushare as ts
from dateutil.rrule import *
from dateutil.parser import *
import sys
import time
def tushare_to_csv(code, method, bdate, edate):
    dates = list(
        rrule(DAILY,
                 dtstart=parse(bdate),
                 until=parse(edate))
        )
    _method = getattr(ts,method)
    for date in dates:
        datestr = date.strftime('%Y-%m-%d')
        file_name='_'.join((datestr, code, method))
        df = _method(code, datestr)
        df.to_csv(file_name+'.csv', encoding='utf-8')
        time.sleep(1)

def main():
    code = sys.argv[1]
    method = sys.argv[2]
    bdate = sys.argv[3]
    edate = sys.argv[4]

    tushare_to_csv(code, method, bdate, edate)


if __name__ == '__main__':
    main()

