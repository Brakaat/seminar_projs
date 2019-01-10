import requests
from bs4 import BeautifulSoup
import re

url = "http://www.taipei-seminar.com.tw/index.php"
form_data = {
    "txbTitle":"研討會",
    "cmbCondition":"研討會",
    "searchKind":"2",
    "pno":"1",
    "RadioButtonList1":"7",
    "btnRadioSearch":"搜尋",}
res = requests.post(url, form_data)
res.encoding = "utf-8"
html = res.text
bs = BeautifulSoup(html, "html.parser")
all_infos = bs.find_all("td", {"style":"font-size: 12 pt"}) 
all_times = bs.find_all("td", {"style":"font-size: 12pt"}) 
all_links = bs.find("div").find_all("a") 

re_infos = [] 
re_times = [] 
re_links = [] 
fees = []

for info in all_infos:
    re_infos.append(info.text)

for time in all_times:
    re_times.append(time.text)

titls = re_infos[1::5]
addrs = re_infos[3::5]
dates = re_times

def ewda(url):
    res = requests.get(url)
    res.encoding = "utf-8"
    html = res.text
    bs = BeautifulSoup(html, "html.parser")

    fee_content = bs.select(".boxcontent td")
    fee_info = []
    for fee in fee_content:
        fee_info.append(fee.text)
    tip_fee = "【活動費用】"
    fee = fee_info.index(tip_fee)
    fees.append(fee_info[fee+1])

    contents = bs.select(".boxcontent")
    content = []
    for cont in contents:
        content.append(cont.text.strip("\n")
                                    .replace(" ","")
                                    .replace("\r","")
                                    .replace("\t","")
                                    .replace("\xa0",""))
    content_string = ''.join(content)
    str_start = content_string.index("【課程講師】")
    str_end = str_start + 9 #向後位移9個字元
    re_links.append(content_string[str_start:str_end])
def iiiedu(url):
    res = requests.get(url)
    res.encoding = "big5"
    html = res.text
    bs = BeautifulSoup(html, "html.parser")
    infos = [] 
    all_info = bs.select("td[width]")
    for info in all_info:
        infos.append(info.text.strip("\n").replace("\r","").replace("\t","").replace(" ","").replace("\n","").replace("\xa0",""))
    re_infos = list(set(infos)) 
    re_infos.sort(key=infos.index)
    infos_string = "".join(re_infos)
    price = re.search(r"(NT\$\d+,\d+)", infos_string).group()
    fees.append(price+"元")
def clptc(url):
    res = requests.get(url)
    res.encoding = "utf-8"
    html = res.text
    bs = BeautifulSoup(html, "html.parser")
    infos = []
    all_infos = bs.select("p")
    for info in all_infos:
        infos.append(info.text
                    .replace("\r","")
                    .replace("\n","")
                    .replace("\t","")
                    .replace("\xa0","")
                    .replace("\uf06c",""))
    infos_string = "".join(infos)
    if "報名費用：" in infos_string:
        fee_start = infos_string.index("報名費用：")
        fee_end = infos_string.index("/人")
        fee = infos_string[fee_start+len("報名費用："):fee_end+len("/人")]
        fees.append(fee)

        ta_start = infos_string.index("講師介紹：姓名：")
        ta_end = ta_start+len("講師介紹：姓名：")+3
        ta = infos_string[ta_start+len("講師介紹：姓名："):ta_end]
        re_links.append("【課程講師】"+ta)
    else:
        
        fees.append("報名截止")
        re_links.append("報名截止")

for link in all_links:
    if link["href"].startswith("http://ewda.tw/"):
        ewda(link["href"])

    elif link["href"].startswith("http://www.iiiedu"):
        iiiedu(link["href"])
        re_links.append(link["href"])

    elif link["href"].startswith("https://www.clptc"):
        clptc(link["href"])

    elif link["href"].startswith("http"):
        re_links.append(link["href"])
        fees.append("check information")

    else:
        pass

for n in range(len(dates)):
    print("名稱：", titls[n], 
          "\n時間：", dates[n][0:10]+" "+dates[n][10:15],
          "\n地址：", addrs[n],
          "\n資訊：", re_links[n],
          "\n費用：", fees[n], "\n")