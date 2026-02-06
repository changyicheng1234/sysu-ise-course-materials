from gurobipy import *
import numpy as np
import pandas as pd

# 数据初始化
filePath = r"D:\\学习\\大三上\\运筹学\\附件数据\\附件数据\\all_1.xlsx"
data = pd.read_excel(filePath)  # 读取需求数据
demand = data.to_numpy()  # 转换为NumPy数组

zone = 16  # 一个中转站有8个客户
timeInterval = 30  # 时间间隔
RentCost = 0.1  # 中转站单位容积租赁费用
RentSize = 800  # 中转站租赁容积
HoardCost = 1  # 单位货物囤积在中转站的囤积成本
TravelCost1 = np.array([1, 3])  # 从仓库到中转站的单位货物运输成本
TravelCost2 = 2 * np.array([2, 2, 2, 3, 3, 2, 4, 4, 7, 3, 4, 2, 3, 4, 7, 5])  # 工厂到客户运输成本
DispathCost = 10 * np.array([[0, 11, 15, 13, 47, 2, 1, 2, 10],
                             [14, 0, 8, 15, 37, 3, 14, 12, 9],
                             [17, 8, 0, 23, 36, 9, 18, 16, 16],
                             [13, 15, 22, 0, 42, 16, 11, 12, 7],
                             [47, 36, 37, 42, 0, 39, 47, 45, 38],
                             [12, 2, 8, 16, 38, 0, 10, 8, 9],
                             [2, 12, 16, 11, 47, 9, 0, 2, 9],
                             [3, 9, 14, 12, 46, 7, 2, 0, 8],
                             [13, 10, 17, 7, 38, 11, 12, 11, 0],
                             [0, 26, 34, 30, 14, 8, 25, 25, 32],
                             [26, 0, 21, 8, 40, 35, 5, 7, 30],
                             [34, 20, 0, 18, 48, 42, 15, 14, 15],
                             [30, 8, 18, 0, 44, 38, 5, 5, 29],
                             [14, 41, 48, 44, 0, 13, 40, 40, 43],
                             [8, 34, 42, 38, 13, 0, 34, 33, 40],
                             [25, 5, 16, 5, 39, 33, 0, 1, 25],
                             [25, 7, 15, 6, 39, 33, 2, 0, 24],
                             [31, 30, 16, 29, 43, 40, 25, 24, 0]])
TimeoutCost = 1000  # 客户超时订单成本

DispathT = np.ones((18, 9))  # 中转站和客户之间的运输时间矩阵，假设为1
TravelT1 = np.array([1, 1])  # 仓库到中转站运输时间
TravelT2 = np.array([1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1, 2, 2, 1] * 2)  # 仓库到客户运输时间

Q = 100  # 车辆最大容量
K = np.array([6, 6])  # 每个中转站车辆数量
T = 10  # 总周期数

# Gurobi模型创建
model = Model("Product Transportation")

# 决策变量
x = model.addVars(18, 9, T, vtype=GRB.BINARY, name="x")  # x[i, j, t]: 是否从i到j运输
y1 = model.addVars(2, T, vtype=GRB.CONTINUOUS, name="y1")  # 仓库到中转站货物量
y2 = model.addVars(16, T, vtype=GRB.CONTINUOUS, name="y2")  # 仓库到客户货物量
y3 = model.addVars(16, T, vtype=GRB.CONTINUOUS, name="y3")  # 中转站到客户货物量
l = model.addVars(16, T, vtype=GRB.CONTINUOUS, name="l")  # 客户未完成需求量
h = model.addVars(2, T, vtype=GRB.CONTINUOUS, name="h")  # 中转站存货量

# 目标函数
model.setObjective(
    quicksum(RentCost * RentSize) +
    quicksum(HoardCost * h[i, t] for i in range(2) for t in range(T)) +
    quicksum(TravelCost1[i] * y1[i, t] for i in range(2) for t in range(T)) +
    quicksum(TravelCost2[j] * y2[j, t] for j in range(16) for t in range(T)) +
    quicksum(DispathCost[i, j] * x[i, j, t] for i in range(18) for j in range(9) for t in range(T)) +
    quicksum(TimeoutCost * l[j, t] for j in range(16) for t in range(T)),
    GRB.MINIMIZE
)

# 约束条件

# 1. 客户需求必须满足
for j in range(16):
    for t in range(T):
        model.addConstr(y2[j, t] + y3[j, t] + l[j, t] == demand[j, t])

# 2. 中转站货物平衡
for i in range(2):
    for t in range(T - 1):
        model.addConstr(h[i, t + 1] == h[i, t] + y1[i, t] - quicksum(y3[j, t] for j in range(8 * i, 8 * (i + 1))))

# 3. 车辆容量限制
for i in range(18):
    for j in range(9):
        for t in range(T):
            model.addConstr(x[i, j, t] * Q >= y3[j, t])

# 4. 客户只能由一辆车服务
for j in range(16):
    for t in range(T):
        model.addConstr(quicksum(x[i, j, t] for i in range(18)) <= 1)

# 求解模型
model.optimize()

# 输出结果
if model.status == GRB.OPTIMAL:
    for v in model.getVars():
        if v.X > 0:
            print(f"{v.VarName}: {v.X}")
    print(f"Optimal Cost: {model.ObjVal}")
else:
    print("No optimal solution found.")
