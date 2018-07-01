# based on : https://github.com/pdevty/googlefinance-client-python
# get  url : https://finance.google.com/finance/getprices?q=LHA&p=10Y&f=d,c,h,l,o,v
# https://gist.github.com/lebedov/f09030b865c4cb142af1


# multiful envirment possible
def get_data(codes, period='30d', interval="86400", output = False):

    # output option check
    if output != False  and  output not in ['Open', 'High', 'Low', 'Close', 'Volume']:
        print('Option Error : output parametor is Not in [ Open, High, Low, Close, Volume]')
        return None

    # working 1 : if "codes" is 'single code'
    if type(codes) == str:
        # return code_to_dataframe(codes, period, interval)
        return get_datum(codes, period, interval)

    # checking the "codes" is not a [list] & single code
    if type(codes) != list:
        print("Input Error : 'code' is not a [list] or 'single code' ")
        return None

    # working 2 : if "codes" is a [list] type
    import pandas as pd
    prices_data     = pd.DataFrame()
    for code in codes:
        # df          = code_to_dataframe(code, period, interval)
        df          = get_datum(code, period, interval)
        df.insert(0,'Code',code)
        prices_data = pd.concat([prices_data, df[~df.index.duplicated(keep='last')]], axis=0)

    # return it, only single data
    if output in ['Open', 'High', 'Low', 'Close', 'Volume']:

        result = []
        if type(codes) == list:
            for code in codes:
                temp      = prices_data[prices_data.code == code ][output]
                temp.name = code
                result.append(temp)
            prices_data   = pd.concat(result, axis=1)

        if type(codes) == str:
            prices_data = prices_data[output]

    return prices_data


# single code to DataFrame
def get_datum(code, period = "30d", interval="86400"):

    if period[-1] not in ['d','M','Y']:
        print('Option Error : period parametor is Not in { d :day, M : month, Y : year }')
        return None

    if type(code) != str:
        print('''Input Error : please use the .get() function, this is for only single code..''')
        return None

    import requests
    from datetime import datetime
    import pandas as pd

    # input the 'codes' by KRX:005930
    split_code = code.split(':')

    # build the Query
    query = { 'x' : split_code[0],   # exchange     ex) "NASD", "KRX", "KOSDAQ"
              'q' : split_code[1],   # company code ex) "gogl", "MSFT"
              'i' : interval,        # interval time : 60 sec X n
              'p' : period }         # Total period  : {"1Y" : 1 year, "30d" : 30 days}  cf) 30D is error
    response = requests.get("https://finance.google.com/finance/getprices", params=query)
    lines    = response.text.splitlines()  # json data split to [list]

    try:
        # response the Finance Data from Google
        data, index, basetime     = [], [], 0
        for price in lines:
            cols = price.split(",")
            if cols[0][0] == 'a':
                basetime = int(cols[0][1:])
                index.append(datetime.fromtimestamp(basetime))
                data.append([float(cols[4]), float(cols[2]), float(cols[3]), float(cols[1]), int(cols[5])])
            elif cols[0][0].isdigit():
                date = basetime + (int(cols[0])*int(query['i']))
                index.append(datetime.fromtimestamp(date))
                data.append([float(cols[4]), float(cols[2]), float(cols[3]), float(cols[1]), int(cols[5])])
        df = pd.DataFrame(data, index = index, columns = ['Open', 'High', 'Low', 'Close', 'Volume'])

        # If you set the 'interval' by day..
        # just printed the Date infomation
        if int(interval) >= 86400:
            df          = df.reset_index()                          # datetimeindex to columns data
            df['index'] = df['index'].apply(lambda x : x.date())    # index is'n using the .apply()
            df          = df.set_index('index')                     # set back to index
            df.index    = pd.to_datetime(df.index)                  # set the attribute to datatimeindex
            df.index.name  = 'date'
        return df

    except:
        print('Could be Blocked by Bot..')
        return response.text[3000:6000]


def get_code(type_info=False):

    print ('We can get the Code Numbers of "NYSE", "NASDAQ" and "KRX(default)"')
    import pandas as pd

    if type_info in ['NYSE', 'NASDAQ']:
        print("Crawling the " + type_info + " 's codes")
        df = pd.read_csv('http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=' +
                          type_info + '&render=download')
        df_code = [type_info + ':'+ code    for code in df.Symbol]
        df.insert(0, 'Code', df_code)
        return df.iloc[:3, :-1]

    else:
        print("Crawling the " + "Kospi & Kosdaq (default)" + " 's codes")

        def krx_info(market = False):

            import pandas as pd
            import numpy as np
            import requests
            from io import BytesIO

            url = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
            data = {
                'method':'download',
                'orderMode':'1',           # 정렬컬럼
                'orderStat':'D',           # 정렬 내림차순
                'searchType':'13',         # 검색유형: 상장법인
                'fiscalYearEnd':'all',     # 결산월: 전체
                'location':'all',          # 지역: 전체
                "marketType": market,      # 유가증권:"stockMkt", 코스닥:"kosdaqMkt",
            }

            r   = requests.post(url, data=data)
            f   = BytesIO(r.content)
            dfs = pd.read_html(f, header=0, parse_dates=['상장일'])
            df  = dfs[0].copy()

            # 숫자를 앞자리가 0인 6자리 문자열로 변환
            df['종목코드'] = df['종목코드'].astype(np.str)
            df['종목코드'] = df['종목코드'].str.zfill(6)
            return df

        def get_code(market):
            # 유가증권:"stockMkt", 코스닥:"kosdaqMkt",
            if market == "stockMkt":
                code_head = 'KRX:'
            else:
                code_head = 'KOSDAQ:'
            kospi = krx_info(market)
            kospi = kospi.iloc[:,:2]
            kospi_code = [code_head + code   for code in kospi.종목코드]
            kospi.insert(1, 'Google', kospi_code)
            kospi = kospi.iloc[:, [2,1,0]]
            kospi.columns = ['Code', 'Google', 'Name']
            return kospi

        kospi  = get_code("stockMkt")
        kosdaq = get_code("kosdaqMkt")
        codes  = pd.concat([kospi, kosdaq])
        codes  = codes.reset_index(drop=True)
        codes_int = [ int(cod)  for cod in codes.Code]
        codes.insert(1, 'Code_int', codes_int)
        return codes