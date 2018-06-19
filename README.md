
<figure class="align-left">
  <img src="https://s3.amazonaws.com/images.seroundtable.com/charts2-Google-1900px--1444997211.jpg" alt="">
  <figcaption>Google Finance Logo</figcaption>
</figure>


Google Finance GET

### Getting the Financial data From Google Finance

.. image:: https://img.shields.io/pypi/v/requests.svg
    :target: https://pypi.org/project/requests/

.. image:: https://img.shields.io/pypi/l/requests.svg
    :target: https://pypi.org/project/requests/

.. image:: https://img.shields.io/pypi/pyversions/requests.svg
    :target: https://pypi.org/project/requests/





## Installation

Based on : https://github.com/pdevty/googlefinance-client-python

```
$ pip install googlefinance.get
$ pip install -i https://pypi.python.org/pypi googlefinance.get
```



## Getting Codes

>  Default Setting is KRX Market's Info (South Korea Market)

```python
from googlefinance.get import get_code
get_code()       
```

> [NASDAQ site's CSV to DataFrame](https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download)

```python
get_code('NASDAQ')
get_code('NYSE')
```



## Getting Historical Financial Data 

Getting the Only Single Company's Historical Financial Data

1. code = 'NASDAQ: code list'

2. period = '30d': 30 days (default) <br>
            '1M' : Month <br>
            '1Y' : year

3. interval = 86400 : 1 day (default)<br>
              60 * integer  (seconds)

```python
from googlefinance.get import get_datum

df = get_datum('KRX:005930', period='2M'， interval =86400)

date        Open     High     Low      Close    Volume
2018-05-04  53000.0  53900.0  51800.0  51900.0  39290305
2018-05-08  52600.0  53200.0  51900.0  52600.0  22907823
2018-05-09  52600.0  52800.0  50900.0  50900.0  15914664

```


## Getting Historical Financial Data 

```python
from googlefinance.get import get_data

df = get_data(['KRX:005930',
               'KOSDAQ:091990',
               'NASDAQ:TSLA',
               'NASDAQ:AMZN'], period='2M'， interval =86400)

date       Code        Open     High     Low      Close    Volume
2018-05-04  KRX:005930  53000.0  53900.0  51800.0  51900.0  39290305
2018-05-08  KRX:005930  52600.0  53200.0  51900.0  52600.0  22907823
2018-05-09  KRX:005930  52600.0  52800.0  50900.0  50900.0  15914664
```

© 2018 GitHub : https://github.com/YongBeomKim