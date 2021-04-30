# -*- coding =utf-8 -*-
# @Time : 2021/4/30 20:41
# @Author : 胡伊斐
# @File : 可视化.py.py
# @Software : PyCharm
# View more python learning tutorial on my Youtube and Youku channel!!!

# Youtube video tutorial: https://www.youtube.com/channel/UCdyjiB5H8Pu7aDTNVXTTpcg
# Youku video tutorial: http://i.youku.com/pythontutorial
import csv
import tkinter as tk
from tkinter import messagebox  # import this to fix messagebox error
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.alert import Alert
import os

#判断是否为浮点数
def IsFloatNum(str):
    s = str.split('.')
    if len(s) > 2:
        return False
    else:
        for si in s:
            if not si.isdigit():
                return False
        return True

#创建主窗口
window = tk.Tk()
window.title('中南林业科技大学GPA计算器')
window.geometry('450x300')

# 欢迎界面
canvas = tk.Canvas(window, height=200, width=500)
image_file = tk.PhotoImage(file='1.png')
image = canvas.create_image(0,0, anchor='nw', image=image_file)
canvas.pack(side='top')

# 用户信息
tk.Label(window, text='学号: ').place(x=50, y=150)
tk.Label(window, text='密码: ').place(x=50, y=190)

#主窗口界面的控件
var_usr_name = tk.StringVar()
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=150)
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=190)

#登陆函数
def usr_login():

    # 读取学号密码信息
    username = var_usr_name.get()
    password = var_usr_pwd.get()
    print("正在加载，马上就好~")

    # 后台运行Chrome
    try:
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-logging'])  # 不打印消息
        mobileEmulation = {'deviceName': 'Galaxy S5'}
        option.add_experimental_option('mobileEmulation', mobileEmulation)
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('headless')  # 后台运行
        url_vpn = 'https://vpn.csuft.edu.cn/por/login_psw.csp?rnd=0.4175854108433872#https%3A%2F%2Fvpn.csuft.edu.cn%2F'
        driver = webdriver.Chrome(chrome_options=option)
        driver.get(url_vpn)
        # 判断是否重复登陆vpn
        try:
            error = driver.find_element_by_xpath("/html/body/div/div/div/p").text
            print(error[0:9] + ',请重新启动并选择处于校园网环境使用本软件')
            sleep(10)
        except:
            # 将窗口最大化
            driver.maximize_window()
            print("登陆vpn中，请等待")
    except Exception as result:
        tk.messagebox.showerror('Error', result)
        print(result)

    # 登录vpn

    user_login = driver.find_element_by_id('user')
    user_login.send_keys(username)
    driver.find_element_by_id("pwd").send_keys(password)
    driver.find_element_by_xpath(
        '//*[@id="login_form"]/div/table[2]/tbody/tr/td/table/tbody/tr/td[1]/button').click()
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="service_item_2"]/div/a'))
        )
        text = driver.page_source
        print("vpn登陆成功")
    except Exception as result:
        tk.messagebox.showerror('Error', result)
        is_sign_up = tk.messagebox.askyesno('是否重新输入？','重复登陆已注销请选择否，其他错误请选择是')
        if is_sign_up:
            return
        else:
            pass
        print(result)

    # 登陆教务系统
    print("登陆教务系统中，请等待")
    url = 'https://vpn.csuft.edu.cn/web/1/http/0/authserver.csuft.edu.cn/authserver/login?service=http%3A%2F%2Fjwgl.csuft.edu.cn%2F'
    driver.get(url)
    # 输入账号--通过html的id属性定位输入位置
    try:
        user_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mobileUsername")))
    except Exception as result:
        tk.messagebox.showerror('Error', result)
        print(result)
    user_login.send_keys(username)
    # 输入密码--通过html的id属性定位输入位置
    driver.find_element_by_id('mobilePassword').send_keys(password)
    sleep(3)
    # 点击登录按钮--通过xpath确定点击位置
    driver.find_element_by_xpath(
        '//*[@id="load"]').click()

    # 登陆成功个人信息不为空，表示登陆教务系统成功
    info = driver.find_element_by_class_name("Nsb_top_menu_nc").text
    if info != '':
        os.system("cls")
        welcome_text = '''中南林业科技大学
        欢迎%s同学，登陆教务系统成功
        '''% info
        window_sign_up = tk.Toplevel(window)
        window_sign_up.geometry('350x350')
        window_sign_up.title('登陆')
        tk.Label(window_sign_up, text=welcome_text).place(x=10, y=10)
        print(welcome_text)
        print("欢迎%s同学，登陆教务系统成功" % info)

    # 切换到成绩界面
    url_grade = 'https://vpn.csuft.edu.cn/web/1/http/1/jwgl.csuft.edu.cn/jsxsd/kscj/cjcx_list'
    driver.get(url_grade)
    sleep(1)
    list = driver.page_source
    grade_page = BeautifulSoup(list, "html.parser")
    table_th = grade_page.find("table", attrs={"class": "Nsb_r_list Nsb_table Nsb_table_first"})
    tbodu_th = table_th.find("tbody")
    table = grade_page.find("table", attrs={"id": "dataList"})
    tbody = table.find("tbody")
    trs = tbody.find_all("tr")
    f = open('results.csv', mode='a')
    for tr in tbodu_th.find_all("tr")[0], tbodu_th.find_all("tr")[1]:
        lst = tr.find_all("th")
        if len(lst) != 0:
            for th in lst:
                f.write(th.text.strip())
                f.write(',')
            f.write('\n')
    for tr in trs:
        lst = tr.find_all("td")
        if len(lst) != 0:
            for td in lst:
                f.write(td.text)
                f.write(',')
            f.write('\n')
    f.close()
    welcome_text = '''成绩数据已经写到根目录下：results.csv文件中
    绩点查询：
    '''
    tk.Label(window_sign_up, text=welcome_text).place(x=10, y=70)
    tk.Label(window, text='学号: ').place(x=50, y=150)
    tk.Label(window, text='密码: ').place(x=50, y=190)

    #计算绩点
    def calGPA():
        # 读取成绩表格数据，并存储在列表list里面
        try:
            csv_reader = csv.reader(open("results.csv"))
        except:
            print("文件读取失败，请检查根目录下是否有results.csv文件")
            input()
            exit(-1)
        # 把表格存到list里
        list = []
        for row in csv_reader:
            list.append(row)

        while True:
            # 输入查询的年份和学期
            start_year = start_semester_str.get()
            start_semester = ''
            end_year = end_semester_str.get()
            end_semester = ''

            # 判断出绩点、学分、开学学期是在表格的第几列
            for row in list:
                try:
                    GPA_col = int(row.index('绩点'))
                    grade_col = int(row.index('学分'))
                    year_col = int(row.index('开课学期'))
                except:
                    continue

            # 找出起始查询的年份学期和结束查询的年份和学期是在表格的第几行
            index = 0
            for i in list:
                try:
                    if i[year_col] == start_year and start_semester == '':
                        start_semester = index
                    if i[year_col] == end_year:
                        end_semester = index
                except:
                    continue
                index += 1
            if start_semester != '' and end_semester != '':
                break
            else:
                print("输入学期格式有误，请检查格式是否规范")

        # 计算总学分
        sum_grade = 0
        index = 0
        for i in list:
            try:
                if float(i[GPA_col]) != 0 and (int(start_semester) <= index + 2 <= int(end_semester)):
                    sum_grade += float(i[grade_col])
            except:
                continue
            index += 1

        # 计算平均绩点
        num_class = 0  # 课程数量
        GPA = 0
        index = 2
        for i in list[2:]:
            try:
                if (str(i[GPA_col]).isdigit() | (IsFloatNum(str(i[GPA_col])) and (float(i[GPA_col]) != 0))) and (
                        int(start_semester) <= index <= int(end_semester)):
                    GPA += float(i[GPA_col]) * float(i[grade_col]) / sum_grade
                    num_class += 1
            except:
                continue
            index += 1
        info = "你从%s到%s共计%d门课程的平均绩点为:%s" % (start_year, end_year, num_class, GPA)
        f = open('GPA.txt', mode='a')
        f.write(info + '\n')
        f.close()

        # 输出结果
        print('-' * 70)
        print("个人练手项目，请自行与教务系统和csv文件的数据对比验证后使用")
        print('-' * 70)
        print(info)
        print("已经将绩点数据写入到GPA.txt中")
        print('-' * 70)
        welcome_text = '-' * 60 + "\n个人练手项目，请自行与教务系统和csv文件的数据对比验证后使用\n" + '-' * 60 + '\n' + info + '\n' + "\n已经将绩点数据写入到GPA.txt中\n"
        window_GPA = tk.Toplevel(window)
        window_GPA.geometry('350x350')
        window_GPA.title('绩点')
        # 创建滚动条
        scroll = tk.Scrollbar()
        text = tk.Text(window_GPA, width=350, height=4)
        # 放到窗体右侧
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT, fill=tk.Y)
        # 关联
        scroll.config(command=text.yview)
        text.config(yscrollcommand=scroll.set)
        # height此处表示显示的行数
        # text = tkinter.Text(win,width=30,height=4)
        # text.pack()
        text.insert(tk.INSERT, welcome_text)

    #计算绩点窗口
    start_semester_str = tk.StringVar()
    start_semester_str.set('2018-2019-1')
    tk.Label(window_sign_up, text='起始学期（格式2018-2019-1）').place(x=10, y=130)
    start_semester_str = tk.Entry(window_sign_up, textvariable=start_semester_str)
    start_semester_str.place(x=200, y=130)

    end_semester_str = tk.StringVar()
    end_semester_str.set('2018-2019-2')
    tk.Label(window_sign_up, text='结束学期（格式2018-2019-2）').place(x=10, y=150)
    end_semester = tk.Entry(window_sign_up, textvariable=end_semester_str)
    end_semester.place(x=200, y=150)

    btn_comfirm_sign_up = tk.Button(window_sign_up, text='查询', command=calGPA)
    btn_comfirm_sign_up.place(x=150, y=230)

    print("成绩数据已经写到根目录下：results.csv文件中")

# 登陆按钮
btn_login = tk.Button(window, text='登陆', command=usr_login)
btn_login.place(x=225, y=230)

#主函数
if __name__ == '__main__':
    window.mainloop()

