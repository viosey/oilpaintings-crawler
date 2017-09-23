#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import os
import sys
import time
from bs4 import BeautifulSoup

# 创建新目录
def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print path + ' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path + ' 目录已存在'
        return False


# 保存图片
def saveImg(imgurl, imgpath):
    headers = { 
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }

    for i in range(10):
        try:
            # 保存图片
            imgRequest = urllib2.Request(imgurl, headers=headers)
            imgResponse = urllib2.urlopen(imgRequest, timeout=2)
            imgData = imgResponse.read()
            wfile = open(imgpath, 'wb')
            wfile.write(imgData)
            wfile.close()
            break
        except KeyboardInterrupt:
            print '\n=== keyboard interrupt ==='
            sys.exit(0)
        except:
            continue


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
    index = 0

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

        # 序号补为两位数
        if index < 9:
            strindex = '0' + str(index + 1)
        else:
            strindex = str(index + 1)

        # 更新命名
        lists[index] = strindex + ' ' + lists[index] + ' - ' + artist

        # 增加序号
        index += 1


# 获取图片地址
def getImgUrl(imgurls, lists, page_path):
    # 序号
    index = 0

    # 遍历
    for item in imgurls:
        print '### 图片：' + str(index+1)

        # 获取图片地址
        imgurl = 'https://www.oilpaintings.com/' + item.get('src')

        # 图片保存地址
        img_path = page_path + '/' + lists[index] + '.jpg'

        # 保存图片
        saveImg(imgurl, img_path)

        # 延迟
        time.sleep(0.01)

        #print imgurl

        # 增加序号
        index += 1


def start(start, end, subject):
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

    # 创建主题目录
    sub_path = 'OilPaintings' + '/' + subject
    mkdir(sub_path)

    pageValid = True

    for page in range(start, end+1):

        if pageValid:
            # 页面地址
            url = 'https://www.oilpaintings.com/subjects/'+ subject + '/' + str(page)

            try:
                # print url
                response = opener.open(url)
                html = response.read()

                # 使用 beautifulsoup 对 HTML 解析
                soup = BeautifulSoup(html, 'lxml')

                # 根据指定元素生成的列表
                titles = soup.select('span#hover-item > a')
                artists = soup.select('td.td_listing div.galArtistProduct > a')
                imgurls = soup.select('a.gal-zoom-img-href img')

                # 从页面中获取当前页码
                currentpage = soup.select('td.paging b')[0].get_text()

                # 如果页面存在
                if int(currentpage) == page:
                    print '\n## 页面：' + str(page)
                    # 命名列表
                    lists = []

                    # 序号补为两位数
                    if page < 10:
                        strpage = '0' + str(page)
                    else:
                        strpage = str(page)

                    # 页面目录
                    page_path = sub_path + '/' + strpage
                    mkdir(page_path)

                    # 获取标题、作者、图片地址
                    getTitles(titles, lists)
                    getArtists(artists, lists)
                    getImgUrl(imgurls, lists, page_path)
                else:
                    print '#### ' + subject + ' 分类扒取完成'
                    pageValid = False

            except urllib2.HTTPError, e_val:
                print e_val.code
            except urllib2.URLError, e_val:
                print e_val.args

def bigstart(subject):
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
    url = 'https://www.oilpaintings.com/subjects/'+ subject + '/'

    response = opener.open(url)
    html = response.read()

    # 使用 beautifulsoup 对 HTML 解析
    soup = BeautifulSoup(html, 'lxml')

    # 子分类列表
    subcats = soup.select('td.category_image > a')

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

        print '\n# 子分类：' + catname
        start(1, 9, subject + '/' + catname)


# 启动爬虫
start(1, 50, 'ships-boats')
# bigstart('still-life')
