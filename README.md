---
title: 5分制绩点计算器3
categories:
  - null
tags:
  - 学习
date: 2021-04-07 17:47:32

---

## 前言

之前已经在我的博客更新了两篇有关[5分制教务系统绩点计算](http://fangyuan99.gitee.io/blog/2020/10/14/%E6%95%99%E5%8A%A1%E7%B3%BB%E7%BB%9F%E7%BB%A9%E7%82%B9%E8%AE%A1%E7%AE%97/#more)，[5分制教务系统计算2](http://fangyuan99.gitee.io/blog/2021/04/03/5%E5%88%86%E5%88%B6%E6%95%99%E5%8A%A1%E7%B3%BB%E7%BB%9F%E7%BB%A9%E7%82%B9%E8%AE%A1%E7%AE%972/#more)，这次利用网页版的vpn实现了不用连接校园网版本的计算器，数据来源于教务系统，并且支持计算输入任意学期的绩点。操作简单功能全面，后续可能会添加更多的功能，比如查询历史等级考试成绩等等，只要电脑上装了Chrome，再下载一个小驱动配合即可使用

<!--more-->

## 教程

### 小白

#### 下载软件

去文末任意位置下载软件后，把`程序.zip`解压

#### 安装驱动

1.本项目是用`selenium`配合[chromedriver](http://npm.taobao.org/mirrors/chromedriver)实现的，首先需要查询自己的Chrome版本号。在Chrome浏览器地址栏输入:`chrome://version/`

![](https://i.vgy.me/IxEF2G.png)

2.到驱动网站找到自己系统对应的版本下载，后几位可以忽略，前几位相同一般就可以用了(我在`程序.zip`已经附上我电脑chrome版本的驱动，如果不能用请根据自己的chrome版本下载)

3.下载好之后解压到与`程序.zip`解压路径相同的路径（必须和`csuft_GPA.exe`同一路径）

4.双击`csuft_GPA.exe`就行，所有成绩数据会被写入到根目录下的`result.csv`文件下，绩点数据会被写入到根目录下的`GPA.txt`文件下，演示（这里我直接把密码封装好了，正式版本是要自己输密码的）：
![教程](https://i.vgy.me/Mo9A5O.gif)
![教程](https://i.vgy.me/uZyjl8.gif)

#### 版本说明

纯小白或者第一次使用直接用`在线版`即可，是否连接校园网按照自己的网络条件选择。若是已经下载好了成绩表格`result.csv`，则可以用`本地版`计算绩点数据，不需要使用网络请求

### 有编程基础

可以自己从文末的仓库里面查看源码，自己可以添加功能......

## 下载地址

博客地址:

https://fangyuan99.gitee.io/blog/2021/04/07/5%E5%88%86%E5%88%B6%E7%BB%A9%E7%82%B9%E8%AE%A1%E7%AE%97%E5%99%A83/#more

github:https://github.com/fangyuan99/csuft_GPA

gitee:https://gitee.com/fangyuan99/csuft_GPA

百度网盘:https://pan.baidu.com/s/1ANwNaYEucwoG64khTYN0yQ  提取码：6666 