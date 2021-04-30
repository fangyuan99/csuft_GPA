# -*- coding =utf-8 -*-
# @Time : 2021/4/7 8:39
# @Author : 胡伊斐
# @File : vpn.py
# @Software : PyCharm

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.alert import Alert
import os

#获取成绩数据
def getResult_vpn():
    #读取学号密码信息
    username = input("学号:")
    password = input("密码:")
    print("正在加载，马上就好~")


    # 后台运行
    try:
        option=webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-logging'])  # 不打印消息
        mobileEmulation = {'deviceName': 'Galaxy S5'}
        option.add_experimental_option('mobileEmulation', mobileEmulation)
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('headless')  # 后台运行
        url_vpn='https://vpn.csuft.edu.cn/por/login_psw.csp?rnd=0.4175854108433872#https%3A%2F%2Fvpn.csuft.edu.cn%2F'
        driver = webdriver.Chrome(chrome_options=option)
        driver.get(url_vpn)
        #判断是否重复登陆vpn
        try:
            error=driver.find_element_by_xpath("/html/body/div/div/div/p").text
            print(error[0:9]+',请重新启动并选择处于校园网环境使用本软件')
            sleep(10)
        except:
            # 将窗口最大化
            driver.maximize_window()
            print("登陆vpn中，请等待")
    except Exception as result:
        print(result)
        print("登陆失败，请检查账号密码或者网络")
        input()
        exit(-1)

    # 登录vpn

    user_login = driver.find_element_by_id('user')
    user_login.send_keys(username)
    driver.find_element_by_id("pwd").send_keys(password)
    driver.find_element_by_xpath('//*[@id="login_form"]/div/table[2]/tbody/tr/td/table/tbody/tr/td[1]/button').click()
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="service_item_2"]/div/a'))
        )
        text = driver.page_source
        print("vpn登陆成功")
    except Exception as result:
        print(result)

    #登陆教务系统
    print("登陆教务系统中，请等待")
    url='https://vpn.csuft.edu.cn/web/1/http/0/authserver.csuft.edu.cn/authserver/login?service=http%3A%2F%2Fjwgl.csuft.edu.cn%2F'
    driver.get(url)
    # 输入账号--通过html的id属性定位输入位置
    user_login = driver.find_element_by_id('mobileUsername')
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
        print('''
      ____ ____  _   _ _____ _____ 
     / ___/ ___|| | | |  ___|_   _|
    | |   \___ \| | | | |_    | |  
    | |___ ___) | |_| |  _|   | |  
     \____|____/ \___/|_|     |_|''')
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
    print("成绩数据已经写到根目录下：results.csv文件中")
