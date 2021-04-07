# -*- coding =utf-8 -*-
# @Time : 2021/4/6 14:42
# @Author : 胡伊斐
# @File : getGrade.py
# @Software : PyCharm
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

#获取成绩数据
def getResult():

    #读取学号密码信息
    username = input("学号:")
    password = input("密码:")
    print("正在加载，马上就好~")
    url='http://authserver.csuft.edu.cn/authserver/login?service=http%3A%2F%2Fjwgl.csuft.edu.cn%2F'

    # 后台运行
    try:
        option=webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-logging'])#不打印消息
        option.add_argument('headless')  # 设置option
        driver = webdriver.Chrome(chrome_options=option)  # 调用带参数的谷歌浏览器
        driver.get(url)
        # 将窗口最大化
        driver.maximize_window()
    except Exception as result:
        print(result)
        print("登陆失败，请检查账号密码或者网络")
        input()
        exit(-1)

    # 输入账号--通过html的id属性定位输入位置--改为你的账号
    user_login = driver.find_element_by_id('username')
    user_login.send_keys(username)
    # 输入密码--通过html的id属性定位输入位置--改为你的密码
    driver.find_element_by_id('password').send_keys(password)
    # 点击登录按钮--通过xpath确定点击位置
    driver.find_element_by_xpath(
        '//*[@id="casLoginForm"]/p[4]/button').click()

    # 登陆成功个人信息不为空，表示登陆教务系统成功
    info = driver.find_element_by_class_name("Nsb_top_menu_nc").text
    if info != '':
        os.system("cls")
        print('''
         ____ ____  _   _ _____ _____ 
        / ___/ ___|| | | |  ___|_   _|
       | |   \___ \| | | | |_    | |  
       | |___ ___) | |_| |  _|   | |  
        \____|____/ \___/|_|     |_|''')
        print("欢迎%s同学，登陆教务系统成功" % info)

    # 切换到成绩界面
    url_grade='http://jwgl.csuft.edu.cn/jsxsd/kscj/cjcx_list'
    driver.get(url_grade)
    sleep(1)
    list=driver.page_source
    grade_page=BeautifulSoup(list,"html.parser")
    table_th = grade_page.find("table",attrs={"class":"Nsb_r_list Nsb_table Nsb_table_first"})
    tbodu_th = table_th.find("tbody")
    table = grade_page.find("table",attrs={"id":"dataList"})
    tbody = table.find("tbody")
    trs = tbody.find_all("tr")
    f = open('results.csv',mode='a')
    for tr in tbodu_th.find_all("tr")[0],tbodu_th.find_all("tr")[1]:
        lst = tr.find_all("th")
        if len(lst) != 0:
            for th in lst:
                f.write(th.text.strip())
                f.write(',')
            f.write('\n')
    for tr in trs:
        lst = tr.find_all("td")
        if len(lst) !=0:
            for td in lst:
                f.write(td.text)
                f.write(',')
            f.write('\n')
    f.close()
    print("成绩数据已经写到根目录下：results.csv文件中")

