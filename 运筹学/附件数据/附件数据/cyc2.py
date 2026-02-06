

from gurobipy import *
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd

# 读取需求数据
filePath = r"D:\\学习\\大三上\\运筹学\\附件数据\\附件数据\\all_1.xlsx"
data = pd.read_excel(filePath)  # 读取文件
demand = data.to_numpy()

# 参数定义
zone = 16  # 一个中转站有8个客户（假设有两个中转站，每个中转站服务8个客户）
timeInterval = 30  # 时间间隔，假设总周期为30个时间段
RentCost = 0.1  # 中转站的单位容积租赁费用
RentSize = 800  # 中转站的租赁容积
HoardCost = 1  # 单位货物在中转站的囤积成本
TravelCost1 = np.array([1, 3])  # 从工厂运输到中转站i的单位货物运输成本
TravelCost2 = 2 * np.array([2, 2, 2, 3, 3, 2, 4, 4, 7, 3, 4, 2, 3, 4, 7, 5])  # 从工厂运输到客户的单位货物运输成本

# 更新 DispathCost 矩阵为 18x18
# 第一个对应中转站,2-9对应8个客户 
DispathCost =  10*np.array([
    [0, 11, 15, 13, 47, 2, 1, 2, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [14, 0, 8, 15, 37, 3, 14, 12, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0],   
    [17, 8, 0, 23, 36, 9, 18, 16, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [13, 15, 22, 0, 42, 16, 11, 12, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [47, 36, 37, 42, 0, 39, 47, 45, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [12, 2, 8, 16, 38, 0, 10, 8, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 12, 16, 11, 47, 9, 0, 2, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 9, 14, 12, 46, 7, 2, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [13, 10, 17, 7, 38, 11, 12, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,0, 26, 34, 30, 14, 8, 25, 25, 32 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,26, 0, 21, 8, 40, 35, 5, 7, 30 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,34, 20, 0, 18, 48, 42, 15, 14, 15],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,30, 8, 18, 0, 44, 38, 5, 5, 29 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0,14, 41, 48, 44, 0, 13, 40, 40, 43],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,8, 34, 42, 38, 13, 0, 34, 33, 40],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,25, 5, 16, 5, 39, 33, 0, 1, 25],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,25, 7, 15, 6, 39, 33, 2, 0, 24],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,31, 30, 16, 29, 43, 40, 25, 24]
])  # 18x18 矩阵，假设未连接的路径成本为0，需要根据实际情况调整

TimeoutCost = 1000  # 客户i超时订单成本

# 运输时间定义
DispathT = np.ones((18, 18), dtype=int)  # 中转站和客户之间的运输时间，全部设为1
TravelT1 = np.array([1, 1])  # 工厂到中转站i的运输时间
TravelT2 = np.array([1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1, 2, 2, 1] * 2)  # 工厂到客户的运输时间

# 车辆及容量参数
Q = 100  # 车辆的最大容量
K = np.array([6, 6])  # 中转站i的车辆总数量
Max1 = RentSize  # 记录工厂运输到中转站运货量的最大值
Max2 = 100  # 记录工厂运输到客户运货量的最大值
Max3 = Q  # 记录从中转站运输到客户运货量的最大值
M = 100000  # 条件约束的一个大数

# 集合定义
warehouse = 0
transshipment_centers = [1, 10]  # 中转站编号
customers = [2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18]  # 客户编号从3到18
N_f = [warehouse]
N_s = transshipment_centers
N_p = customers
N = range(0,19)
T = range(timeInterval)  # 时间周期

# 客户到中转站的映射（假设每个中转站负责8个客户）
# 这里需要根据具体情况调整，假设中转站1负责客户3-10，中转站2负责客户11-18
customer_groups = {
    1: list(range(3, 11)),
    2: list(range(11, 19))
}

# 订单需求 r_i^t 和未完成订单 l_i^t 的初始化
# 假设demand数组的第一维对应时间，第二维对应客户
# 这里需要确认demand数据的结构，假设每一行对应一个时间段，每一列对应一个客户
# 如果不是，请根据实际数据调整
# 初始化未完成订单 l_i_t 和新增订单 r_i_t
# 这里假设demand.shape = (timeInterval, len(N_p))
r_i_t = {(i, t): demand[t, i - 3] for i in N_p for t in T}  # 时刻t客户i新增的订单需求量
l_i_t = {(i, t): 0 for i in N_p for t in T}  # 时刻t客户i累计的未完成订单

# 创建Gurobi模型
model = gp.Model("Transportation_Scheduling")

# 决策变量定义

# y_i^{1 t}: 从仓库运输到中转站 i 在时间 t 的货物量
y1 = model.addVars(N_s, T, vtype=GRB.CONTINUOUS, name="y1")

# y_i^{2 t}: 从仓库运输到客户 i 在时间 t 的货物量
y2 = model.addVars(N_p, T, vtype=GRB.CONTINUOUS, name="y2")

# y_i^{3 t}: 从中转站运输到客户 i 在时间 t 的货物量
y3 = model.addVars(N_p, T, vtype=GRB.CONTINUOUS, name="y3")

# x_{i j}^t: 车辆是否从点 i 到点 j 在时间 t 的二进制变量
# 由于i和j可以是中转站和客户，所以定义所有i,j属于N_s ∪ N_p
vehicle_nodes = range(1,19)
x = model.addVars(vehicle_nodes, vehicle_nodes, T, vtype=GRB.BINARY, name="x")

# h_i^t: 时刻 t 车辆到客户 i 时未卸货前的剩余负载
h = model.addVars(N_s, T, vtype=GRB.CONTINUOUS, name="h")

# k_i^t: 时刻 t 中转站 i 的实时存货量
k = model.addVars(N_s, T, vtype=GRB.CONTINUOUS, name="k")

# 目标函数
# 成本包括：
# 1. 中转站租赁成本
# 2. 中转站存货成本
# 3. 仓库到中转站运输成本
# 4. 仓库到客户运输成本
# 5. 车辆使用成本
# 6. 客户需求的超时成本

# 1. 中转站租赁成本
rent_cost = quicksum(RentCost * RentSize for i in N_s for t in T)

# 2. 中转站存货成本
hoard_cost = quicksum(HoardCost * k[i, t] for i in N_s for t in T)

# 3. 仓库到中转站运输成本
transport_cost1 = quicksum( (TravelCost1[i-1] if i ==1 else TravelCost1[i-9]) * y1[i, t]
                            for  i in N_s for t in T)
# 4. 仓库到客户运输成本
transport_cost2 = quicksum((TravelCost2[i - 2] if i <=9  else TravelCost2[i-3]) * y2[i, t]
                            for i in N_p for t in T)

# 5. 车辆使用成本
# 需要根据DispathCost矩阵定义车辆从i到j的运输成本
# 现在DispathCost是18x18矩阵，vehicle_nodes有18个节点
# 需要将i和j映射到DispathCost的行列
dispath_cost = quicksum(DispathCost[i-1][j-1] * x[i, j, t]
                        for i in vehicle_nodes for j in vehicle_nodes for t in T)

# 6. 客户需求的超时成本
timeout_cost = quicksum(TimeoutCost * l_i_t[i, t] for i in N_p for t in T)

# 目标函数为总成本的负数（因为题目中提到）
model.setObjective(
    -(
        rent_cost +
        hoard_cost +
        transport_cost1 +
        transport_cost2 +
        dispath_cost +
        timeout_cost
    ),
    GRB.MAXIMIZE
)

# 约束条件

# 1. 初始化约束
# 假设初始时刻所有中转站库存为0
for i in N_s:
    model.addConstr(k[i, 0] == 0, f"Initial_Inventory_{i}")


# 2. 车辆路径约束

# 2.1 每辆车在每个时间段只能有一个出发或到达
for t in T:
        # 中转站有多个车辆，限制每个车辆的出发
        # 这里简化为每个节点在每个时间段只能有K[i]次出发
    model.addConstr(
        quicksum(x[i, j, t] for i in  vehicle_nodes[1:9]  for j in vehicle_nodes[1:9]) <= 6,
        f"Vehicle_One_Path1_{i}_{t}"
    )
    model.addConstr(
        quicksum(x[i, j, t] for i in vehicle_nodes[1:9] for j in vehicle_nodes[10:18]) ==0,
        f"Vehicle_One_Path2_{i}_{t}"
    )
    model.addConstr(
        quicksum(x[i, j, t] for i in  vehicle_nodes[10:18] for j in vehicle_nodes[1:9]) ==0,
        f"Vehicle_One_Path3_{i}_{t}"
    )
    model.addConstr(
        quicksum(x[i, j, t] for i in  vehicle_nodes[10:18] for j in vehicle_nodes[10:18]) <= 6,
        f"Vehicle_One_Path4_{i}_{t}"
    )

# 2.2 每个客户最多只能有一辆车到达

for j in N_p:
    for t in T:
        model.addConstr(
            quicksum(x[i,j, t] for i in vehicle_nodes) <= 1,
            f"One_Vehicle_Per_Customer_{j}_{t}"
        )


# 3. 货物量约束

# 3.1 运输货物量不超过中转站容量
for i in N_s:
    for t in T:
        model.addConstr(
            y1[i, t] <= RentSize,
            f"Capacity_Constraint_{i}_{t}"
        )

for i in N_s:
    for t in T:
        model.addConstr(
            k[i, t] <= RentSize,
            f"k_constraint{i}_{t}"
        )



# 3.2 客户需求满足
for i in N_p:
    for t in T:
        model.addConstr(
            y2[i, t] + y3[i, t] + l_i_t[i, t] >= r_i_t[i, t],
            f"Demand_Constraint_{i}_{t}"
        )

# 3.3 车辆容量限制
for i in vehicle_nodes:
    for j in N_p:
            for t in T:
                model.addConstr(
                    y3[j, t] <= Q * x[i, j, t],
                    f"Vehicle_Capacity_{i}_{j}_{t}"
                )

# 4. 状态更新约束

for t in T:
    for i in N_s:
        if t < timeInterval - 1:
            # 中转站库存更新
            model.addConstr(
                k[i, t + 1] == k[i, t] + y1[i, t] - quicksum(y3[j, t] for j in [2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18]),
                f"Inventory_Update_{i}_{t}"
            )
    for i in N_p:
        if t < timeInterval - 1:
            # 未完成订单更新
            model.addConstr(
                l_i_t[i, t + 1] == l_i_t[i, t] + r_i_t[i, t] - y2[i, t] - y3[i, t],
                f"Unmet_Order_Update_{i}_{t}"
            )

# 5. 车辆路径与运输货物的关联约束

for i in N_s:
    for j in N_p:
        for t in T:
            model.addConstr(x[i, j, t] <= y3[j, t],  # 如果 y3[j, t] 为0，x[i, j, t] 必须为0
                            f"Vehicle_Path_Association_{i}_{j}_{t}")


            
            # 如果没有车辆开往客户 j，则 y3[j, t] = 0
            model.addConstr(
                y3[j, t] <= Q * quicksum(x[i, j, t] for i in N_s),
                f"Vehicle_Path_Relation_{i}_{j}_{t}"
            )

# 6. 车辆不经过中转站 i 到客户 j 的路径时，y3[j, t] = 0
for i in N_s:
    for j in N_p:
        for t in T:
            model.addConstr(
                y3[j, t] <= Q * x[i, j, t],
                f"Y3_Zero_If_No_Vehicle_{i}_{j}_{t}"
            )

# 7. 客户未完成订单为0如果没有车辆开往


# 8. 车辆流平衡约束


# 9. 客户一次只能由一辆车服务（已在2.2中定义）

# 设置模型参数（可选，根据需要调整）
model.Params.TimeLimit = 600  # 设置求解时间限制为600秒
model.Params.MIPGap = 0.01  # 设置MIPGap为1%

# 求解模型
model.optimize()

# 输出结果
if model.status == GRB.OPTIMAL:
    print("最优解找到。目标值（成本）:", model.objVal)
    # 输出决策变量的值
    # y1: 从仓库到中转站的运输量
    print("\n从仓库到中转站的运输量 y1:")
    for i in N_s:
        for t in T:
            if y1[i, t].X > 0:
                print(f"中转站 {i}, 时间 {t}: {y1[i, t].X}")

    # y2: 从仓库到客户的运输量
    #print("\n从仓库到客户的运输量 y2:")
    #for i in N_p:
    #    for t in T:
     #       if y2[i, t].X > 0:
     #           print(f"客户 {i}, 时间 {t}: {y2[i, t].x}")

    # y3: 从中转站到客户的运输量
    print("\n从中转站到客户的运输量 y3:")
    for i in N_p:
        for t in T:
            if y3[i, t].X > 0:
                print(f"客户 {i}, 时间 {t}: {y3[i, t].X}")

    # x: 车辆路径
    print("\n车辆路径 x:")
    for i in vehicle_nodes:
        for j in vehicle_nodes:
            for t in T:
                if x[i, j, t].X > 0.5:  # 二进制变量，使用0.5作为阈值
                    print(f"时间 {t}: 从 {i} 到 {j} 有车辆移动")
else:
    print("未找到最优解。")
