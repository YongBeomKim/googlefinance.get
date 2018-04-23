
# pip install googlefinance.get

based on : https://github.com/pdevty/googlefinance-client-python

```
$ pip install googlefinance.get
$ (or) pip install -i https://pypi.python.org/pypi googlefinance.get
```


## <Parmetor's>

**_NASDAQ : Code Name_** [download](http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download)

1. code = 'NASDAQ: code list'

2. period = '30d': 30 days (default) <br>
            '1M' : Month <br>
            '1Y' : year

3. interval = 86400 : 1 day (default)<br>
              60 * integer  (seconds)


## How to Use it

1. Import googlefinance.get <br>
input the Codes by [list] 

```python
from googlefinance.get import get_data

df = get_data(['KRX:005930',
               'KOSDAQ:091990',
               'NASDAQ:TSLA',
               'NASDAQ:AMZN'], period='2M')
print(df.shape)
df

# (154, 6)
#     Code    Open    High    Low     Close   Volume
# Date
# 2018-02-05  KRX:005930  2325000.0   2416000.0   2300000.0   2396000.0   516513
# 2018-02-06  KRX:005930  2330000.0   2396000.0   2329000.0   2371000.0   364291
```

```python
# 2. filtering by Code
df[df.Code == 'NASDAQ:TSLA']

#     Code    Open    High    Low     Close   Volume
# Date
# 2017-04-04  NASDAQ:AMZN     888.00  893.4900    885.4200    891.51  3422328
# 2017-04-05  NASDAQ:AMZN     891.50  908.5384    890.2800    906.83  4984656
# 2017-04-06  NASDAQ:AMZN     910.82  923.7200    905.6200    909.28  7508370
```


```python
# 3. googlefinance.get
# input the Single Code

df = get_data('NASDAQ:AMZN',
               period='1Y')
df
#     Code    Open    High    Low     Close   Volume
# Date
# 2017-04-04  NASDAQ:AMZN     888.00  893.4900    885.4200    891.51  3422328
# 2017-04-05  NASDAQ:AMZN     891.50  908.5384    890.2800    906.83  4984656
# 2017-04-06  NASDAQ:AMZN     910.82  923.7200    905.6200    909.28  7508370
# 2017-04-07  NASDAQ:AMZN     913.80  917.1899    894.4927    898.28  6344065
# 2017-04-08  NASDAQ:AMZN     899.65  900.0900    889.3100    894.88  3710922
```

```pyhton
# 4. Yahoo Finance API
# Using Yahoo finance history data API

from googlefinance.get import get_data_yahoo
get_data_yahoo('005930.KS'
                start_date = '2010-01-01', # (default) : 2010-01-01
                end_date   = '2018-04-01') # (default) : Today Date 

[*********************100%***********************]  1 of 1 downloaded

    Open    High    Low     Close   Adj Close   Volume
Date                        
2010-01-04  803000.0    809000.0    800000.0    809000.0    7.338929e+05    239016
2010-01-05  826000.0    829000.0    815000.0    822000.0    7.456860e+05    558517
2010-01-06  829000.0    841000.0    826000.0    841000.0    7.629221e+05    458977
```

© 2018 GitHub : https://github.com/YongBeomKim