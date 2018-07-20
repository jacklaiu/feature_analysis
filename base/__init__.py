import tushare as ts

start = "2018-07-17"
end = "2018-07-19"
dataf = ts.get_k_data('002636', start="2018-07-16", end="2018-07-20")
df = dataf[(dataf['date']>=start) & (dataf['date']<=end)]
for row in dataf.values:
    print(row[0])