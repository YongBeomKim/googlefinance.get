
# googlefinance.get

### What is different??
1. based on : **https://github.com/pdevty/googlefinance-client-python** [link](https://github.com/pdevty/googlefinance-client-python)
1. Merged on sigle function 
1. and Covert input query to simple (same as Google finance site's format)

### Default setting is...
1. period   : 30 day ( 1d ~ 10Y )
1. invertal : 86400 sec by daily closed time (300 ~ 86400)

`get_finance("KRX:005930")` and  `get_finance(["INDEXDJX:.DJI","INDEXNYSEGIS:NYA","KRX:005930","KOSDAQ:053800"])` is worked..



## 1. single code's DataFrame (SamSung Electronic)

```python
$ pip install -i https://pypi.python.org/pypi googlefinance.get

from googlefinance.get import get_data
df = get_data("KRX:005930",
              period='30d')    # total period

print(df)
#                          Code       Open       High        Low      Close  \
#2018-02-12   KRX:005930  2255000.0  2258000.0  2252000.0  2254000.0
#2018-02-13   KRX:005930  2254000.0  2260000.0  2253000.0  2259000.0
#2018-02-14   KRX:005930  2259000.0  2271000.0  2259000.0  2263000.0

#                      Volume
#2018-02-12    35993
#2018-02-13    11044
#2018-02-14     9902
```

## If you set the interval in single code (ex) SamSung Electronic)

```python
$ pip install googlefinance.get

from googlefinance.get import get_data
df = get_data("KRX:005930",
              period='30d',    # total period
              interval='300')  # data interval (step by : 60 sec * n)
print(df)
#                          Code       Open       High        Low      Close  \
#2018-02-12 09:05:00  KRX:005930  2255000.0  2258000.0  2252000.0  2254000.0
#2018-02-12 09:10:00  KRX:005930  2254000.0  2260000.0  2253000.0  2259000.0
#2018-02-12 09:15:00  KRX:005930  2259000.0  2271000.0  2259000.0  2263000.0

#                      Volume
#2018-02-12 09:05:00   35993
#2018-02-12 09:10:00   11044
#2018-02-12 09:15:00    9902
```


## If you set the Codes to DataFrame ([code1, code2, code3, ...])
```python
df = get_data(["INDEXDJX:.DJI",
               "INDEXNYSEGIS:NYA",
               "KRX:005930",
               "KOSDAQ:053800"], 
               interval='300',
               period='1Y')
print(df)

#                              Code      Open      High       Low     Close  \
#2016-03-29 09:05:00  INDEXDJX:.DJI  17526.08  17583.81  17493.03  17535.39
#2016-03-30 09:10:00  INDEXDJX:.DJI  17512.58  17642.81  17434.27  17633.11
#2016-03-31 09:15:00  INDEXDJX:.DJI  17652.36  17790.11  17652.36  17716.66

#                        Volume
#2016-03-29 09:05:00   70452434
#2016-03-30 09:10:00   86159775
#2016-03-31 09:15:00   79326225
```


© 2018 GitHub : https://github.com/YongBeomKim