import base.FinanceDataSource as fd
import tushare as ts
import base.Dao as dao
import time

def caculateMarketAnd2DB():
    openDates = fd.getOpenDates()
    openDates.reverse()

    for date in openDates:
        if date == '' or date > '2018-07-20' or date < '2018-02-28': continue

        arr = dao.select("select code, date, open, close, high, low, volume from "
                   "security_data where date=%s", (date))

        ye_arr = dao.select("select code, date, open, close, high, low, volume from "
                   "security_data where date=(select max(date) from security_data where date<%s) ", (date))

        ty_arr = dao.select("select code, date, open, close, high, low, volume from "
                            "security_data where date=(select max(date) from security_data where date<%s) ", (fd.preOpenDate(date, 1)))

        code_item = {}
        code_ye_item = {}
        code_ty_item = {}
        for item in arr: code_item[item['code']] = item
        for ye_item in ye_arr: code_ye_item[ye_item['code']] = ye_item
        for ty_item in ty_arr: code_ty_item[ty_item['code']] = ty_item
        open_yzzt = 0
        open_yzdt = 0
        ye_dt = 0
        ye_zrzt = 0
        for item in arr:
            code = item['code']
            try:
                ye_item = code_ye_item[code]
            except:
                _date = item['date']
                ye_items = dao.select("select code, date, open, close, high, low, volume from security_data "
                                     "where code=%s and date=(select max(date) from security_data where date<%s and code=%s) ",
                                     (code, _date, code))
                if ye_items is None or ye_items.__len__() == 0:
                    continue
                else:
                    ye_item = ye_items[0]
            try:
                ty_item = code_ty_item[code]
            except:
                _date = ye_item['date']
                ty_items = dao.select("select code, date, open, close, high, low, volume from security_data "
                                     "where code=%s and date=(select max(date) from security_data where date<%s and code=%s) ",
                                     (code, _date, code))
                if ty_items is None or ty_items.__len__() == 0:
                    continue
                else:
                    ty_item = ty_items[0]

            if(is_open_yzzt(item, ye_item) == True):
                open_yzzt = open_yzzt + 1
            if (is_open_yzdt(item, ye_item) == True):
                open_yzdt = open_yzdt + 1
            if (is_ye_dt(ye_item, ty_item) == True):
                ye_dt = ye_dt + 1
            if (is_ye_zrzt(ye_item, ty_item) == True):
                ye_zrzt = ye_zrzt + 1
            print("-->date: " + date)

        print('Date: ' + date + ' open_yzzt: ' + str(open_yzzt) + ' open_yzdt: ' + str(open_yzdt) + ' ye_dt: ' + str(ye_dt) + ' ye_zrzt:' + str(ye_zrzt))
        dao.update("delete from market_env where date=%s", (date))
        dao.update("insert into market_env(date, open_yzzt, open_yzdt, ye_dt, ye_zrzt) values(%s,%s,%s,%s,%s)", (date, open_yzzt, open_yzdt, ye_dt, ye_zrzt))

        # for item in arr:
        #     code = item['code']
        #     pre_date = fd.preOpenDate(item['date'], 1)
        #     ty_date  = fd.preOpenDate(item['date'], 2)
        #     ye_item = dao.select("select code, date, open, close, high, low, volume from "
        #                          "security_data where code=%s and date=%s", (code, pre_date))[0]
        #     ty_item = dao.select("select code, date, open, close, high, low, volume from "
        #                          "security_data where code=%s and date=%s", (code, ty_date))[0]
        #     if(is_open_yzzt(item, ye_item) == True):
        #         open_yzzt = open_yzzt + 1
        #     if (is_open_yzdt(item, ye_item) == True):
        #         open_yzdt = open_yzdt + 1
        #     if (is_ye_dt(ye_item, ty_item) == True):
        #         ye_dt = ye_dt + 1
        #     if (is_ye_zrzt(ye_item, ty_item) == True):
        #         ye_zrzt = ye_zrzt + 1
        #     print("-->date: " + date)
        #
        #     count = count + 1
        # print('Date: ' + date + ' open_yzzt: ' + str(open_yzzt) + ' open_yzdt: ' + str(open_yzdt) + ' ye_dt: ' + str(ye_dt) + ' ye_zrzt:' + str(ye_zrzt))

def is_open_yzzt(item, ye_item):
    open = float(item['open'])
    pre_close = float(ye_item['close'])
    open_rate = round(float((open - pre_close)/pre_close)*100, 2)
    if open_rate >= 9.89:
        return True
    else:
        return False

def is_open_yzdt(item, ye_item):
    open = float(item['open'])
    pre_close = float(ye_item['close'])
    open_rate = round(float((open - pre_close)/pre_close)*100, 2)
    if open_rate <= -9.89:
        return True
    else:
        return False

def is_ye_dt(ye_item, ty_item):
    pre_close = float(ye_item['close'])
    ty_close = float(ty_item['close'])
    open_rate = round(float((pre_close - ty_close)/ty_close)*100, 2)
    if open_rate <= -9.89:
        return True
    else:
        return False

def is_ye_zrzt(ye_item, ty_item):
    pre_close = float(ye_item['close'])
    ty_close = float(ty_item['close'])
    pre_open = ye_item['open']
    pre_high = ye_item['high']
    open_rate = round(float((pre_close - ty_close)/ty_close)*100, 2)
    if open_rate >= 9.89 and pre_open != pre_high:
        return True
    else:
        return False



def crawlSecurityData(endDate, daysCount):
    securities = fd.get_all_securities()
    #endDate = "2018-07-20"
    for code in securities:
        count = 0
        df = ts.get_k_data(code, fd.preOpenDate(endDate, daysCount), endDate)
        arr_values = []
        while count < df.index.__len__():
            open = str(df['open'].values[count])
            close = str(df['close'].values[count])
            high = str(df['high'].values[count])
            low = str(df['low'].values[count])
            volume = str(df['volume'].values[count])
            date = str(df['date'].values[count])
            arr_values.append((code, date, open, close, high, low, volume))
            count = count + 1
            print("Date: " + date + " Code: " + code)

        dao.update("delete from security_data where code=%s", (code,))
        dao.updatemany(
            "insert into security_data(code, date, open, close, high, low, volume) values(%s,%s,%s,%s,%s,%s,%s)",
            arr_values)
        time.sleep(0.5)

caculateMarketAnd2DB()

