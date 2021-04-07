# -*- coding =utf-8 -*-
# @Time : 2021/4/6 11:06
# @Author : 胡伊斐
# @File : 模拟Chrome.py
# @Software : PyCharm
import csv
import os
from getGrade import getResult
from getGrade import IsFloatNum
from vpn import getResult_vpn


# 计算绩点的函数
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
        start_year = input("请输入你要查询的起始学期(例如2018-2019-1):")
        start_semester = ''
        end_year = input("请输入你要查询的结束学期(例如2018-2019-2):")
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
        if start_semester!='' and end_semester!='':
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

    #输出结果
    print('-'*70)
    print("个人练手项目，请自行与教务系统和csv文件的数据对比验证后使用")
    print('-'*70)
    print(info)
    print("已经将绩点数据写入到GPA.txt中")
    print('-'*70)


if __name__ == "__main__":
    while True:
        judge=input("请选择使用本地版还是在线版? 1.在线版（第一次使用或者没有成绩表格数据选在线版）， 2.本地版， 3.退出:")
        if judge!='2' and judge!='1' and judge!='3':
            print("输入有误，请重新选择")
        elif judge=='1':
            judge2=input("请选择是否处于校园网环境：1.是，2.否")
            if judge2=='1':
                getResult()
            elif judge2=='2':
                getResult_vpn()
            else:
                print("输入有误，请重试")
                continue
            calGPA()
            continue
        elif judge=='2':
            calGPA()
            continue
        elif judge=='3':
            exit(0)
