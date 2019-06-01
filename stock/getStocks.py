import tushare as ts

ts.set_token('4abafd1cf60dc6b9bc3f2a00ad85c6395c010e794c238f937a0d4dd6')
pro = ts.pro_api()

# df_basic = pro.index_dailybasic(ts_code='000001.SH')
# df_basic.head()
data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
print(data)