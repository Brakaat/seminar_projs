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

infos = bs.select("div[align] td[style]")
info = []
# 五個一組
for i in infos:
    info.append(i)
step = 6
info = [info[n:n+step] for n in range(0,len(info),step)]

links = bs.find("div").find_all("a") 
url = []
for link in links:
    if link["href"].startswith("http"):
        url.append(link["href"])

def ewda(url):
    res = requests.get(url)
    res.encoding = "utf-8"
    html = res.text
    bs = BeautifulSoup(html, "html.parser")

    top_content = bs.select(".boxcontent td")
    info = []
    for top in top_content:
        info.append(top.text)
    tip_fee = "【活動費用】"
    fee = info.index(tip_fee)
    print("費用："+info[fee+1])

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
    name = content_string[str_start+len("【課程講師】"):str_end]
    print("講師："+name)
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
    print("費用："+price+"元")
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
        print("費用："+fee)

        ta_start = infos_string.index("講師介紹：姓名：")
        ta_end = ta_start+len("講師介紹：姓名：")+3
        ta = infos_string[ta_start+len("講師介紹：姓名："):ta_end]
        print("課程講師："+ta)
    else:
        
        print("報名截止")

count = 0
for i in info:
    name = i[0].text
    if name == "ewdaewda":
        print("名稱："+i[1].text
            +"\n主辦單位："+i[2].text
            +"\n時間："+i[3].text[0:10]+" "+i[3].text[10:15]
            +"\n地址："+i[4].text
            +"\n連結："+url[count])
        ewda(url[count])
        print("---------------------------------")

    elif name == "iiiedu":
        print("名稱："+i[1].text
            +"\n主辦單位："+i[2].text
            +"\n時間："+i[3].text[0:10]+" "+i[3].text[10:15]
            +"\n地址："+i[4].text
            +"\n連結："+url[count])
        iiiedu(url[count])
        print("---------------------------------")
    elif name == "tiensir":
        print("名稱："+i[1].text
            +"\n主辦單位："+i[2].text
            +"\n時間："+i[3].text[0:10]+" "+i[3].text[10:15]
            +"\n地址："+i[4].text
            +"\n連結："+url[count])
        clptc(url[count])
        print("---------------------------------")
    count += 1
