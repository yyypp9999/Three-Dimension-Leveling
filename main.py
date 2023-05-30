import os
import sys
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import xlrd
import math

# 创建tkinter窗口并隐藏
root = tk.Tk()
root.withdraw()

# 弹出文件选择框，让用户选择基准平面坐标文件
basiclev_file = filedialog.askopenfilename(title='选择基准平面坐标文件' ,filetypes=[("Excel files", "*.xls;*.xlsx")])

# 弹出文件选择框，让用户选择测量平面坐标文件
measurelev_files = filedialog.askopenfilenames(title='选择测量平面坐标文件' , filetypes=[("Excel files", "*.xls;*.xlsx")])

# 读取基准平面坐标
basiclev = xlrd.open_workbook(basiclev_file)
sheet = basiclev.sheet_by_index(0)

# 第一行是列名
colName = []
for j in range(sheet.ncols):
    colName.append(sheet.cell_value(0, j))

# 提取除了第一行以外的数据

data = np.ones((sheet.nrows - 1, sheet.ncols))
for j in range(data.shape[1]):
    for i in range(data.shape[0]):
        try:
            data[i, j] = sheet.cell_value(i + 1, j)
        except:
            print("err occur:", i, j, sheet.cell_value(i, j))

basiclev_data = pd.DataFrame(data)

#平面方程计算

x1 = data[0,0]
y1 = data[0,1]
z1 = data[0,2]
x2 = data[1,0]
y2 = data[1,1]
z2 = data[1,2]
x3 = data[2,0]
y3 = data[2,1]
z3 = data[2,2]


a = (y2-y1)*(z3-z1)-(z2-z1)*(y3-y1)
b = (z2-z1)*(x3-x1)-(x2-x1)*(z3-z1)
c = (x2-x1)*(y3-y1)-(y2-y1)*(x3-x1)
d = 0-(a*x1+b*y1+c*z1)

print("平面方程为：",a,"x+",b,"y+",c,"z+",d,"=0")

cos_level = abs(c/math.sqrt(a**2+b**2+c**2))

# 创建保存结果的文件夹
result_folder = os.path.dirname('D:') + os.sep + '平面校准'

if not os.path.exists(result_folder):
    os.mkdir(result_folder)


# 遍历每个测量平面文件并进行处理
for measurelev_file in measurelev_files:
    # 读取需要处理的数据
    measurelev_data = xlrd.open_workbook(measurelev_file)
    sheet = measurelev_data.sheet_by_index(0)

    # 第一行是列名
    colName = []
    for j in range(sheet.ncols):
        colName.append(sheet.cell_value(0, j))
    # 提取除了第一行以外的数据

    data_temp = np.ones((sheet.nrows - 1, sheet.ncols))
    for j in range(data_temp.shape[1]):
        for i in range(data_temp.shape[0]):
            try:
                data_temp[i, j] = sheet.cell_value(i + 1, j)
            except:
                print("err occur:", i, j, sheet.cell_value(i, j))

    data = pd.DataFrame(data_temp)
    
    # 读取第一列数据
    col1 = data.iloc[:, 0]

    # 读取第二列数据
    col2 = data.iloc[:, 1]

    # 读取第三列数据
    col3 = data.iloc[:, 2]

    z_delta =[]
    z_calibrated = []

    #遍历每行数据并将平面校准的数据保存在下一列
    for i in range(data.shape[0]):
        x = data.iloc[i,0]
        y = data.iloc[i,1]
        z = data.iloc[i,2]
        m = -(d+a*x+b*y)/c
        z_delta.append(m)
        n = (m-z)/cos_level
        z_calibrated.append(n)

    # 将处理后的data以xlsx保存到结果文件夹中
    result_file = os.path.join(result_folder, os.path.basename(measurelev_file))
    pd.DataFrame({'X': col1, 'Y': col2, 'Z': col3, '基准平面理论Z值': z_delta, '校准后的Z值': z_calibrated}).to_excel(result_file, index=False)
    print(f"{measurelev_file} 处理完成，并保存到 {result_file} 中。")    
