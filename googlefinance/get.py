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

        def get_krx(date=None, market = 'ALL'):
            import requests
            import pandas as pd
            from io import BytesIO
            from datetime import datetime

            if date == None:
                date = datetime.today().strftime('%Y%m%d')

            headers               = requests.utils.default_headers()
            headers['User-Agent'] = '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'''
            gen_otp_url  = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
            gen_otp_data = {'name'         : 'fileDown',
                            'filetype'     : 'xls',
                            'market_gubun' : market,     # 'STK': Kospi
                            'url'          : 'MKD/04/0404/04040200/mkd04040200_01',
                            'indx_ind_cd'  : '', 'sect_tp_cd'   : '',
                            'schdate'      : date,
                            'pagePath'     : '/contents/MKD/04/0404/04040200/MKD04040200.jsp', }
            r                     = requests.post(gen_otp_url, gen_otp_data, headers=headers)
            OTP_code              = r.content

            # Ajax XLS file download
            down_url  = 'http://file.krx.co.kr/download.jspx'
            down_data = {'code': OTP_code}
            r         = requests.post(down_url, down_data)
            df        = pd.read_excel(BytesIO(r.content), header=0, thousands=',')
            return df


        krx   = get_krx().iloc[:,:2]              # 상장기업 모든목록
        kospi = get_krx(market='STK').iloc[:,:2]  # 상장사  기업목록

        import pandas as pd
        kosdaq_code = [ code   for code      in  krx['종목코드']
                               if  code  not in  list(kospi['종목코드']) ]

        kosdaq_ = [krx[krx['종목코드'] == code]  for code in kosdaq_code]
        kosdaq  = pd.concat(kosdaq_, axis = 0)
        kosdaq  = kosdaq.reset_index(drop = True)
        kosdaq.columns = ['No','Name']
        kosdaq_code    = ['KOSDAQ:' + code  for code in kosdaq.No]
        kosdaq.insert(0, 'Code', kosdaq_code)

        kospi.columns  = ['No','Name']
        kospi_code     = ['KRX:' + code  for code in kospi.No]
        kospi.insert(0, 'Code', kospi_code)

        df = pd.concat([kosdaq, kospi], axis=0)
        df = df.reset_index(drop = True)
        return df
