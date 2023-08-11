import time
import json
import requests
from sql_do import *
from wxapi import *
from datetime import datetime, time as dt_time



class AWVSScanner:
    def __init__(self):
        self.base_url = 'https://127.0.0.1:3443/api/v1/'
        self.api_key = ''   # API_KEY
        self.headers = {"X-Auth": self.api_key, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}

    # 需要创建一个扫描组  9babebaf-b1f9-4a72-9786-66c469c3a679"为组id
    def get_group_num(self):
        url = self.base_url + 'target_groups?l=20'
        response = requests.request("GET", url, headers=self.headers)
        num = json.loads(response.text)
        for i in num["groups"]:
            if "9babebaf-b1f9-4a72-9786-66c469c3a679" == i["group_id"]:
                return i["target_count"]

    def get_data(self,ips):
        values = {
            "targets": [

            ],
            "groups": [
                "9babebaf-b1f9-4a72-9786-66c469c3a679"
            ]
        }
        numbers = self.get_group_num()
        diff_values = len(ips) - numbers   #计算差值，按索引添加新的url
        if diff_values == 0:
            return values
        else:
            for i, ip in enumerate(ips[-diff_values:],numbers):
                dict_ip = {}
                dict_ip["address"] = ip
                dict_ip["description"] = "无登录扫描" + str(i)
                values["targets"].append(dict_ip)
            return values


    # 批量添加
    def add_target(self,ips):
        url = self.base_url + 'targets/add'
        values = self.get_data(ips)
        data = bytes(json.dumps(values), 'utf-8')
        response = requests.request("POST", url, data=data, headers=self.headers)

    # 获取none_login组的所有targetid
    def get_target_ids(self):
        url = self.base_url + 'targets?l=100&q=group_id:9babebaf-b1f9-4a72-9786-66c469c3a679;&s=description:asc'
        response = requests.get(url, headers=self.headers)
        targets = response.json()['targets']
        return targets

    # 获取扫描结果
    def get_result(self,page):
        url = self.base_url + 'scans?c={}&l=100&q=group_id:9babebaf-b1f9-4a72-9786-66c469c3a679;&s=description:asc'.format(page)
        response = requests.get(url, headers=self.headers)
        scans = response.json()["scans"]
        return scans

    # 扫描
    def start_scan(self,target_id):
        url = self.base_url + 'scans'
        values = {
            "profile_id": "11111111-1111-1111-1111-111111111111",
            "ui_session_id": "30c11e18be69df40ee09e4dcb44e1bd6",
            "incremental": False,
            "schedule": {
                "disable": False,
                "start_date": None,
                "time_sensitive": False
            },
            "target_id": target_id
        }
        data = bytes(json.dumps(values), 'utf-8')
        response = requests.request("POST", url, data=data, headers=self.headers)
        scan_id = json.loads(response.text)
        return scan_id["scan_id"]


    # 配置
    def set_configuration(self,target_id):
        url = self.base_url + 'targets/'+target_id+'/configuration'
        values = {
            "ad_blocker": True,
            "authentication": {
                "enabled": False
            },
            "case_sensitive": "no",
            "client_certificate_password": "",
            "custom_cookies": [],
            "custom_headers": [],
            "debug": False,
            "default_scanning_profile_id": "11111111-1111-1111-1111-111111111111",
            "excluded_paths": [],
            "limit_crawler_scope": True,
            "login": {
                "kind": "none"
            },
            "preseed_mode": "",
            "proxy": {
                "address": "127.0.0.1",
                "enabled": True,
                "port": 10802,
                "protocol": "http"
            },
            "restrict_scans_to_import_files": False,
            "scan_speed": "slow",
            "sensor": False,
            "sensor_secret": "cd824ba514552ef52bd4a18532228490",
            "skip_login_form": False,
            "ssh_credentials": {
                "kind": "none",
                "port": 22
            },
            "technologies": [],
            "user_agent": ""
        }
        data = bytes(json.dumps(values), 'utf-8')
        response = requests.request("PATCH", url, data=data, headers=self.headers)

    # 获取扫描任务状态
    def get_scan_status(self,scan_id):
        scan_endpoint = self.base_url + 'scans/{}'.format(scan_id)
        response = requests.get(scan_endpoint, headers=self.headers)
        return response.json()['current_session']['status']

    # 判断是否在指定的时间范围内
    def is_within_time_range(self):
        current_datetime = datetime.now()

        # 指定扫描允许的日期和时间范围
        allowed_days1 = [0, 1, 2, 3, 4]  # 周一到周五
        start_time1 = dt_time(9, 0)  # 早上 9 点
        end_time1 = dt_time(11, 00)  # 晚上 9 点
        allowed_days2 = [5,6]  # 周一到周五
        start_time2 = dt_time(0, 0)  # 早上 9 点
        end_time2 = dt_time(9, 0)  # 晚上 9 点
        if current_datetime.weekday() in allowed_days1:
            return (
                current_datetime.weekday() in allowed_days1
                and start_time1 <= current_datetime.time() <= end_time1
            )
        else:
            return (
                    current_datetime.weekday() in allowed_days2
                    and start_time2 <= current_datetime.time() <= end_time2
            )


    # 扫描url列表的索引，异常中断后不至于每次都从第一个开始还能继续往下走
    def write_index(self,index):
        index = str(index)
        with open("index.txt","w",encoding="utf-8") as f:
            f.write(index)

    def read_index(self):
        with open("index.txt", "r", encoding="utf-8") as f:
            index = f.read()
            index = int(index)
            return index

    def main(self):
        # ips = get_url_sql()
        ips = ["http://43.138.109.28:80", "http://43.138.109.28:8080", "http://43.138.109.28:8090","http://43.138.109.28:8088"]
        self.add_target(ips)
        target_ids = self.get_target_ids()

        index = self.read_index()

        try:
            target_ids[index]
        except IndexError:
            print("都已扫描完毕，强制结束,如果想重新扫描，请将索引手动置为0")
            return 0
        for k,v in enumerate(target_ids,index):
            # while self.is_within_time_range():
            #     print('Waiting for scan time...')
            #     time.sleep(3600)  # 每小时检查一次
            self.write_index(k+1)
            self.set_configuration(target_ids[k]["target_id"])
            scan_id = self.start_scan(target_ids[k]["target_id"])
            print('Started scan for target:', ips[k])

            while True:
                status = self.get_scan_status(scan_id)
                print('Scan ID: {}, Target: {}, Status: {}, Time: {}'.format(scan_id, ips[k], status, datetime.now()))
                if status == 'completed':
                    break
                # # 测试用
                # if status != "processing":
                #     break

                time.sleep(300)  # 每 5分钟查询一次扫描状态
            print('Scan for target', ips[k], 'completed')
            time.sleep(2)
            scans = self.get_result(index // 100)
            vul_info = scans[index]["current_session"]["severity_counts"]
            vul_info["high"] = 1
            logical_processing(vul_info,ips[k],k+1,len(target_ids))
            # print("高危数：{}\n中危数：{}\n低危数：{}\n".format(vul_info["high"],vul_info["medium"],vul_info["low"]))
            if k >= len(target_ids) - 1:
                break
        self.write_index(0)


if __name__ == '__main__':
    awvs_scanner = AWVSScanner()
    awvs_scanner.main()
