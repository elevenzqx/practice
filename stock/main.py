import tushare as ts
import yaml
import os
import mysql.connector
from sqlalchemy import create_engine
import time
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

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
  with engine.connect() as conn, conn.begin():
    data=pd.read_sql_table("t_daily", conn)
    print(data)
    # data.to_csv('t_daily.csv')


def main():
  read_daily()
  print('Finished')
  
if __name__== "__main__" :
  main()
