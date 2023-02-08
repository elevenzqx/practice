import tushare as ts
import yaml
import os
import mysql.connector

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
print(host)
globalTs = ts.pro_api(token)

def read_stock():
    df = globalTs.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')

def main():
    print("Hello, World!")


mydb = mysql.connector.connect(
  host="127.0.0.1",       # 数据库主机地址
  user="root",    # 数据库用户名
  passwd="12345678"   # 数据库密码
)
mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")
 
for x in mycursor:
  print(x)

if __name__== "__main__" :
    main()
