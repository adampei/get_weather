import xlsxwriter

# 创建excel
workbook = xlsxwriter.Workbook("weather.xlsx")
# 创建sheet & 命名
worksheet = workbook.add_worksheet(name="test")
# 清空A列 0~20
worksheet.set_column("A:A", 20)
# 设置要写入内容属性 bold:字体加粗
bold = workbook.add_format({"bold" : True})
# 写入数据
worksheet.write("A1", "hello")
worksheet.write("A2", "world", bold)
worksheet.write(2, 0, 123)
worksheet.write(3, 0, 122.4311)

# 插入图片
worksheet.insert_image("B1", "timg.jpeg")


workbook.close()