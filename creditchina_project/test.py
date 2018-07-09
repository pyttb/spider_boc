import pandas as pd
from datetime import datetime
def datelist(beginDate, endDate):
    date_l=[datetime.strftime(x,'%Y-%#m-%#d') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_l
print datelist('20160601','20160605')
