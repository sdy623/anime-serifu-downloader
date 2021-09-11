# coding:utf8
import os
import time
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


def search(bangumi_name: str) -> list:

    headers_search = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/88.0.4324.104 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;\
            q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,\
            application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://anicobin.ldblog.jp/search?\
            q=%E5%91%8A%E7%99%BD&x=8&y=13',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    }

    params_search = (
        ('q', bangumi_name),
        ('x', '13'),
        ('y', '9'),
    )

    id = 0
    result_list = []

    response = requests.get('http://anicobin.ldblog.jp/search', 
                            headers=headers_search, params=params_search,  
                            verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    # 找到所有class=info的div标签内容
    div = soup.find_all('h2', attrs={'class': 'top-article-title entry-title'})
    for elem in div:
        mydict = {}
        id += 1
        # link = elem.find('a')['href'] # 找到每个音频链
        mydict['id'] = id
        mydict['title'] = elem.string
        mydict['link'] = elem.find('a')['href']
        result_list.append(mydict)
    return result_list


def pick(i, result_list: list) -> str:
    i = int(i)-1
    tg_title = result_list[i]['title']
    # print(tg_title)
    serifu_url = result_list[i]['link']
    return serifu_url


def get_serifu(serifu_url: str) -> str:
    cookies = {
        'ldblog_u': '97c795cc40069e70ad52a23e638a4d07',
        'ldblog_v': '1',
        'ldblog_c': '1',
        'ldblog_f': '1612345539',
        'livedoor-blog-gdpr-agreed': '1',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104\
                 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,\
            image/avif,image/webp,image/apng,*/*;q=0.8,application/signed\
                -exchange;v=b3;q=0.9',
        'Referer': 'http://anicobin.ldblog.jp/search?q=%E3%81%8B%E3%81%90\
            %E3%82%84%E6%A7%98%E3%81%AF%E5%91%8A%E3%82%89%E3%81%9B%E3%81%\
                9F%E3%81%84&x=13&y=9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    }
    pbar = tqdm(total=100)
    response = requests.get(serifu_url, headers=headers,
                            cookies=cookies, verify=False)
    pbar.update(50)
    sou_gennbunn = ''
    soup = BeautifulSoup(response.text, "lxml")
    pbar.update(20)
    div = soup.find_all('span', attrs={
                        'style': 'color:#06C;font-size:18px;'
                        })  # 找到所有class=info的div标签内容
    if len(div) == 0:
        div = soup.find_all('span', attrs={
            'style': 'font-size: large; color: rgb(0, 102, 153);'})

    for elem in div:
        text = elem.find('b')
        # link = elem.find('a')['href'] # 找到每个音频链接
        sou_gennbunn += text.text + '\n'
    pbar.update(30)
    time.sleep(0.1)
    pbar.close()
    # print(sou_gennbunn)
    return sou_gennbunn


def write_file(sou_gennbunn: str, tg_title: str):
    intab = '?/|\.><:*'
    for s in intab:
        if s in tg_title:
            print('\033[1;33m警告，存在系统不支持的文件名已自动替换 \033[0m')
            tg_title = tg_title.replace(s, ' ')
    filename = '{}.txt'.format(tg_title)
    with open(filename, 'w+', encoding='UTF-8') as fo:
        fo.write(sou_gennbunn)


def main():
    bangumi_name = input('搜索番剧名称（日文原名）\n')
    result_list = search(bangumi_name)
    df = pd.DataFrame(result_list)
    df_reset = df.set_index('id')
    print(df_reset)
    i = input('请选择id \n')
    serifu_url = pick(i, result_list)
    i = int(i)-1
    tg_title = str(result_list[i]['title'])
    print(serifu_url)
    print(tg_title)
    print('正在爬取台词')
    sou_gennbunn = get_serifu(serifu_url)
    print('正在写入台词到txt文件')
    write_file(sou_gennbunn, tg_title)
    print('写入完成，请查看文件')
    os.system("pause")

    
if __name__ == "__main__":
    main()
