# -*- coding=utf-8 -*-
import random
import time
import requests
import os
import re
import urllib
import json
import string
import threading
from lxml import etree
from urllib import request, parse


def get_UserAgent():
    '''
        返回一个随机的请求头 headers
    '''
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    UserAgent = random.choice(USER_AGENTS)
    headers = {'User-Agent': UserAgent}
    return headers


def filterType(filename):
    '''
    返回文件类型
    '''
    filter_type = ['.zip', '.pdf', '.doc', '.docx',
                   '.xls', '.xlsx', '.png', '.img', '.rar', '.txt']
    IsExist = ''
    if filename != '':
        for item in filter_type:
            if filename.find(item) != -1:
                IsExist = item
                break
    return IsExist


def save_file(downloadUrl, saveFilePath):
    '''
    文件下载1
    '''
    print('文件开始下载并保存...')
    try:
        header_dict = get_UserAgent()
        with requests.get(downloadUrl, headers=header_dict, timeout=6, stream=True) as web:
            print(web.status_code)
            # 为保险起见使用二进制写文件模式，防止编码错误
            with open(saveFilePath, 'wb') as outfile:
                for chunk in web.iter_content(chunk_size=1024):
                    outfile.write(chunk)
        print('文件下载完成...')
    except Exception as ex:
        print(ex)


def save_file_retrieve(downloadUrl, saveFileName):
    '''''
    文件下载2
    '''
    local = os.path.join('D://downLoad//', saveFileName)
    request.urlretrieve(downloadUrl, local, Schedule)


def Schedule(a, b, c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('%.2f%%' % per)


def get_file(downloadUrl, saveFilePath):
    '''
    文件下载3
    '''
    try:
        u = request.urlopen(downloadUrl)
        print('文件开始下载并保存...')
        block_sz = 8192
        with open(saveFilePath, 'wb') as f:
            while True:
                buffer = u.read(block_sz)
                if buffer:
                    f.write(buffer)
                else:
                    break
        print('文件下载完成...')
    except urllib.error.HTTPError:
        # 碰到了匹配但不存在的文件时，提示并返回
        print(downloadUrl, "url file not found")
    except IOError:
        print(IOError.message)


def getAll_contentForJs(html, re_str):
    '''
          获取js里面yunData数据,返回yunData字符串
     html: html代码
     re_str: 正则表达式
    '''
    #res_str = r'yunData.setData\({(.*?)}\)'
    my_js = re.findall(re_str, html, re.S | re.M)
    jsData = my_js
    return jsData


def getAll_contentFosXpath(html, myxpath):
    '''
          获取页面上指定内容
     html: html代码
     myxpath: xpath语法
    '''
    myHtml = etree.HTML(html)
    mydata = myHtml.xpath(myxpath)
    return mydata


def get_postUrl(Jsparams):
    '''
            拼接请求百度网盘真实下载地址post的url地址
    '''
    urlstr = 'https://pan.baidu.com/api/sharedownload?'
    params = json.loads(Jsparams)
    urlstr += 'sign=' + str(params.get('sign')) + ''
    urlstr += '&timestamp=' + str(params.get('timestamp')) + ''
    urlstr += '&bdstoken=' + str(params.get('bdstoken')) + ''
    urlstr += '&channel=chunlei'
    urlstr += '&clienttype=0'
    urlstr += '&web=1'
    urlstr += '&app_id=250528'
    return urlstr


def get_postData(Jsparams):
    '''
          拼接请求百度网盘真实下载地址post的请求参数
    '''
    postdata = {}
    params = json.loads(Jsparams)
    postdata["encrypt"] = 0
    postdata["product"] = "share"
    postdata["uk"] = str(params.get("uk"))
    postdata["primaryid"] = str(params.get("shareid"))
    postdata["fid_list"] = "[" + \
        str(params['file_list']['list'][0].get('fs_id')) + "]"
    return postdata


def get_downLoad(Jsparams):
    '''
          发送post请求获取真实下载地址
    '''
    print('发送post请求获取真实下载路径...')
    try:
        header_dict = get_UserAgent()
        params = parse.urlencode(get_postData(
            Jsparams)).encode(encoding='UTF8')
        req = request.Request(url=get_postUrl(Jsparams),
                              data=params, headers=header_dict, method="POST")
        resp = request.urlopen(req)
        resp = resp.read().decode(encoding='utf-8')
        return resp
    except Exception as ex:
        print(ex)


def get_html(urlLink, headers):
    '''
    获取页面代码html,  同IP多次请求会出现超时现象。
    '''
    try:
        response = requests.get(
            url=urlLink, headers=headers, timeout=60)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
    except urllib.request.URLError as e:
        print('URLError! The bad Msg is %s' % e)
        return None
    except urllib.request.HTTPError as e:
        print('HTTPError! The bad Msg is %s' % e)
        return None
    except Exception as e:
        print('Unknown Errors! The bad Msg is %s ' % e)
        return None


def get_redirects(urlLink, headers):
    try:
        response = requests.get(
            url=urlLink, headers=headers, timeout=60, allow_redirects=False)
        return response.headers['Location']
    except urllib.request.URLError as e:
        print('URLError! The bad Msg is %s' % e)
        return None
    except urllib.request.HTTPError as e:
        print('HTTPError! The bad Msg is %s' % e)
        return None
    except Exception as e:
        print('Unknown Errors! The bad Msg is %s ' % e)
        return None


def baiDuShare(bdUrl):
    try:
        print('解析盘搜搜详情页')
        header_dict = get_UserAgent()
        shareHtml = get_html(bdUrl, header_dict)
        if shareHtml != None:
            '''
            解析网站数据获取百度网盘共享文件URL
            '''
            # 共享文件名称
            share_file = getAll_contentFosXpath(
                shareHtml, '//*[@id="con"]/div/div[1]/h1')
            fileName = share_file[0].text
            # 共享文件大小
            share_size = getAll_contentForJs(
                shareHtml, '<dd>文件大小：(.*?)MB</dd>')
            # 百度网盘共享地址
            share_link = getAll_contentForJs(
                shareHtml, 'a=go&url=(.*?)&t=')
            share_url = 'http://to.pansoso.com/?a=to&url=' + \
                share_link[0]
            panRedirects = get_redirects(share_url, header_dict)
            if panRedirects != None:
                # 获取文件对应类型
                print(panRedirects)
                print(fileName)
                FirtHtml = get_html(panRedirects, header_dict)
                share_type = filterType(fileName)
                MyJS = getAll_contentForJs(
                    FirtHtml, r'yunData.setData\({(.*?)}\)')
                StrMyJS = '{' + MyJS[0] + '}'
                DownLink = json.loads(get_downLoad(StrMyJS))
                print(DownLink['list'][0].get('dlink'))
                save_file(DownLink['list'][0].get('dlink'),
                          'D://downLoad//' + str(fileName).replace(share_type, '') + share_type)  # 有些文件后缀不在标题的最后，所以将它替换为空再在最后加上文件后缀
            else:
                print('百度共享盘解析失败')
        else:
            print('盘搜搜详情页失败')
    except Exception as e:
        print('Unknown Errors! The bad Msg is %s ' % e)
        return None


if __name__ == '__main__':
    headers = get_UserAgent()  # 定制请求头
    targeturl = 'http://www.pansoso.com'
    headers["Host"] = "www.pansoso.com"
    headers["Accept-Language"] = "zh-CN,zh;q=0.9"
    searchStr = input('请输入关键字：')
    searchUrl = 'http://www.pansoso.com/zh/%s' % searchStr
    searchUrl = request.quote(searchUrl, safe=string.printable)
    print('开始搜索【%s】网盘共享: %s' % (searchStr, searchUrl))
    try:
        time.sleep(random.random() * 10)
        panSosoHtml = get_html(searchUrl, headers)
        if panSosoHtml != None:
            #从盘搜搜网站获取关键字相关连接
            panSosoLink = getAll_contentFosXpath(
                panSosoHtml, '//div[@id="content"]/div[@class="pss"]/h2/a')
            baiduthreads = []
            for titleItem in panSosoLink:
                # 筛选出文件类型以及关键字匹配的 共享文件
                if filterType(titleItem.text) != '' and str(titleItem.text).find(searchStr) != -1:
                    print(targeturl + titleItem.attrib['href'])
                    Urlparam = targeturl + titleItem.attrib['href']
                    t = threading.Thread(
                        target=baiDuShare, args=(Urlparam,))
                    baiduthreads.append(t)
            for s in baiduthreads:  # 开启多线程爬取
                s.start()
                time.sleep(random.random() * 10)
            for e in baiduthreads:  # 等待所有线程结束
                e.join()
        else:
            print('请求失败')
    except Exception as e:
        print('Unknown Errors! The bad Msg is %s ' % e)
