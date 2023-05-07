import os
import sys
import numpy


#平面方程计算

A = input("请输入第一个点的坐标：")
B = input("请输入第二个点的坐标：")
C = input("请输入第三个点的坐标：")
x1 = A[1]
y1 = A[2]
z1 = A[3]
x2 = B[1]
y2 = B[2]
z2 = B[3]
x3 = C[1]
y3 = C[2]
z3 = C[3]

a = (y2-y1)*(z3-z1)-(z2-z1)*(y3-y1)
b = (z2-z1)*(x3-x1)-(x2-x1)*(z3-z1)
c = (x2-x1)*(y3-y1)-(y2-y1)*(x3-x1)
d = 0-(a*x1+b*y1+c*z1)

print("平面方程为：",a,"x+",b,"y+",c,"z+",d,"=0")

z_delta = -(d+a*x+b*y)/c

z_p = input("请输入测量点的坐标：")

z_calibrated = z_p-z_delta


