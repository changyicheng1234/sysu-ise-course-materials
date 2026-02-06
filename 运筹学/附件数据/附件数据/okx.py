import gurobipy as gp
from gurobipy import GRB, quicksum
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ====================
# 读取需求数据
# ====================
filePath = r"D:\\学习\\大三上\\运筹学\\附件数据\\附件数据\\all_1.xlsx"
try:
    data = pd.read_excel(filePath)  # 读取文件
    demand = data.to_numpy()
    print("需求数据成功读取。")
except Exception as e:
    print(f"读取需求数据时出错: {e}")
    exit()

# ====================
# 基本参数设置
# ====================
zone = 16            # 总客户数量（每个中转站有8个客户）
timeInterval = 30    # 时间间隔数量

# ====================
# 成本和容量等参数
# ====================
RentCost = 0.1       # 中转站的单位容积租赁费用
RentSize = 800       # 中转站的租赁容积
HoardCost = 1      # 单位货物在中转站的囤积成本（调整后）

TravelCost1 = np.array([1, 3])
# 工厂 -> 中转站 i 的单位货物运输成本
#   - 中转站1: TravelCost1[0] = 1
#   - 中转站2: TravelCost1[1] = 3

TravelCost2 = 2 * np.array([2, 2, 2, 3, 3, 2, 4, 4,
                            7, 3, 4, 2, 3, 4, 7, 5])
# 工厂 -> 客户 j 的单位货物运输成本（16个客户）



TimeoutCost = 1000
# 客户j超时订单成本



# 车辆最大容量
Q = 100

# 每个中转站可用车辆总数
K = np.array([6, 6])

# 其他参数
Max1 = RentSize
Max2 = 100
Max3 = Q
M = 100000

# ====================
# 定义集合
# ====================
S = [1, 2]          # 中转站节点编号为1和2
P1 = list(range(3, 11))   # 中转站1对应的客户编号3-10（8个客户）
P2 = list(range(11, 19))  # 中转站2对应的客户编号11-18（8个客户）
P = P1 + P2         # 所有客户
N = S + P           # 所有节点（不包括仓库）

# ====================
# DispatchCost 的处理
# ====================
# 假设 DispatchCost 为每个中转站到客户的固定调度成本（与时间无关）
# DispatchCost 是一个18x9矩阵，假设前8行对应 P1，后8行对应 P2
# 并假设 DispatchCost 的第一列为基础调度成本
DispatchCost_matrix = np.array([
    [0, 11, 15, 13, 47, 2, 1, 2, 10],
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
    [31, 30, 16, 29, 43, 40, 25, 24, 0]
])

# 取 DispatchCost1 和 DispatchCost2 的第一列作为调度成本
DispatchCost1 = DispatchCost_matrix[0:9, :]  # 中转站1对应P1的调度成本
DispatchCost2 = DispatchCost_matrix[9:17, :] # 中转站2对应P2的调度成本

# ====================
# 创建模型
# ====================
model = gp.Model("Transportation_Optimization")

# ====================
# 决策变量
# ====================
# x[i,j,t]: 是否有车辆从中转站i到客户j在时刻t运输
x = model.addVars(S, P, range(timeInterval), vtype=GRB.BINARY, name="x")

# y1[i,t]: 从工厂到中转站 i 的货物量
y1 = model.addVars(S, range(timeInterval), lb=0, ub=Max1, vtype=GRB.CONTINUOUS, name="y1")

# y2[j,t]: 从工厂到客户 j 的货物量
y2 = model.addVars(P, range(timeInterval), lb=0, ub=Max2, vtype=GRB.CONTINUOUS, name="y2")

# y3[i,j,t]: 中转站 i -> 客户 j 的货物量，仅定义有效的 (i,j,t)
y3 = model.addVars([(i, j, t) for i in S for j in (P1 if i ==1 else P2) for t in range(timeInterval)],
                  lb=0, ub=Max3, vtype=GRB.CONTINUOUS, name="y3")

# l[j,t]: 客户 j 在时刻 t 的未完成订单量
l = model.addVars(P, range(timeInterval), lb=0, vtype=GRB.CONTINUOUS, name="l")

# h[i,t]: 中转站 i 在时刻 t 的实时存货量
h = model.addVars(S, range(timeInterval), lb=0, vtype=GRB.CONTINUOUS, name="h")

# k[i,t]: 中转站 i 在时刻 t 的可用车辆数量
k_ub = {(i, t): K[i - 1] for i in S for t in range(timeInterval)}
k = model.addVars(S, range(timeInterval), lb=0, ub=k_ub, vtype=GRB.INTEGER, name="k")

# li[j,t]: 时刻 t 车辆到客户 j 时未卸货前的剩余负载
li = model.addVars(P, range(timeInterval), lb=0, ub=Q, vtype=GRB.CONTINUOUS, name="li")

# ====================
# 目标函数
# ====================

# 1. 中转站租赁费用：RentCost * RentSize * len(S)
total_rent_cost = RentCost * RentSize * len(S)

# 2. 存货成本：HoardCost * h[i,t]
total_hoard_cost = quicksum(HoardCost * h[i, t] for i in S for t in range(timeInterval))

# 3. 工厂 -> 中转站 运输成本：TravelCost1[i-1] * y1[i,t]
total_travel_cost1 = quicksum(TravelCost1[i - 1] * y1[i, t]
                              for i in S
                              for t in range(timeInterval))

# 4. 工厂 -> 客户 运输成本：TravelCost2[j-3] * y2[j,t]
total_travel_cost2 = quicksum(TravelCost2[j - 3] * y2[j, t]
                              for j in P
                              for t in range(timeInterval))

# 5. 中转站 -> 客户 运输成本：TravelCost3 * y3[i,j,t]
# total_travel_cost3 = quicksum(TravelCost3 * y3[i, j, t]
                            # for (i, j, t) in y3.keys())


# 6. 调用车辆的成本：每调度一次车辆，成本为 DispatchCost1[j-3] 或 DispatchCost2[j-11]
total_dispatch_cost = quicksum(DispatchCost1[j-3,j-3] * x for (i, j, t) in y3.keys()) + \
                       quicksum(DispatchCost2[j-11,j-11] * x for (i, j, t) in y3.keys())



# 7. 客户需求超时成本：TimeoutCost * l[j,t]
total_timeout_cost = quicksum(TimeoutCost * l[j, t]
                              for j in P
                              for t in range(timeInterval))



# 合并目标函数
total_cost = (total_rent_cost
              + total_hoard_cost
              + total_travel_cost1
              + total_travel_cost2
              + total_dispatch_cost
              + total_timeout_cost)

model.setObjective(total_cost, GRB.MINIMIZE)

# ====================
# 约束条件
# ====================

# 1. 每个客户在每个时刻的需求必须被满足（包括未完成订单）
for j in P:
    for t in range(timeInterval):
        if t == 0:
            # t=0 时刻未完成订单 = 当期需求 - 当期满足量
            model.addConstr(
                y2[j, t] + quicksum(y3[i, j, t] for i in S if j in (P1 if i ==1 else P2)) + l[j, t] == demand[t, j - 3],
                name=f"Demand_Fulfill_{j}_{t}"
            )
        else:
            # t>0 时刻未完成订单 = 上时刻未完成订单 + 当期需求 - 当期满足量
            model.addConstr(
                y2[j, t] + quicksum(y3[i, j, t] for i in S if j in (P1 if i ==1 else P2)) + l[j, t] == l[j, t - 1] + demand[t, j - 3],
                name=f"Load_Balance_{j}_{t}"
            )
# 2. 中转站库存容量限制
for i in S:
    for t in range(timeInterval):
        model.addConstr(
            h[i, t] <= RentSize,
            name=f"Storage_Limit_{i}_{t}"
        )

# 3. y3 与 x 的车辆容量挂钩
for (i, j, t) in y3.keys():
    model.addConstr(
        y3[i, j, t] <= Q * x[i, j, t],
        name=f"Vehicle_Capacity_{i}_{j}_{t}"
    )

# 4. 动态库存平衡
for i in S:
    for t in range(timeInterval):
        if t == 0:
            model.addConstr(
                h[i, t] == y1[i, t] - quicksum(y3[i, j, t] for j in (P1 if i ==1 else P2)),
                name=f"Initial_Inventory_{i}_{t}"
            )
        else:
            model.addConstr(
                h[i, t] == h[i, t - 1] + y1[i, t] - quicksum(y3[i, j, t] for j in (P1 if i ==1 else P2)),
                name=f"Inventory_Balance_{i}_{t}"
            )

# 5. 未完成订单 l[j,t] 动态更新
for j in P:
    for t in range(timeInterval):
        if t == 0:
            model.addConstr(
                l[j, t] == demand[t, j - 3] - y2[j, t] - quicksum(y3[i, j, t] for i in S if j in (P1 if i ==1 else P2)),
                name=f"Initial_Load_{j}_{t}"
            )
        else:
            model.addConstr(
                l[j, t] == l[j, t - 1] + demand[t, j - 3] - y2[j, t] - quicksum(y3[i, j, t] for i in S if j in (P1 if i ==1 else P2)),
                name=f"Load_Balance_{j}_{t}"
            )

# 6. 客户服务约束：每个客户在每个时刻只能由一辆车服务
for j in P:
    for t in range(timeInterval):
        model.addConstr(
            quicksum(x[i, j, t] for i in S if j in (P1 if i ==1 else P2)) <= 1,
            name=f"One_Vehicle_Per_Customer_{j}_{t}"
        )

# 7. 车辆数量限制：中转站 i 每个时刻调度车辆 <= K[i -1]
for i in S:
    for t in range(timeInterval):
        model.addConstr(
            quicksum(x[i, j, t] for j in (P1 if i ==1 else P2)) <= K[i -1],
            name=f"Vehicle_Limit_{i}_{t}"
        )


# 8. 车辆可用性约束：k[i,t] 动态追踪可用车辆
for i in S:
    for t in range(timeInterval):
        if t ==0:
            model.addConstr(
                k[i, t] == K[i -1] - quicksum(x[i, j, t] for j in (P1 if i ==1 else P2)),
                name=f"Initial_Vehicle_Availability_{i}_{t}"
            )
        else:
            model.addConstr(
                k[i, t] == k[i, t -1] + quicksum(x[i, j, t -1] for j in (P1 if i ==1 else P2)) - \
                            quicksum(x[i, j, t] for j in (P1 if i ==1 else P2)),
                name=f"Vehicle_Availability_{i}_{t}"
            )


# ====================
# 求解模型
# ====================
model.setParam('OutputFlag', 1)  # 启用详细日志以便调试
model.optimize()

# ====================
# 输出结果
# ====================
if model.status == GRB.OPTIMAL:
    print(f"Optimal cost: {model.objVal}\n")

    # 打印 y1, y2, y3, h, l, li, k, x 变量
    print("\n--- y1 (Warehouse to Station) ---")
    for v in model.getVars():
        if v.varName.startswith('y1') and v.x > 1e-6:
            print(f"{v.varName}: {v.x}")

    print("\n--- y2 (Warehouse to Customer) ---")
    for v in model.getVars():
        if v.varName.startswith('y2') and v.x > 1e-6:
            print(f"{v.varName}: {v.x}")

    print("\n--- y3 (Station to Customer) ---")
    for v in model.getVars():
        if v.varName.startswith('y3') and v.x > 1e-6:
            print(f"{v.varName}: {v.x}")

    print("\n--- h (Inventory at Stations) ---")
    for v in model.getVars():
        if v.varName.startswith('h') and v.x > 1e-6:
            print(f"{v.varName}: {v.x}")

    print("\n--- l (Unfulfilled Orders at Customers) ---")
    for v in model.getVars():
        if v.varName.startswith('l') and v.x > 1e-6:
            print(f"{v.varName}: {v.x}")

    print("\n--- li (Remaining Load at Customers) ---")
    for v in model.getVars():
        if v.varName.startswith('li') and v.x > 1e-6:
            print(f"{v.varName}: {v.x}")

    print("\n--- k (Available Vehicles at Stations) ---")
    for v in model.getVars():
        if v.varName.startswith('k') and v.x > 1e-6:
            print(f"{v.varName}: {v.x}")

    print("\n--- x (Vehicle Dispatch) ---")
    for v in model.getVars():
        if v.varName.startswith('x') and v.x > 0.5:
            print(f"{v.varName}: {v.x}")
else:
    print("No optimal solution found.")

# ====================
# 结果可视化
# ====================
if model.status == GRB.OPTIMAL:
    # 从模型中提取变量值
    y1_values = {key: y1[key].x for key in y1.keys()}
    y2_values = {key: y2[key].x for key in y2.keys()}
    y3_values = {key: y3[key].x for key in y3.keys()}
    h_values = {key: h[key].x for key in h.keys()}
    l_values = {key: l[key].x for key in l.keys()}
    li_values = {key: li[key].x for key in li.keys()}
    k_values = {key: k[key].x for key in k.keys()}
    x_values = {(i, j, t): x[i, j, t].x
                for (i, j, t) in x.keys()
                if x[i, j, t].x > 0.5}

    # 打印非零的 y3 值
    print("\n--- Non-zero y3 (Station to Customer) ---")
    for (i, j, t), val in y3_values.items():
        if val > 1e-6:
            print(f"y3[{i},{j},{t}]: {val}")

    # 打印非零的 x 值
    print("\n--- Non-zero x (Vehicle Dispatch) ---")
    for (i, j, t), val in x_values.items():
        print(f"x[{i},{j},{t}]: {val}")

    # 图 1: 中转站库存量变化趋势
    plt.figure(figsize=(10, 6))
    for i in S:
        inventory = [h_values.get((i, t), 0) for t in range(timeInterval)]
        plt.plot(range(timeInterval), inventory, label=f"Station {i}")
    plt.title("Inventory Levels in Transfer Stations")
    plt.xlabel("Time Period")
    plt.ylabel("Inventory Level")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 图 2: 工厂到中转站的货物流量
    plt.figure(figsize=(10, 6))
    for i in S:
        flow = [y1_values.get((i, t), 0) for t in range(timeInterval)]
        plt.plot(range(timeInterval), flow, label=f"Warehouse to Station {i}")
    plt.title("Flow from Warehouse to Transfer Stations")
    plt.xlabel("Time Period")
    plt.ylabel("Flow Volume")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 图 3: 工厂到客户的货物流量
    plt.figure(figsize=(12, 8))
    for j in P:
        flow = [y2_values.get((j, t), 0) for t in range(timeInterval)]
        if any(flow):
            plt.plot(range(timeInterval), flow, label=f"Warehouse to Customer {j}")
    plt.title("Flow from Warehouse to Customers")
    plt.xlabel("Time Period")
    plt.ylabel("Flow Volume")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 图 4: 中转站到客户的货物流量
    plt.figure(figsize=(12, 8))
    for i in S:
        for j in (P1 if i ==1 else P2):
            flow = [y3_values.get((i, j, t), 0) for t in range(timeInterval)]
            if any(flow):  # 仅绘制有流量的路径
                plt.plot(range(timeInterval), flow, label=f"Station {i} to Customer {j}")
    plt.title("Flow from Transfer Stations to Customers")
    plt.xlabel("Time Period")
    plt.ylabel("Flow Volume")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small', ncol=2)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 图 5: 未完成订单量的动态变化
    plt.figure(figsize=(12, 8))
    for j in P:
        backlog = [l_values.get((j, t), 0) for t in range(timeInterval)]
        if any(backlog):
            plt.plot(range(timeInterval), backlog, label=f"Customer {j}")
    plt.title("Unfulfilled Orders Over Time")
    plt.xlabel("Time Period")
    plt.ylabel("Backlog Volume")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small', ncol=2)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 图 6: 中转站可用车辆数量变化趋势
    plt.figure(figsize=(10, 6))
    for i in S:
        vehicles = [k_values.get((i, t), 0) for t in range(timeInterval)]
        plt.plot(range(timeInterval), vehicles, label=f"Station {i}")
    plt.title("Available Vehicles at Transfer Stations")
    plt.xlabel("Time Period")
    plt.ylabel("Number of Vehicles")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 图 7: 车辆调度路径示意
    plt.figure(figsize=(12, 8))
    labels_added = set()
    for (i, j, t), val in x_values.items():
        # 仅添加每个 (i, j) 组合一次标签
        if (i, j) not in labels_added:
            plt.scatter(t, j, c='blue', marker='o', label=f"Dispatch from {i} to {j}")
            labels_added.add((i, j))
        else:
            plt.scatter(t, j, c='blue', marker='o')
    plt.title("Vehicle Dispatch from Stations to Customers Over Time")
    plt.xlabel("Time Period")
    plt.ylabel("Customer")
    if labels_added:
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
    plt.grid(True)
    plt.tight_layout()
    plt.show()
