import tkinter as tk
import tkinter.messagebox
import pandas as pd
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
import re
import xlwt
import matplotlib
from os import path
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import jieba
from PIL import Image, ImageTk


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("welcome to Yuxin Du's scrap system")
        width, height = self.master.maxsize()
        self.master.geometry("{}x{}".format(width, height))
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.create_show_pic_fm()
        self.create_show_title_fm()
        self.create_show_passage_fm()

    def create_show_pic_fm(self):
        self.show_pic_fm = tk.Frame(self)
        self.main_show_image_fm = tk.Frame(self.show_pic_fm)
        self.show_next_buttom_fm = tk.Frame(self.show_pic_fm)
        self.load_pic = Image.open('fm3.jpg')
        # print(load)
        render = ImageTk.PhotoImage(self.load_pic)
        self.img1 = tk.Label(self.main_show_image_fm, image=render)
        self.img1.image = render
        self.img1.pack()
        self.show_next_picture = tk.Button(self.show_next_buttom_fm, text="下一张图片",
                                           command=self.next_image)
        self.show_last_picture = tk.Button(self.show_next_buttom_fm, text="上一张图片",
                                           command=self.last_image)
        self.show_next_picture.pack(side=tk.RIGHT, expand=tk.NO, anchor=tk.W)
        self.show_last_picture.pack(side=tk.LEFT, expand=tk.NO, anchor=tk.E)
        self.main_show_image_fm.pack()
        self.show_next_buttom_fm.pack(fill=tk.X)
        self.show_pic_fm.pack(side=tk.BOTTOM)

    def create_show_title_fm(self):
        self.show_title_fm = tk.Frame(self)
        self.main_show_area = tk.Frame(self.show_title_fm)
        self.rbotton_up = tk.Frame(self.show_title_fm)
        self.rbotton_down = tk.Frame(self.show_title_fm)
        load = Image.open('fm1.jpg')
        # print(load)
        render = ImageTk.PhotoImage(load)
        self.img2 = tk.Label(self.main_show_area, image=render)
        self.img2.image = render
        self.img2.pack()
        self.get_local_name_button = tk.Button(self.rbotton_up, text="本地获取报道列表",
                                               command=self.get_local_name_list)
        self.get_local_name_button.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X, anchor=tk.NW)

        self.sort_view_button = tk.Button(self.rbotton_up, text="依据浏览次数排序",
                                          command=self.sort_view)
        self.sort_view_button.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X, anchor=tk.NE)

        self.get_online_name_list_button = tk.Button(self.rbotton_down, text="网上获取报道列表",
                                                     command=self.get_online_name_list)
        self.get_online_name_list_button.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X, anchor=tk.SW)

        self.get_passage_button = tk.Button(self.rbotton_down, text="本地查看报道内容",
                                            command=self.get_passage)
        self.get_passage_button.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X, anchor=tk.NE)
        self.main_show_area.pack()
        self.rbotton_up.pack(fill=tk.X)
        self.rbotton_down.pack(fill=tk.X)
        self.show_title_fm.pack(side=tk.LEFT, expand='no')

    def create_show_passage_fm(self):
        self.show_passage_fm = tk.Frame(self)
        self.main_show_passage_area = tk.Frame(self.show_passage_fm)
        self.lbotton_up = tk.Frame(self.show_passage_fm)
        self.lbotton_down = tk.Frame(self.show_passage_fm)
        load = Image.open('fm2.jpg')
        # print(load)
        render = ImageTk.PhotoImage(load)
        self.img3 = tk.Label(self.main_show_passage_area, image=render)
        self.img3.image = render
        self.img3.pack()
        self.b5 = tk.Button(self.lbotton_up, text="每年的报道量统计",
                            command=self.show_stat_by_year)
        self.b5.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X, anchor=tk.NW)

        self.b6 = tk.Button(self.lbotton_up, text="每年每月报道统计",
                            command=self.show_stat_by_month)
        self.b6.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X, anchor=tk.NE)

        self.b7 = tk.Button(self.lbotton_down, text="查看报道词云",
                            command=self.show_word_cloud)
        self.b7.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X, anchor=tk.SW)

        self.b8 = tk.Button(self.lbotton_down, text="查看报道图片",
                            command=self.show_each_image)
        self.b8.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X, anchor=tk.NE)
        self.main_show_passage_area.pack()
        self.lbotton_up.pack(fill=tk.X)
        self.lbotton_down.pack(fill=tk.X)
        self.show_passage_fm.pack(side=tk.RIGHT, expand='no')

    def say_hi(self):
        tk.messagebox.showinfo("message", "hello")

    def creat_list_box(self):
        self.var2 = tk.StringVar()
        y_bar = tk.Scrollbar(self.main_show_area)
        y_bar.pack(side=tk.RIGHT, fill=tk.Y)
        x_bar = tk.Scrollbar(self.main_show_area, orient=tk.HORIZONTAL)
        x_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.name_listbox = tk.Listbox(self.main_show_area, selectmode=tk.SINGLE, listvariable=self.var2, width=75,
                                       height=15, yscrollcommand=y_bar.set, xscrollcommand=x_bar.set)
        x_bar.config(command=self.name_listbox.xview)
        print(self.name_listbox.curselection())

    def get_local_name_list(self):
        try:
            self.data = pd.read_excel('1.1.xls')
        except FileNotFoundError:
            tk.messagebox.showerror("警告", "未在本地发现链接，需要在线爬取")
        else:
            if self.img2.winfo_exists():
                self.img2.destroy()
                self.creat_list_box()
            self.name_listbox.delete(0, tk.END)
            list_items = list(self.data.values)
            for item in list_items:
                self.name_listbox.insert('end', str(item).replace("\\n", " ")
                                         .replace("'", '').replace("[", '')
                                         .replace("]", '').replace("\\u200b", ''))
            self.name_listbox.pack(expand=tk.YES, fill=tk.X)

    def sort_view(self):
        try:
            self.data = self.data.sort_values(by="浏览次数", ascending=False)
        except AttributeError:
            tk.messagebox.showerror("警告", "未导入报道列表，请先本地或在线导入报道列表")
        else:
            self.name_listbox.delete(0, tk.END)
            list_items = list(self.data.values)
            for item in list_items:
                self.name_listbox.insert('end', str(item).replace("\\n", " ")
                                         .replace("'", '').replace("[", '')
                                         .replace("]", '').replace("\\u200b", ''))

    def get_excel(self):
        number_pre_web = "http://news.bnu.edu.cn"
        web_pre_web = "http://news.bnu.edu.cn/zx/ttgz/"

        write_book = xlwt.Workbook()
        main_sheet = write_book.add_sheet('1')
        main_sheet.write(0, 0, '日期')
        main_sheet.write(0, 1, '标题')
        main_sheet.write(0, 2, '链接')
        main_sheet.write(0, 3, '浏览次数')

        def get_number(website):
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
        self.page = 1
        print("page 1 done!")
        for self.page in range(1, 62):
            websites = "http://news.bnu.edu.cn/zx/ttgz/index" + str(self.page) + ".htm"
            get_view_number(websites, done_dict)
            print("page", self.page + 1, 'done!')
        sort_list = sorted(done_dict.items(), key=lambda x: x[1], reverse=False)
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

    def get_online_name_list(self):
        tk.messagebox.showinfo("温馨提示", "网上获取报道列表很慢，请耐心等待， "
                               "并且在程序运行时不要乱点（请关闭此窗口，否则程序不会运行）")
        if self.img2.winfo_exists():
            self.img2.destroy()
            self.creat_list_box()
        self.get_excel()
        self.data = pd.read_excel('1.1.xls')
        self.name_listbox.delete(0, tk.END)
        list_items = list(self.data.values)
        for item in list_items:
            self.name_listbox.insert('end', str(item).replace("\\n", " ")
                                     .replace("'", '').replace("[", '')
                                     .replace("]", '').replace("\\u200b", ''))
        self.name_listbox.pack(expand=tk.YES, fill=tk.X)

    def write_image_text(self):
        html = urlopen(self.web)
        bs0bj = BeautifulSoup(html, features='html.parser')
        self.all_text = bs0bj.find('div', {"class": "article"}).get_text()

        self.title = bs0bj.find("div", {"class": "articleTitle"}).get_text().replace('\n', '')
        global top_title
        top_title = self.title
        all_image = bs0bj.find('div', {'class', 'articleList03'}).find_all('img')
        self.image_number = 1
        for image in all_image:
            image_link = "http://news.bnu.edu.cn" + image['src'][5:]
            try:
                urllib.request.urlretrieve(image_link, "downloadImage\\" + self.title
                                           + str(self.image_number) + '.png')
                print('image', self.image_number, 'download!')
            except urllib.error.URLError or OSError:
                pass
            self.image_number += 1
        with open("downloadText\\" + str(self.title) + '.txt', 'a', encoding='utf-8') as f:
            f.write(self.all_text)
            f.write("\n")
        print(self.title, 'done!')

    def get_passage(self):
        try:
            h = int(self.name_listbox.curselection()[0])
            web = str(self.data[h:h + 1]["链接"])[5:]
            self.web = web[0: web.rfind('Na') - 1]
            self.write_image_text()
            if self.img3.winfo_exists():
                self.img3.destroy()
                y2_bar = tk.Scrollbar(self.main_show_passage_area)
                y2_bar.pack(side=tk.RIGHT, fill=tk.Y)
                self.show_passage_text = tk.Text(self.main_show_passage_area, width=75,
                                                 height=22, yscrollcommand=y2_bar.set)
            self.show_passage_text.delete('1.0', tk.END)
            self.show_passage_text.insert(tk.END, self.all_text)
            self.show_passage_text.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
        except AttributeError:
            tk.messagebox.showerror("警告", "未导入报道列表，请先本地或在线导入报道列表")
        except IndexError:
            tk.messagebox.showerror("警告", "请先选择想要查看的报道")

    def show_stat_by_year(self):
        try:
            def get_month(year_month):
                return int(year_month[5:7])
            matplotlib.rcParams['font.family'] = 'SimHei'
            self.data['年份'] = self.data.apply(lambda x: "2018" if "2018" in x['日期'] else "2019", axis=1)
            self.data['月份'] = self.data.apply(lambda x: get_month(x['日期']), axis=1)
            # print(df)
            year_df = self.data['年份'].value_counts().sort_values()
            year_df.plot(kind='bar', color=['c', 'b', 'r', 'm', 'y'])
            plt.xticks(rotation=0)
            plt.title('每年报道总量统计', fontproperties='SimHei', size=15)
            plt.xlabel('年份', fontproperties='SimHei', size=10)
            plt.ylabel('报道量', fontproperties='SimHei', size=10)
            plt.rcParams['figure.figsize'] = (4.0, 2.0)
            plt.rcParams['figure.dpi'] = 100
            plt.rcParams['savefig.dpi'] = 100
            plt.savefig('year_plot.png', format='png', dpi=80)
            for self.widget in self.main_show_image_fm.winfo_children():
                self.widget.destroy()
        except AttributeError:
            tk.messagebox.showerror("警告", "未导入报道列表，请先本地或在线导入报道列表")
        else:
            self.load_pic = Image.open('year_plot.png')
            render = ImageTk.PhotoImage(self.load_pic)
            self.img1 = tk.Label(self.main_show_image_fm, image=render)
            self.img1.image = render
            self.img1.pack()

    def show_stat_by_month(self):
        try:
            def get_year_plot(year):
                def get_month(year_month):
                    return int(year_month[5:7])
                matplotlib.rcParams['font.family'] = 'SimHei'
                self.data['年份'] = self.data.apply(lambda x: "2018" if "2018" in x['日期'] else "2019", axis=1)
                self.data['月份'] = self.data.apply(lambda x: get_month(x['日期']), axis=1)
                month_df = self.data.loc[(self.data['年份'] == year)]["月份"].value_counts().sort_index()
                month_df.plot(kind='bar', color=['r', 'g', 'b', 'm', 'y'])
                plt.xticks(rotation=0)
                plt.title(year + "年每个月的报道量 ", fontproperties='SimHei', size=15)
                plt.xlabel('月份', fontproperties='SimHei', size=10)
                plt.ylabel('报道量', fontproperties='SimHei', size=10)
                plt.savefig(year + '.png', format='png', dpi=65)
            get_year_plot("2018")
            get_year_plot("2019")
            for self.widget in self.main_show_image_fm.winfo_children():
                self.widget.destroy()
        except AttributeError:
            tk.messagebox.showerror("警告", "未导入报道列表，请先本地或在线导入报道列表")
        else:
            self.load_pic = Image.open('2018.png')
            render = ImageTk.PhotoImage(self.load_pic)
            self.img2018 = tk.Label(self.main_show_image_fm, image=render)
            self.img2018.image = render
            self.img2018.pack(side=tk.LEFT)
            self.load_pic = Image.open('2019.png')
            render = ImageTk.PhotoImage(self.load_pic)
            self.img2019 = tk.Label(self.main_show_image_fm, image=render)
            self.img2019.image = render
            self.img2019.pack(side=tk.RIGHT)

    def show_word_cloud(self):
        try:
            d = path.dirname(__file__)
            self.cloud_text = ' '.join(jieba.cut(self.all_text))
            coloring = np.array(Image.open(path.join(d, 'timg.png')))
            image_colors = ImageColorGenerator(coloring)
            wc = WordCloud(font_path='C:\Windows\Fonts\simsun.ttc',
                           background_color='white', max_words=2000,
                           mask=coloring, max_font_size=40,
                           random_state=42, color_func=image_colors).generate(self.cloud_text)
            wc.to_file('cloud.png')
            for self.widget in self.main_show_image_fm.winfo_children():
                self.widget.destroy()
        except AttributeError:
            tk.messagebox.showerror("警告", "未选择文章，请先本地或在线导入报道内容")
        else:
            self.load_pic1 = Image.open('cloud.png').resize((350, 350))
            render = ImageTk.PhotoImage(self.load_pic1)
            self.img_cloud = tk.Label(self.main_show_image_fm, image=render)
            self.img_cloud.image = render
            self.img_cloud.pack()

    def show_image(self):
        self.showing_image = Image.open("downloadImage\\" + self.title +
                                        str(self.pic_num) + '.png').resize((600, 400))
        render = ImageTk.PhotoImage(self.showing_image)
        self.img1 = tk.Label(self.main_show_image_fm, image=render)
        self.img1.image = render
        self.img1.pack()

    def warning_no_pic(self):
        self.load_pic = Image.open('fm3.jpg')
        # print(load)
        render = ImageTk.PhotoImage(self.load_pic)
        self.img1 = tk.Label(self.main_show_image_fm, image=render)
        self.img1.image = render
        self.img1.pack()
        tk.messagebox.showerror("警告", "这篇文章中没有图片")

    def show_each_image(self):
        try:
            for self.widget in self.main_show_image_fm.winfo_children():
                self.widget.destroy()
            self.pic_num = 1
            self.show_image()
        except AttributeError:
            self.load_pic = Image.open('fm3.jpg')
            # print(load)
            render = ImageTk.PhotoImage(self.load_pic)
            self.img1 = tk.Label(self.main_show_image_fm, image=render)
            self.img1.image = render
            self.img1.pack()
            tk.messagebox.showerror("警告", "未选择文章，请先本地或在线导入报道内容")
        except FileNotFoundError or OSError:
            self.warning_no_pic()

    def next_image(self):
        try:
            self.pic_num += 1
            if self.pic_num == self.image_number:
                self.pic_num -= 1
                tk.messagebox.showerror("警告", "已经是最后一张图片")
            else:
                for self.widget in self.main_show_image_fm.winfo_children():
                    self.widget.destroy()
                self.show_image()
        except AttributeError:
            tk.messagebox.showerror("警告", "未选择文章，请先本地或在线导入报道内容")
        except FileNotFoundError or OSError:
            self.warning_no_pic()

    def last_image(self):
        try:
            self.pic_num -= 1
            if self.pic_num == 0:
                tk.messagebox.showerror("警告", "已经是第一张图片")
                self.pic_num = 1
            else:
                for self.widget in self.main_show_image_fm.winfo_children():
                    self.widget.destroy()
                self.show_image()
        except AttributeError:
            tk.messagebox.showerror("警告", "未选择文章，请先本地或在线导入报道内容")
        except FileNotFoundError or OSError:
            self.warning_no_pic()


window = tk.Tk()
window.title('anc')
# window.geometry('400x200+500+500')
app = Application(master=window)
app.mainloop()
