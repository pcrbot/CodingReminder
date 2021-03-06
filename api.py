from datetime import datetime
from datetime import timedelta
from .utils import *
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
import requests
from bs4 import BeautifulSoup


def getNiuKeSchool():
    url = 'https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=14'

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    div = soup.find_all("div", class_='platform-item js-item')

    name = []
    time = []
    link = []

    for it in div:
        div1 = it.find("div", class_='platform-item-cont')
        # print(div1)
        a = div1('a')
        i = div1('i')
        li = div1.find("li", class_='match-time-icon')

        if (len(i) > 0):
            if ("加密" in i[0]['title']):
                continue

        name.append(a[0].string)
        link.append("https://ac.nowcoder.com" + a[0]['href'])
        time.append(li.string[5:21])

    data = {}

    for i in range(0, len(name)):
        data[name[i]] = {}
        data[name[i]]['time'] = time[i]
        data[name[i]]['link'] = link[i]

    save_json("niuke_school.json", data)


def getAtcoder():
    url = 'https://atcoder.jp/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0)Gecko/20100101 Firefox/66.0"
    }
    r = requests.get(url, timeout=30, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find("div", id="contest-table-upcoming")

    if div is None:

        print("最近没有比赛")
        data = {"最近没有比赛" : "......"}
        save_json("atcoder.json", data)


    else:
        name = []
        time = []
        link = []
        tbody = div.find("tbody")
        for it in tbody.find_all("tr"):
            a = it.find_all("a")
            link.append("https://atcoder.jp" + a[1]['href'])
            time.append(a[0].string)
            name.append(a[1].string)


        data = {}

        for i in range(0, len(name)):
            ti = time[i][:-8]
            date = datetime.strptime(ti, '%Y-%m-%d %H:%M')
           # print(date)
            #print(name[i])
            data[name[i]] = {}
            data[name[i]]['time'] = (date - timedelta(hours = 1)).strftime("%Y-%m-%d %H:%M")
            data[name[i]]['link'] = link[i]

       # print(data)
        save_json("atcoder.json", data)


def getCodeChef():
    url = 'https://www.codechef.com/contests'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    r = requests.get(url, timeout=30, headers=headers)
    if (r.status_code != 200):  # 由于codechef网站访问比较慢当出错的时候就在进行访问一次
        r = requests.get(url, timeout=30, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find_all("table", class_="dataTable")
    table = table[1]
    tbody = table.find("tbody")
    name = []
    time = []
    link = []

    data_time = tbody.find_all("td", class_="start_date")
    for it in tbody.find_all('td'):
        # print(it)

        a = it.find("a")

        if a is not None:
            name.append(a.string)
            print(a['href'])
            link.append("https://www.codechef.com" + a['href'])

    for it in data_time:
        time.append(it.text)

    for i in range(0, len(time)):
        date = datetime.strptime(time[i], '%d %b %Y  %H:%M:%S')
        time[i] = (date + timedelta(hours = 2, minutes = 30)).strftime("%Y-%m-%d %H:%M")  # 印度与中国时间相差2时30分
    # 创建字典 比赛名称-->时间
    data = {}

    for i in range(0, len(time)):
        data[name[i]] = {}
        data[name[i]]['time'] = time[i]
        data[name[i]]['link'] = link[i]

    # 将获取的字典信息 导入json  不建议用数据库 因为信息比较少用json文件方便
    save_json("codechef.json", data)


def getCodefores():
    contest_name = []
    contest_time = []
    contest_id = []
    urls = 'https://codeforces.com/contests'
    r = requests.get(urls, timeout=30)
    if r.status_code != 200:
        return
    else:

        soup = BeautifulSoup(r.text, "html.parser")
        div = soup.find("div", class_="contestList")
        table = div.find("table", class_="")
        for tr in table.find_all('tr'):
            for td in tr.find_all('td'):
                if td.text.count('\n') <= 2:
                    contest_name.append(td.text.strip())
                else:
                    contest_name.append(td.text[:td.text.find('\n', td.text.find('\n') + 1) + 1].strip())
                contest_id.append(tr.get('data-contestid'))
                break

        for tr in table.find_all('tr'):
            # print(tr)
            for td in tr.find_all('td'):
                span = td.find("span", class_='format-time')
                if span:
                    contest_time.append(span.string)

        t = []
        for it in contest_time:
            dete = datetime.strptime(it, '%b/%d/%Y %H:%M')
            #print(dete)
            times = dete + timedelta(hours = 5, minutes = 0)
            t.append(times.strftime("%Y-%m-%d %H:%M"))
        data = {}
        for i in range(0, len(contest_time)):
            if 'Div. 1' in contest_name[i]:
                continue
            data[contest_name[i]] = {}
            data[contest_name[i]]['time']= t[i]
            data[contest_name[i]]['link']= "https://codeforces.com/contest/" + contest_id[i]

        save_json("cf.json", data)

def getNiuKe():
    url = 'https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=13'
    html = requests.get(url)
    if html.status_code != 200:
        return
    else:
        soup = BeautifulSoup(html.text, "html.parser")
        data = {}
        data1 = {}

        div = soup.find("div", class_="nk-main with-banner-page clearfix js-container")
        div_content = div.find("div", class_="nk-content")
        div_contest = div_content.find("div", class_="platform-mod js-current")
        for contest in div_contest.find_all("div", class_="platform-item js-item"):
            next = contest.find("div", class_="platform-item-cont")
            a = next.find("a")
            li = next.find('li', class_='match-time-icon')
            link = a['href']
            name = a.string
            if "小白" in name or "练习赛" in name or "周赛" in name or "挑战赛" in name or "月赛" in name or "竞赛" in name:
                data[name] = li.string
                data1[name] = "https://ac.nowcoder.com" + link
        name = list(data)
        f = 0
        for it in name:
            time = data[it][:21]
            time = time[5:]
            data[it] = time
            data[it] = {}
            data[it]['time'] = time
            data[it]['link'] = data1[it]

        save_json("niuke.json", data)

def getNews():
    url = 'https://news.cnblogs.com/'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    content = []
    link = []
    div = soup.find("div", id="news_list")
    for h in div.find_all("h2"):
        a = h.find('a')
        content.append(a.string)
        link.append(a['href'])

    text = ""
    for i in range(0, 10):
        #cnt = random.randint(0, len(content))
        text += str(i +1) +"." + content[i] +"\n"
        text +=  'https://news.cnblogs.com' + link[i] +"\n"
    return text