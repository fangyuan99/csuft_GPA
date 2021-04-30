# -*- coding =utf-8 -*-
# @Time : 2021/4/30 21:43
# @Author : 胡伊斐
# @File : test.py
# @Software : PyCharm
import tkinter as tk
import csv
from tkinter import messagebox  # import this to fix messagebox error
import pickle
window = tk.Tk()
window.title('Welcome to Mofan Python')
window.geometry('450x300')
window_sign_up = tk.Toplevel(window)
window_sign_up.geometry('350x200')
window_sign_up.title('登陆')

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
btn_comfirm_sign_up.place(x=150, y=30)

# entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
# entry_new_name.place(x=150, y=10)
window.mainloop()
