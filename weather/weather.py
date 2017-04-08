#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import xlsxwriter


# 创建excel
workbook = xlsxwriter.Workbook("weather.xlsx")
# 创建sheet
worksheet = workbook.add_worksheet("weather")
# 清空列以及行数
worksheet.set_column("A:A", 7)
worksheet.set_column("B:B", 7)
worksheet.set_column("C:C", 7)

# 存储数据 方法
def savedata(colom, content_list):
    # 传入参数 colom: 操作的行 content_list:行中每列内容
    colom_a = "A" + colom
    colom_b = "B" + colom
    colom_c = "C" + colom
    # 日期
    worksheet.write(colom_a, content_list[0])
    # 天气
    worksheet.write(colom_b, content_list[1])
    # 最高温度 - 最低温度
    worksheet.write(colom_c, content_list[2] + "-" + content_list[3])



def get_content(url, data=None):
    rep = requests.get(url, timeout=60)
    rep.encoding = 'utf-8'
    return rep.text

# 获取数据
def get_data(htmltext, city):
    content = []
    bs = BeautifulSoup(htmltext, "html.parser")
    body = bs.body
    data = body.find('div', {'id': '7d'})
    ul = data.find('ul')
    li = ul.find_all('li')
    for day in li:
        # line = [city] # 城市名
        line = [] 
        date = day.find('h1').string
        line.append(date) # 日期
        text = day.find_all('p')
        # 天气状况
        line.append(text[0].string)
        # 最高温度
        if text[1].find('span') is None:
            temperature_H = None
        else:
            temperature_H = text[1].find('span').string.replace('℃', '')
        # 最低温度
        temperature_L = text[1].find('i').string.replace('℃', '')
        line.append(temperature_H)
        line.append(temperature_L)
        content.append(line)
    return content

# 根据城市名称拼接url
def get_url(city_name):
    url = 'http://www.weather.com.cn/weather/'
    with open('city.txt', 'r', encoding='UTF-8') as fs:
        lines = fs.readlines()
        for line in lines:
            if(city_name in line):
                code = line.split('=')[0].strip()
                return url + code + '.shtml'
    raise ValueError('invalid city name')


if __name__ == '__main__':
    cities = input('请输入城市名称:').split(" ")
    print("|     日期     |  天气状况  |    温度   |")
    print("-----------------------------------------")
    for city in cities:
        url = get_url(city)
        html = get_content(url)
        result = get_data(html, city)

        # 从第二行开始存储,因为第一行 ["日期", "天气状况", "温度", ""] 存储这些信息
        colom = 2
        savedata("1", ["日期", "天气状况", "温度", ""])
        for day_list in result:

            # 存储数据
            savedata(str(colom), day_list)
            # 一共7天数据
            colom = colom + 1


            if len(day_list[1]) == 1:
                day_list[1] = "   " + day_list[1] + "     "
            elif len(day_list[1]) == 2:
                day_list[1] = "  " + day_list[1] + "    "
            elif len(day_list[1]) == 4:
                day_list[1] = " " + day_list[1] + " "
            elif len(day_list[1]) == 3:
                day_list[1] = "  " + day_list[1] + "  "

            if len(day_list[0]) == 6:
                day_list[0] = day_list[0] + " "
            if len(day_list[3]) == 1:
                day_list[3] = day_list[3] + " "
            print("| " + day_list[0] + " | " + day_list[1] + " | " + day_list[2] + "℃ ~ " + day_list[3] + "℃ |") 
            print("-----------------------------------------")
    # 操作完毕关闭excel 类似数据库操作
    workbook.close()








