#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import requests
from bs4 import BeautifulSoup


class Test:

    def __init__(self):
        self.site_url = 'https://mmzztt.com/beauty/page/%s/'
        self.root_folder = os.getcwd()+'/pics/'
        self.css_selector="body > section > div > div > main > div > div:nth-child(1)"
        self.user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36"
        self.referer = "https://mmzztt.com/beauty/"
        # 指明解码方式
        #reload(sys)
        #sys.setdefaultencoding('utf-8')

        # 创建根目录
        print('创建根目录 {0}'.format(self.createFolder(self.root_folder)))

    # 获取beautifulSoup实例
    @staticmethod
    def get_beautiful_soup(url,header):
        r = requests.get(url,headers=header)
        if r.status_code == 200:
            html = r.content
            # print(html)
            soup = BeautifulSoup(html, 'html.parser')
            # print(soup.prettify)
            return soup

    # 创建文件夹
    def createFolder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            # print('创建文件目录成功 ' + folder_path)
        else:
            # print('文件目录已存在 ' + folder_path)
            pass
        return folder_path

    # 获取二级目录名称
    def get_two_level_directory(self):
        contents = []
        for i in range(100):
            url = self.site_url % (i+1)
            header = {"user-agent":self.user_agent,
                      "referer":self.referer}
            soup = self.get_beautiful_soup(url,header)
            items = soup.find_all('div', class_='uk-article')
            for item in items:
                category = item.find_all('div',class_='u-category')[0].string
                title_obj = item.find_all('h2',class_='uk-margin-remove')[0]
                img_obj = item.find_all('div',class_='uk-inline')
                pics = []
                for img_e in img_obj:
                    pic_href = img_e.find('img').get('data-src')
                    if pic_href is not None:
                        pic_href = pic_href.replace('thumb300','mw2000')
                        pics.append(pic_href)
                    else:
                        print("None")
                title = title_obj.string
                href = title_obj.find('a').get('href')
                contents.append((category,title,href,pics))

        return contents

    # 保存图片到本地
    @staticmethod
    def download_pic(pic_url, pic_path):
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer': "https://mmzztt.com/beauty/"
        }
        try:
            # 设置绝对路径，文件夹路径 + 图片路径
            if os.path.isfile(pic_path):
                print('该图片已存在  ' + pic_path)
                return
            print('文件路径：' + pic_path + ' 图片地址：' + pic_url)
            try:
                img = requests.get(pic_url, headers=headers, timeout=10)
                with open(pic_path, 'ab') as f:
                    f.write(img.content)
                    print(pic_path)
            except Exception as e:
                print(e)
            print("保存图片完成")
        except Exception as e:
            print(e)
            print("保存图片失败: " + pic_url)

    def get_three_level_directory(self,ee):
        category, title, href, pics = ee
        category = category.replace("#","",3)
        category_root = self.root_folder+"/"+category
        if not os.path.exists(category_root):
            os.makedirs(category_root)
        idx1 = href.rindex('/')
        pic_root = category_root+"/"+href[idx1:]
        if not os.path.exists(pic_root):
            os.makedirs(pic_root)

        pic_info = pic_root+".txt"
        with open(pic_info, 'ab') as f:
            f.write(title.encode('utf-8'))

        for pic_url in pics:
            #9d52c073gy1gymkmyo29pj20oo1hcqk7.jpg
            idx2 = pic_url.rindex('/')
            pic_path = pic_root+pic_url[idx2:]
            self.download_pic(pic_url,pic_path)






mm = Test()

# 获取二级目录
contents = mm.get_two_level_directory()
count = 0
for ee in contents:
    count +=1
    print("count %d size %d" % (count,len(contents)))
    category, title, href,pics = ee
    mm.get_three_level_directory(ee)

print('爬取完成')
