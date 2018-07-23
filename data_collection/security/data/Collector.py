import base.FinanceDataSource as fd
import tushare as ts
import base.Dao as dao
import time

securities = fd.get_all_securities()
endDate = "2018-07-20"
for code in securities:
    count = 0
    df = ts.get_k_data(code, fd.preOpenDate(endDate, 100), endDate)
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
    dao.updatemany("insert into security_data(code, date, open, close, high, low, volume) values(%s,%s,%s,%s,%s,%s,%s)", arr_values)
    time.sleep(0.5)
