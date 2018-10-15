# coding=utf-8
__author__ = "alvin"
__date__ = "2018/4/12 19:02"

import requests
import sys
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="article", charset="utf8")
cursor = conn.cursor()


def crawl_ips():
    header = {"User-Agent": "'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0'"}
    for i in range(100):
        re = requests.get('http://www.xicidaili.com/nn/{0}'.format(i), headers=header)
        selector = Selector(text=re.text)
        all_trs = selector.css('#ip_list tr')
        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css('.bar::attr(title)').extract_first()
            if speed_str:
                speed = float(speed_str.split("秒")[0])
                all_texts = tr.css("td::text").extract()
                ip = all_texts[0]
                port = all_texts[1]
                proxy_type = all_texts[5]

                ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:
            cursor.execute(
                "insert proxy_ip(ip, port, speed, proxy_type) values('{0}', '{1}', {2}, '{3}')".
                format(ip_info[0], ip_info[1], ip_info[3], ip_info[2])
                            )
            conn.commit()


class GetIP(object):
    def delete_ip(self, ip):
        # 删除无效ip
        delete_sql = "delete from proxy_ip where ip='{0}'".format(ip)
        cursor.execute(delete_sql)
        conn.commit()

    def judge_ip(self, ip, port):
        # 判断ip是否可用
        http_url = "https://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        proxy_dict = {
                    "http": proxy_url
        }
        try:
            response = requests.get(http_url, proxies=proxy_dict)
            return True
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code <= 200 and code < 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        #  从数据库中随机取IP
        fetch_sql = "select ip, port from proxy_ip ORDER BY RAND() LIMIT 1"
        cursor.execute(fetch_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "https://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()


if __name__ == '__main__':
    crawl_ips()



