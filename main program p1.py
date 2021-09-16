from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
import re
import xlwt
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import jieba

# ------------problem 1--------------
number_pre_web = "http://news.bnu.edu.cn"
web_pre_web = "http://news.bnu.edu.cn/zx/ttgz/"

write_book = xlwt.Workbook()
main_sheet = write_book.add_sheet('1')
main_sheet.write(0, 0, '日期')
main_sheet.write(0, 1, '标题')
main_sheet.write(0, 2, '链接')
main_sheet.write(0, 3, '浏览次数')


def get_number(website):
    # 生成浏览量的网页只有文字元素 直接用bs解析之后取text 之后用正则表达式提取数字
    new_html = urlopen(website)
    new_bs0bj = str(BeautifulSoup(new_html, features='html.parser').get_text())
    number = int(re.findall(r"\d+\.?\d*", new_bs0bj)[0])
    return number


def get_title_time(website):
    html = urlopen(website)
    bs0bj = BeautifulSoup(html, features='html.parser')
    titles = bs0bj.find('div', {"class": "articleTitle"}).get_text().replace('\n', '')
    times = bs0bj.find('span', {"class": "time"}).get_text()
    return titles, times


def get_view_number(website, result_dict):
    number_list = []
    website_list = []
    html = urlopen(website)
    bs0bj = BeautifulSoup(html, features='html.parser')
    all_number = bs0bj.find_all('span', {"class": "view"})
    all_web = bs0bj.find_all("p", {"class": "inner"})
    for numbers in all_number:
        done_web = numbers.find('script').attrs['src']
        complete_web = number_pre_web + done_web
        number_list.append(get_number(complete_web))
    for webs in all_web:
        if '.htm' in webs.find('a').attrs['href']:
            website_list.append(web_pre_web + webs.find('a').attrs['href'])
    result_dict.update(dict(zip(website_list, number_list)))


done_dict = {}
websites = "http://news.bnu.edu.cn/zx/ttgz/index.htm"
get_view_number(websites, done_dict)
for page in range(1, 61):
    websites = "http://news.bnu.edu.cn/zx/ttgz/index" + str(page) + ".htm"
    get_view_number(websites, done_dict)
    print("page", page, 'done!')

sort_list = sorted(done_dict.items(), key=lambda x: x[1], reverse=True)
for n in range(0, len(sort_list)):
    link = sort_list[n][0]
    # print(link)
    title, time = get_title_time(link)
    view_number = sort_list[n][1]
    main_sheet.write(n + 1, 0, time)
    main_sheet.write(n + 1, 1, title)
    main_sheet.write(n + 1, 2, link)
    main_sheet.write(n + 1, 3, view_number)


write_book.save('1.1.xls')

# ------------problem 2--------------
# 排序的工作在上面已经做过


def write_image_text(website):
    html = urlopen(website)
    bs0bj = BeautifulSoup(html, features='html.parser')
    all_text = bs0bj.find('div', {"class": "article"}).get_text()
    title = bs0bj.find("div", {"class": "articleTitle"}).get_text().replace('\n', '')
    global top_title
    top_title = title
    all_image = bs0bj.find('div', {'class', 'articleList03'}).find_all('img')
    image_number = 1
    for image in all_image:
            image_link = "http://news.bnu.edu.cn"+image['src'][5:]
            try:
                urllib.request.urlretrieve(image_link, title+str(image_number)+'.png')
                print('image', image_number, 'download!')
            except urllib.error.URLError:
                pass
            image_number += 1
    with open(str(title)+'.txt', 'a', encoding='utf-8') as f:
        f.write(all_text)
        f.write("\n")
    print(title, 'done!')


top_passage_link = sort_list[0][0]
write_image_text(top_passage_link)

# ----------------problem 3---------------


def create_cloud(text_name):
    d = path.dirname(__file__)
    text = open(path.join(d, text_name), encoding='utf-8').read()
    text = ' '.join(jieba.cut(text))
    coloring = np.array(Image.open(path.join(d, 'timg.png')))
    image_colors = ImageColorGenerator(coloring)

    wc = WordCloud(font_path='C:\Windows\Fonts\simsun.ttc',
                   background_color='white', max_words=2000,
                   mask=coloring, max_font_size=40,
                   random_state=42, color_func=image_colors).generate(text)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    plt.imshow(coloring, interpolation='bilinear')
    plt.axis("off")
    wc.to_file('cloud.png')


high_title = top_title + '.txt'
create_cloud(high_title)
