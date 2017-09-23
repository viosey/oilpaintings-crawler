#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import os
import sys
import time
import json
import xlwt
from bs4 import BeautifulSoup

# 删除多余空格
def stripSpaces(target):
    po4s = target.find('    ')
    po3s = target.find('   ')
    po2s = target.find('  ')

    # 判断结果
    if po4s == -1:
        if po3s == -1:
            if po2s == -1:
                pass
            else:
                str1 = target[0:po2s]
                str2 = target[po2s+1:]
                target = str1 + str2
        else:
            str1 = target[0:po3s]
            str2 = target[po3s+2:]
            target = str1 + str2
    else:
        str1 = target[0:po4s]
        str2 = target[po4s+3:]
        target = str1 + str2

    return target

# 获取图片标题
def getTitles(titles, lists):
    # 遍历
    for item in titles:
        title = item.get('title')

        # 删除多余空格
        title = stripSpaces(title)

        # 开头若有空格则删除
        if title[0] == ' ':
            title = title[1:]

        # 结尾若有空格则删除
        if title[-1] == ' ':
            title = title[:-1]

        # 删除反斜杠
        # pobs = title.find('\\')
        # if pobs == -1:
        #     pass
        # else:
        #     str1 = title[0:pobs]
        #     str2 = title[pobs+1:]
        #     title = str1 + str2

        # 删除冒号
        pocolon = title.find(':')
        if pocolon == -1:
            pass
        else:
            str1 = title[0:pocolon]
            str2 = title[pocolon+1:]
            title = str1 + str2

        # 添加到命名列表
        lists.append(title)
        #print 'title:' + title


# 获取图片作者
def getArtists(artists, lists):
    # 序号
    indexoflists= 0

    # 遍历
    for item in artists:
        # 删除开头空格
        artist = item.get_text()
        artist = artist[1:]

        # 删除换行
        pob = artist.find('\n')
        if pob == -1:
            pass
        else:
            str1 = artist[0:pob]
            str2 = artist[pob+1:]
            artist = str1 + str2

        # 删除多余空格
        artist = stripSpaces(artist)

        # # 更新命名
        # lists[indexoflists] = lists[indexoflists] + ' - ' + artist
        hasnoArtist = True

        # 检查是否艺术家是否存在
        for item in lists:
            if artist == item:
                hasnoArtist = False

        if hasnoArtist:
            lists.append(artist)

        # 增加序号
        indexoflists += 1


def writetows(lists, ws, indexofsubcat):
    indexofimg = 1

    for item in lists:  
      ws.write(indexofimg, indexofsubcat, item)
      # print item
      indexofimg += 1
  

def start(start, end, subject, ws, indexofsubcat):
    # headers params
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    opener = urllib2.build_opener()
    opener.addheaders = [
        ('Accept', accept),
        ('X-Requested-With', 'XMLHttpRequest'),
        ('Cookie', 'itemperpage=72'),
        ('Content-Type', 'application/json; charset=UTF-8'),
        ('User-Agent', user_agent)
    ]

    # 创建主题目录
    # sub_path = 'OilPaintingsOrg' + '/' + subject
    # mkdir(sub_path)

    pageValid = True

    # 命名列表
    lists = []

    for page in range(start, end+1):

        if pageValid:
            # 页面地址
            url = 'https://www.oilpaintings.com/styles/'+ subject + '/' + str(page)

            for retryi in range(100):
                try:
                    # print url
                    response = opener.open(url, timeout=2)
                    html = response.read()

                    # 使用 beautifulsoup 对 HTML 解析
                    soup = BeautifulSoup(html, 'lxml')

                    # 根据指定元素生成的列表
                    # titles = soup.select('span#hover-item > a > img')
                    artists = soup.select('td.Artist_name > a')

                    # 从页面中获取当前页码
                    currentpage = soup.select('td.paging b')[0].get_text()

                    # 如果页面存在
                    if int(currentpage) == page:
                        print '## 页面:' + str(page) + ' (' + str(indexofsubcat)

                        # 获取标题、作者、图片地址
                        # getTitles(titles, lists)
                        getArtists(artists, lists)
                    else:
                        print '#### ' + str(indexofsubcat) + ' - ' + subject + ' 分类扒取完成'
                        pageValid = False

                    # 延迟
                    time.sleep(0.2)

                    break
                except KeyboardInterrupt:
                    print '\n=== keyboard interrupt ==='
                    sys.exit(0)
                except:
                    continue

    writetows(lists, ws, indexofsubcat)
    wb.save('art-styles.xls')


def bigstart():
    # headers params
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'

    opener = urllib2.build_opener()
    opener.addheaders = [
        ('Accept', accept),
        ('X-Requested-With', 'XMLHttpRequest'),
        ('Cookie', 'itemperpage=72'),
        ('Content-Type', 'application/json; charset=UTF-8'),
        ('User-Agent', user_agent)
    ]

    # 页面地址
    url = 'https://www.oilpaintings.com/styles'

    response = opener.open(url)
    html = response.read()

    # 使用 beautifulsoup 对 HTML 解析
    soup = BeautifulSoup(html, 'lxml')

    # 子分类列表
    subcats = soup.select('td.productListing > a')
    indexofsubcat = 0

    wb = xlwt.Workbook()
    ws = wb.add_sheet('artists')

    # 逆转子分类列表
    # subcats = reversed(subcats)

    #自动获取的分类
    for subcat in subcats:
        catname = subcat.get('href')

        slashp = catname.rfind('/')
        qmp = catname.rfind('?')

        catname = catname[slashp+1:qmp]

        # 连接 catname s 字符串
        # catnames = catnamestr + "'" + catname + "', "

        print '\n# 子分类：' + str(indexofsubcat) + ' ' + catname
        ws.write(0, indexofsubcat, catname)
        start(1, 1000, catname, ws, indexofsubcat)

        indexofsubcat += 1

    
    wb.save('colors1.xls')

wb = xlwt.Workbook()
ws = wb.add_sheet('artists')
# 启动爬虫
# start(1, 500, 'impressionism', ws, 0)
bigstart()
