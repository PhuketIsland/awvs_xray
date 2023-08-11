import csv
from sql_do import *
import subprocess

def get_data(filename):

    with open(filename,'r',encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row["url"]
            subdomain = row["subdomain"]
            cname = row["cname"]
            ip = row["ip"]
            status = row["status"]

            if status == "200":
                # print(url, subdomain, cname, ip, status)
                Insert_into(url,subdomain,cname,ip)

def get_name():
    out = ["xxx.com.csv","xxxxx.cn.csv"]
    for i in out:
        get_data(i)


