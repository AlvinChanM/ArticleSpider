# coding=utf-8
__author__ = "alvin"
__date__ = "2018/4/9 19:13"

import requests
s = requests.session()
headers = {
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/signup?next=%2F',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/64.0.3282.140 Safari/537.36',
        'Cookie': 'q_c1=bbe313be5f10409fac05a3894738446c|1522660227000|1522660227000; __DAYU_PP=3YuZ3vQfiJQqny2Ff7Fy3d6328efaf58; _zap=8ef1ed29-d303-4868-b67d-a519ecc89750; l_cap_id="YWNmMTlmYzkwYWIyNGQ4MThlOGNhNTQ2MjY0ZjdkYmQ=|1523277955|e8e2292c01122c5d76c0cf7ee640dac853299fd0"; r_cap_id="MDcxMzAwY2ViMGNiNDQ0NmIyNjBjNWQ0MDdjZDg0NzI=|1523277955|6803414603aafec44b3b7abf83df575cc4010ba1"; cap_id="ZTYyZjY0MTg1ZTMwNDAyYmIwYzUwM2ZkN2YzNDMyOTU=|1523277955|4b15e1ce026a7b33d5a67e501f2e5ccbd01e0b6e"; aliyungf_tc=AQAAAFU/7XIyxwEAzrddZds8r2XJpOP2; _xsrf=2439fef6-4320-4df2-a858-135e18146e0e; d_c0="AADgiO2Faw2PTmWlEc8kJAlzAciyWiFBjbE=|1523334056"; __utma=51854390.1712126696.1523334092.1523334092.1523334092.1; __utmc=51854390; __utmz=51854390.1523334092.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/chen-miao-26-34/activities; __utmv=51854390.100--|2=registration_date=20161008=1^3=entry_date=20161008=1; capsion_ticket="2|1:0|10:1523337095|14:capsion_ticket|44:Y2EwZjE2MmQzNjkzNDVhY2IxMTg1ZmIyNGU1M2JlZGI=|456e9376edde330b49a6e827c8e9293208e68da215f360c6e0be01d575b13ce2"; z_c0="2|1:0|10:1523337123|4:z_c0|92:Mi4xVi1pTEF3QUFBQUFBQU9DSTdZVnJEU1lBQUFCZ0FsVk5vNVc1V3dEeThFZF9hUEdJaC1nYXlOV0t3Z1pvZWlSMmd3|6aa44a6074d2eaaf406133a2ab017c5ebaf324f7d428b3e22906b4c313aa4583"'
}
# cookies = {'Cookie': 'q_c1=bbe313be5f10409fac05a3894738446c|1522660227000|1522660227000; __DAYU_PP=3YuZ3vQfiJQqny2Ff7Fy3d6328efaf58; _zap=8ef1ed29-d303-4868-b67d-a519ecc89750; l_cap_id="YWNmMTlmYzkwYWIyNGQ4MThlOGNhNTQ2MjY0ZjdkYmQ=|1523277955|e8e2292c01122c5d76c0cf7ee640dac853299fd0"; r_cap_id="MDcxMzAwY2ViMGNiNDQ0NmIyNjBjNWQ0MDdjZDg0NzI=|1523277955|6803414603aafec44b3b7abf83df575cc4010ba1"; cap_id="ZTYyZjY0MTg1ZTMwNDAyYmIwYzUwM2ZkN2YzNDMyOTU=|1523277955|4b15e1ce026a7b33d5a67e501f2e5ccbd01e0b6e"; aliyungf_tc=AQAAAFU/7XIyxwEAzrddZds8r2XJpOP2; _xsrf=2439fef6-4320-4df2-a858-135e18146e0e; d_c0="AADgiO2Faw2PTmWlEc8kJAlzAciyWiFBjbE=|1523334056"; __utma=51854390.1712126696.1523334092.1523334092.1523334092.1; __utmc=51854390; __utmz=51854390.1523334092.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/chen-miao-26-34/activities; __utmv=51854390.100--|2=registration_date=20161008=1^3=entry_date=20161008=1; capsion_ticket="2|1:0|10:1523337095|14:capsion_ticket|44:Y2EwZjE2MmQzNjkzNDVhY2IxMTg1ZmIyNGU1M2JlZGI=|456e9376edde330b49a6e827c8e9293208e68da215f360c6e0be01d575b13ce2"; z_c0="2|1:0|10:1523337123|4:z_c0|92:Mi4xVi1pTEF3QUFBQUFBQU9DSTdZVnJEU1lBQUFCZ0FsVk5vNVc1V3dEeThFZF9hUEdJaC1nYXlOV0t3Z1pvZWlSMmd3|6aa44a6074d2eaaf406133a2ab017c5ebaf324f7d428b3e22906b4c313aa4583"'}
response = s.get('https://www.zhihu.com/settings/profile', headers=headers, verify=False,
                 allow_redirects=False)
# with open("zhihu.index", "wb") as f:
#     f.write(response.text.encode('utf8'))
# res = s.get('https://www.zhihu.com/settings/profile',headers=headers)
print(response.text)