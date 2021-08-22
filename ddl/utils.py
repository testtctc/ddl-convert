# encoding=utf-8
import  pandas  as pd
import datetime

def generate_date_range(statdate,enddate):
    """generate doris date range"""
    dates = pd.date_range(statdate,enddate)
    templates='partition p{partition} Values[("{start}"),("{end}"))'
    out=[]
    for d in dates:
        start=d
        end =d + datetime.timedelta(1)
        t= templates.format(partition=start.strftime('%Y%m%d'),start=start.strftime('%Y-%m-%d'),end=end.strftime('%Y-%m-%d'))
        out.append(t)
    return ',\n'.join(out)

