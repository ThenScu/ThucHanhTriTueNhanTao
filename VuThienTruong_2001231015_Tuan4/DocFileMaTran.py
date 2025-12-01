# -*- coding: utf-8 -*-
import sys 

"""
Created on Mon Dec  1 13:59:33 2025
@author: Administrator
"""

# --- PHẦN ĐỌC FILE ---
G = []
try:
    with open('InputMatrix.txt', 'r') as f:
        for line in f:
            row = [int(x) for x in line.strip().split()]
            if row:
                G.append(row)
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file 'input_matrix.txt'. Hãy tạo file này trước!")
    sys.exit() 

# Tên các đỉnh của đồ thị (Theo bảng của bạn)
node = "123456" 
# --------------------------------

t_={}
for i in range(len(G)):
  t_[node[i]] = i
# Bậc của các đỉnh
degree =[]
for i in range(len(G)):
  degree.append(sum(G[i]))
  
# Màu có thể sử dụng để tô cho các đỉnh
colorDict = {}
for i in range(len(G)):
  colorDict[node[i]]=["Blue","Red","Yellow","Green","Purple","Orange"]

# Sắp xếp các đỉnh theo thứ tự bậc
sortedNode=[]
indeks = []
# use selection sort
for i in range(len(degree)):
  _max = -1
  idx = -1
  for j in range(len(degree)):
    if j not in indeks:
      if degree[j] > _max:
        _max = degree[j]
        idx = j
  indeks.append(idx)
  sortedNode.append(node[idx])
# Phần xử lý tô màu (sử dụng màu ít nhất có thể)
theSolution={}
for n in sortedNode:
  setTheColor = colorDict[n]
  theSolution[n] = setTheColor[0]
  adjacentNode = G[t_[n]]
  for j in range(len(adjacentNode)):
    if adjacentNode[j]==1 and (setTheColor[0] in colorDict[node[j]]):
      colorDict[node[j]].remove(setTheColor[0])
# In kết quả từng đỉnh và màu đã tô tương ứng
for t,w in sorted(theSolution.items()):
  print("Đỉnh ",t," = ",w)