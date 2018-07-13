import urllib.request
import urllib.error
import itertools
import re

def buildUrl():
    nms = itertools.count(start=0, step=20)
    urls = []
    for pn in nms:
        if pn > 100:
            break
        else:
            url = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%E5%9B%BE%E7%89%87&pn=" + str(pn) + "&ct=&ic=0&lm=-1&width=0&height=0"
            urls.append(url)
    return urls

url_lists = buildUrl()
headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
     'Accept': 'text/plain, */*; q=0.01',
     'Accept-Language': 'zh-CN,zh;q=0.8',
     'X-Requested-With': 'XMLHttpRequest',
     'Connection': 'keep-alive',
    "Cookie":"__cfduid=d9625fabd71ff1ba94d67ec814e05e1571473486956; BDUSS=4tcGMxYzd-dm94ZzhzaTNqenptWVlpWFFGeUh5OGR1ZTRFMnhwNnRJekdEV0ZZSVFBQUFBJCQAAAAAAAAAAAEAAACevjl7vvTYvMq~2LwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMaAOVjGgDlYY2; BAIDUID=D6E9D0B92F3F35B1E4A7AD3CABCBAED3:FG=1; BIDUPSID=FF63886073870CA5ABC6EA2663979765; PSTM=1482469381; indexPageSugList=%5B%22king%20of%20the%20Kill%E5%A4%B4%E5%83%8F%22%2C%22%E5%88%9B%E6%84%8F%E6%91%84%E5%BD%B1%22%2C%22%E9%AB%98%E6%B8%85%E6%91%84%E5%BD%B1%22%2C%22test%22%2C%22s%20logo%22%5D; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; firstShowTip=1; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; userFrom=null",
    "referer": "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1490169358952_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E7%BE%8E%E5%A5%B3"
    }
for ul in range(0,len(url_lists)):
    req = urllib.request.Request(url=url_lists[ul], headers=headers)
    data = urllib.request.urlopen(req).read().decode('utf-8')
    pat = '"objURL":"(.*?)",'
    image_list = re.compile(pat).findall(data)
    print(len(image_list))

    for i in range(0, 20):
        try:
            urllib.request.urlretrieve(image_list[i], filename="E:/Python_test/" + str(ul) + "." +str(i) + ".jpg")
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
