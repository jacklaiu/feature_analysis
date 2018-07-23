import base.FinanceDataSource as fds
import data_collection.security.feature.Dao as sdao
import tushare as ts

rows = sdao.getCodeAndDateArray()
# for row in rows:
#     code = row['code']
#     date = row['date']
#     continuous_z_day_count = fds.get_continuous_z_day_count(code, date)
#     sdao.updateColume(code, date, "continuous_z_day_count", continuous_z_day_count)
#     print("Code: " + code + " Date: " + date + " continuous_z_day_count: " + str(continuous_z_day_count))

# for row in rows:
#     code = row['code']
#     date = row['date']
#     ty_chg = fds.get_ty_chg(code, date)
#     sdao.updateColume(code, date, "ty_chg", ty_chg)
#     print("Code: " + code + " Date: " + date + " ty_chg: " + str(ty_chg))

df = ts.get_stock_basics()
# outstanding_code_dict = {}
# for code in df.index:
#     row = df['outstanding'][code]*1000000
#     outstanding_code_dict[code] = row

# for row in rows:
#     code = row['code']
#     date = row['date']
#     volume = ts.get_k_data(code, date, date)['volume'].values[0]
#     date = fds.preOpenDate(date, 1)
#     ye_volume = ts.get_k_data(code, date, date)['volume'].values[0]
#     outstanding = outstanding_code_dict[code]
#     tr = round(float(volume/outstanding)*100, 2)
#     ye_tr = round(float(ye_volume/outstanding)*100, 2)
#     sdao.updateColume(code, row['date'], "ye_tr", str(ye_tr))
#     sdao.updateColume(code, row['date'], "tr", str(tr))
#     print("Code: " + code + " Date: " + date + " ye_tr: " + str(ye_tr))
#     print("Code: " + code + " Date: " + date + " tr: " + str(tr))

for row in rows:
    code = row['code']
    date = row['date']
    start = fds.preOpenDate(date, 4)
    end = date
    df = ts.get_k_data(code, start, end)
    total = 0
    count = 0
    for close in df['close'].values:
        if count == (df['close'].values.__len__() - 1):
            open = df['open'].values[count]
            total = total + open
        else:
            total = total + close
        count = count + 1
    ma5_inopen = total / 5
    open_ma5_distance_rate = round((open - ma5_inopen)/close*100, 2)
    sdao.updateColume(code, row['date'], "open_ma5_distance_rate", str(open_ma5_distance_rate))
    print("Code: " + code + " Date: " + date + " open_ma5_distance_rate: " + str(open_ma5_distance_rate))



