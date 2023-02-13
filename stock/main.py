import tushare as ts
import yaml
import os
import mysql.connector
from sqlalchemy import create_engine
import time
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import mplfinance as mpf
# import seaborn as sns

print(ts.__version__)

def load_config():
    # 获取当前脚本所在文件夹路径
    curPath = os.path.dirname(os.path.realpath(__file__))
    # 获取yaml文件路径
    yamlPath = os.path.join(curPath, "conf/config_local.yaml")

    # open方法打开直接读出来
    f = open(yamlPath, 'r', encoding='utf-8')
    cfg = f.read()
    d = yaml.full_load(cfg)  # 用load方法转字典
    return d

cfg = load_config()
token = cfg['token']
host = cfg['mysql']['host']
user = cfg['mysql']['user']
passwd = cfg['mysql']['passwd']

globalTs = ts.pro_api(token)

# 检验数据库是否存在代码
mydb = mysql.connector.connect(
  host=host,       # 数据库主机地址
  user=user,    # 数据库用户名
  passwd=passwd,   # 数据库密码
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

isInit = False
for x in mycursor:
  if x[0] == 'd_stock':
    isInit = True

def create_databases():
  mycursor.execute("CREATE DATABASE d_stock")
  
if not isInit:
  create_databases()

mycursor.execute("USE d_stock")

mycursor.execute("SHOW TABLES")

isInitBasic = False
isInitDaily = False

for x in mycursor:
  if x[0] == 't_basic':
    isInitBasic = True
  if x[0] == 't_daily':
    isInitDaily = True
    
# engine = create_engine('mysql+pymysql://root:12345678@localhost:3306/testdb')

engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(user, passwd, host, '3306', 'd_stock'))

def read_basic():
  data = globalTs.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,fullname,enname,cnspell,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
  print(data)
  data.to_sql('t_basic', engine, index=False, if_exists='replace')
  return data
  
if not isInitBasic:
  read_basic()

def read_stock(ts_code, start_date, end_date):
  df = globalTs.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
  print(df)
  df.to_sql('t_daily', engine, index=False, if_exists='append')
  
def init_daily():
  basic = read_basic()
  for _, row in basic.iterrows():
    print(row['ts_code']) # 输出每行的索引值
    print(row['list_date']) # 输出每行的索引值
    startDate = datetime.datetime.strptime(row['list_date'], '%Y%m%d') 
    
    endDate = startDate + relativedelta(years=18)
    print(startDate)
    print(endDate)
    
    read_stock(row['ts_code'], startDate.strftime("%Y%m%d"), endDate.strftime("%Y%m%d"))
    
    time.sleep(1)
    
    if endDate < datetime.datetime.now():
      startDate = endDate + datetime.timedelta(days=1)
      endDate = datetime.datetime.now()
      print(startDate)
      print(endDate)
      read_stock(row['ts_code'], startDate.strftime("%Y%m%d"), endDate.strftime("%Y%m%d"))
      
    time.sleep(1)
    
if not isInitDaily:
  init_daily()  

def read_daily():
  sql ="""
    select * from t_daily where ts_code="000001.SZ"
"""
  data = pd.read_sql_query(sql, mydb)
  print(data)
  
  fig,axes = plt.subplots(2,1,sharex=True,figsize=(15,8))
  ax1,ax2 = axes.flatten()
  
  df_arr = data.values
  data = data.drop(labels=["ts_code", "pct_chg", "pre_close", "amount", "change"], axis=1)
  data.rename(columns={'trade_date':'Date', 'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'vol':'Volume'}, inplace=True)
  data.set_index(["Date"], inplace=True)
  data.index = pd.to_datetime(data.index)
  
  # 绘制K线图和均线图
  mpf.plot(data, type='candle', mav=(3,6,9), volume=True)
  # mpf.candlestick_ochl(ax1,df_arr,width=0.6,colorup='r',colordown='g',alpha=1.0)
  ax1.plot(df_arr[:,0],data['MA5'])
  ax1.plot(df_arr[:,0],data['MA10'])
  
  ax1.grid()
  ax1.xaxis_date()
  ax1.set_title('平安银行',fontsize=16)
  ax1.set_ylabel('价格',fontsize=16)
  
  # 绘制每日成交量图
  ax2.bar(df_arr[:,0],df_arr[:,5])
  ax2.set_xlabel('日期',fontsize=16)
  ax2.set_ylabel('成交量',fontsize=16)
  ax1.grid()

  # with engine.connect() as conn, conn.begin():
    # data=pd.read_sql_table("t_daily", conn)
    # data.to_csv('t_daily.csv')

# 标题格式，字体为中文字体，颜色为黑色，粗体，水平中心对齐
title_font = {'fontname': 'Microsoft YaHei',
              'size':     '16',
              'color':    'black',
              'weight':   'bold',
              'va':       'bottom',
              'ha':       'center'}
# 红色数字格式（显示开盘收盘价）粗体红色24号字
large_red_font = {'fontname': 'Microsoft YaHei',
                  'size':     '24',
                  'color':    'red',
                  'weight':   'bold',
                  'va':       'bottom'}
# 绿色数字格式（显示开盘收盘价）粗体绿色24号字
large_green_font = {'fontname': 'Microsoft YaHei',
                    'size':     '24',
                    'color':    'green',
                    'weight':   'bold',
                    'va':       'bottom'}
# 小数字格式（显示其他价格信息）粗体红色12号字
small_red_font = {'fontname': 'Microsoft YaHei',
                  'size':     '12',
                  'color':    'red',
                  'weight':   'bold',
                  'va':       'bottom'}
# 小数字格式（显示其他价格信息）粗体绿色12号字
small_green_font = {'fontname': 'Microsoft YaHei',
                    'size':     '12',
                    'color':    'green',
                    'weight':   'bold',
                    'va':       'bottom'}
# 标签格式，可以显示中文，普通黑色12号字
normal_label_font = {'fontname': 'Microsoft YaHei',
                     'size':     '12',
                     'color':    'black',
                     'va':       'bottom',
                     'ha':       'right'}
# 普通文本格式，普通黑色12号字
normal_font = {'fontname': 'Microsoft YaHei',
               'size':     '12',
               'color':    'black',
               'va':       'bottom',
               'ha':       'left'}


def fig_text(plot_data, my_style):
  # data是测试数据，可以直接下载后读取，在下例中只显示其中100个交易日的数据
  # plot_data = data.iloc[100: 200]
  # 读取显示区间最后一个交易日的数据
  last_data = plot_data.iloc[-1]
  # 使用mpf.figure()函数可以返回一个figure对象，从而进入External Axes Mode，从而实现对Axes对象和figure对象的自由控制
  fig = mpf.figure(style=my_style, figsize=(12, 8), facecolor=(0.82, 0.83, 0.85))
  # 添加三个图表，四个数字分别代表图表左下角在figure中的坐标，以及图表的宽（0.88）、高（0.60）
  ax1 = fig.add_axes([0.06, 0.25, 0.88, 0.60])
  # 添加第二、三张图表时，使用sharex关键字指明与ax1在x轴上对齐，且共用x轴
  ax2 = fig.add_axes([0.06, 0.15, 0.88, 0.10], sharex=ax1)
  ax3 = fig.add_axes([0.06, 0.05, 0.88, 0.10], sharex=ax1)
  # 设置三张图表的Y轴标签
  ax1.set_ylabel('价格')
  ax2.set_ylabel('成交量')
  ax3.set_ylabel('macd')
  # 在figure对象上添加文本对象，用于显示各种价格和标题
  fig.text(0.50, 0.94, '平安银行股票行情', **title_font)
  fig.text(0.12, 0.90, '开/收: ', **normal_label_font)
  fig.text(0.14, 0.89, f'{np.round(last_data["Open"], 3)} / {np.round(last_data["Close"], 3)}', **large_red_font)
  fig.text(0.14, 0.86, f'{last_data["change"]}', **small_red_font)
  # fig.text(0.22, 0.86, f'[{np.round(last_data["pct_chg"], 2)}%]', **small_red_font)
  # fig.text(0.12, 0.86, f'{last_data.name.date()}', **small_red_font)
  fig.text(0.40, 0.90, '高: ', **normal_label_font)
  fig.text(0.40, 0.90, f'{last_data["High"]}', **small_red_font)
  fig.text(0.40, 0.86, '低: ', **normal_label_font)
  fig.text(0.40, 0.86, f'{last_data["Low"]}', **small_red_font)
  fig.text(0.55, 0.90, '量(万手): ', **normal_label_font)
  fig.text(0.55, 0.90, f'{np.round(last_data["Volume"] / 10000, 3)}', **small_red_font)
  fig.text(0.55, 0.86, '额(千元): ', **normal_label_font)
  fig.text(0.55, 0.86, f'{last_data["amount"]}', **small_red_font)
  # fig.text(0.70, 0.90, '涨停: ')
  # fig.text(0.70, 0.90, f'{last_data["upper_lim"]}')
  # fig.text(0.70, 0.86, '跌停: ')
  # fig.text(0.70, 0.86, f'{last_data["lower_lim"]}')
  # fig.text(0.85, 0.90, '均价: ')
  # fig.text(0.85, 0.90, f'{np.round(last_data["average"], 3)}')
  fig.text(0.85, 0.86, '昨收: ', **normal_label_font)
  fig.text(0.85, 0.86, f'{last_data["pre_close"]}', **small_red_font)
  # 调用mpf.plot()函数，注意调用的方式跟上一节不同，这里需要指定ax=ax1，volume=ax2，将K线图显示在ax1中，交易量显示在ax2中
  mpf.plot(plot_data, mav=(3, 6, 9, 30),
      ax=ax1,
      volume=ax2,
      type='candle',
      style=my_style)

  fig.show()
  plt.savefig('1.png')
  plt.show()


def main():
  # read_daily()
  # 参考链接: https://blog.csdn.net/Shepherdppz/article/details/117575286
  df = globalTs.daily(ts_code='000001.SZ', start_date='20220601', end_date='20230212')
  # 删除 tushare 提供的不需要的数据，保留 Date, Open, High, Low, Close, Volume
  # df = df.drop(labels=["ts_code", "pct_chg", "pre_close", "amount", "change"], axis=1)
  
  # 对数据进行改名，mplfinance有要求
  df.rename(
      columns={'trade_date': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'vol': 'Volume'},
      inplace=True)
      
  # 转换时间序列
  df = df[::-1]
  
# 将Date设置为索引，并转换为 datetime 格式
  df.set_index(["Date"], inplace=True)
  df.index = pd.to_datetime(df.index)
  
  # 显示中文
  plt.rcParams['font.sans-serif'] = ['SimHei']
  # 显示负数
  plt.rcParams['axes.unicode_minus'] = False


  # 设置mplfinance的蜡烛颜色，up为阳线颜色，down为阴线颜色
  my_color = mpf.make_marketcolors(up='r',
                                  down='g',
                                  edge='inherit',
                                  wick='inherit',
                                  volume='inherit')
  # 使用mplfinance库绘图
  # 选择平安银行2020年11月和12月的数据进行绘图
  # 只需要多加一句：
  s = mpf.make_mpf_style(marketcolors= my_color,
                         base_mpf_style='yahoo', 
                         rc={'font.family': 'SimHei', 'axes.unicode_minus': False})
  # 即在继承了原有style的基础上,重新定义了style。其中base_mpf_style为原设定的style。然后把新的风格s作为style的值传入下边绘图函数中。

  fig_text(df, s)
  # mpf.plot(df, mav=(3, 6, 9),
  #        title='平安银行股票行情',		# 设置图标标题
  #        style=s,				# 应用上面设置的样式
  #        type='candle',			# 设置显示样式 选项[‘ohlc’, ‘candle’, ‘line’, ‘renko’, ‘pnf’]
  #        ylabel='元/股',		# 设置 Y轴标题
  #        xlabel='日期',  # 设置横座标名称
  #        volume=True,			# 下方是否显示成交量
  #       #  show_nontrading=True,	# 是否跳过非交易日 默认False
  #        ylabel_lower='成交量',	# 成交量图标的Y轴标题
  #        datetime_format='%m-%d',	# X轴时间显示的格式
  #        xrotation=45,			# X轴时间显示 旋转的角度
  #        linecolor='#00ff00',	# 若type='line' 设置线条颜色
  #        tight_layout=False,	# 是否紧密显示
  #       #  marketcolors=my_color
  #        )
  
  np.fft.fft()
  
  print('Finished')
  
if __name__== "__main__" :
  main()
