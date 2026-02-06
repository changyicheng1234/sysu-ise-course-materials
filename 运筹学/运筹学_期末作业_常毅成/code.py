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

# 集合定义
warehouse = 0
transshipment_centers = [1, 10]  # 中转站编号
customers = [2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18]  # 客户编号
N_f = [warehouse]
N_s = transshipment_centers
N_p = customers
N = range(0,19)
T = range(timeInterval)  # 时间周期

# 客户到中转站的映射（假设每个中转站负责8个客户）
customer_groups = {
    1: list(range(2, 10)),    # 客户2-9
    10: list(range(11, 19))    # 客户11-18
}

# 创建节点编号到索引的映射
node_list = [0, 1, 10] + customers  # 按顺序排列所有节点
node_to_index = {node: idx for idx, node in enumerate(node_list)}  # 0:0, 1:1, 10:2, 2:3, ..., 18:18

# 更新 DispathCost 矩阵为 19x19
# 第一个对应仓库, 1和10对应中转站, 2-9和11-18对应客户
# 原始 DispathCost 是 18x18，需扩展为 19x19
# 这里假设节点18与其他节点的运输成本均为0，请根据实际情况调整
original_DispathCost = 10*np.array([
    [0, 11, 15, 13, 47, 2, 1, 2, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [14, 0, 8, 15, 37, 3, 14, 12, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0],   
    [17, 8, 0, 23, 36, 9, 18, 16, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [13, 15, 22, 0, 42, 16, 11, 12, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [47, 36, 37, 42, 0, 39, 47, 45, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [12, 2, 8, 16, 38, 0, 10, 8, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 12, 16, 11, 47, 9, 0, 2, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 9, 14, 12, 46, 7, 2, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [13, 10, 17, 7, 38, 11, 12, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 34, 30, 14, 8, 25, 25, 32 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 0, 21, 8, 40, 35, 5, 7, 30 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 34, 20, 0, 18, 48, 42, 15, 14, 15],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 8, 18, 0, 44, 38, 5, 5, 29 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0,14, 41, 48, 44, 0, 13, 40, 40, 43],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,8, 34, 42, 38, 13, 0, 34, 33, 40],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,25, 5, 16, 5, 39, 33, 0, 1, 25],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,25, 7, 15, 6, 39, 33, 2, 0, 24],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,31, 30, 16, 29, 43, 40, 25, 24]
])  # 18x18

# 扩展 DispathCost 至 19x19，添加节点18的行和列（暂时填充为0）
DispathCost_extended = np.zeros((19, 19))
DispathCost_extended[:18, :18] = original_DispathCost
# 如果有节点18的具体运输成本，请在这里填写
# 例如：
# DispathCost_extended[18, :] = [ ... ]  # 填写节点18到其他节点的运输成本
# DispathCost_extended[:, 18] = [ ... ]  # 填写其他节点到节点18的运输成本
# 目前暂时设为0
DispathCost = DispathCost_extended

TimeoutCost = 1000  # 客户i超时订单成本

# 运输时间定义
DispathT = np.ones((19, 19), dtype=int)  # 中转站和客户之间的运输时间，全部设为1
TravelT1 = np.array([1, 1])  # 工厂到中转站i的运输时间
TravelT2 = np.array([1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1, 2, 2, 1] * 2)  # 工厂到客户的运输时间

# 车辆及容量参数
Q = 100  # 车辆的最大容量
K = {1:6, 10:6}  # 中转站i的车辆总数量
Max1 = RentSize  # 记录工厂运输到中转站运货量的最大值
Max2 = 100  # 记录工厂运输到客户运货量的最大值
Max3 = Q  # 记录从中转站运输到客户运货量的最大值
M = 100000  # 条件约束的一个大数

# 订单需求 r_i^t 和未完成订单 l_i^t 的初始化
# 假设demand数组的第一维对应时间，第二维对应客户
# 初始化未完成订单 l_i_t 和新增订单 r_i_t
# 使用 N_p.index(i) 来正确映射客户到 demand 列
# 注意 node_to_index 中客户编号从 2 开始，对应 demand 列从 0 开始
r_i_t = {(i, t): demand[t, N_p.index(i)] for i in N_p for t in T}  # 时刻 t 客户 i 新增的订单需求量
l_i_t = {(i, t): 0 for i in N_p for t in T}  # 时刻 t 客户 i 累计的未完成订单

# 创建 Gurobi 模型
model = gp.Model("Transportation_Scheduling")

# 决策变量定义

# y1: 从仓库运输到中转站的货物量（通过火车）
y1 = model.addVars(N_s, T, vtype=GRB.CONTINUOUS, name="y1")

# y2: 从仓库直接运输到客户的货物量（通过货车）
y2 = model.addVars(N_p, T, vtype=GRB.CONTINUOUS, name="y2")

# y3: 从中转站运输到客户的货物量（通过货车）
y3 = model.addVars(N_p, T, vtype=GRB.CONTINUOUS, name="y3")

# x: 车辆路径，从中转站到客户的二进制变量
x = model.addVars(N_s, N_p, T, vtype=GRB.BINARY, name="x")

# k_i^t: 时刻 t 中转站 i 的实时存货量
k = model.addVars(N_s, T, vtype=GRB.CONTINUOUS, name="k")

# l_i^t: 时刻 t 客户 i 的未完成订单
l = model.addVars(N_p, T, vtype=GRB.CONTINUOUS, name="l")

# 目标函数
# 成本包括：
# 1. 中转站租赁成本
# 2. 中转站存货成本
# 3. 仓库到中转站运输成本（火车）
# 4. 仓库直接到客户运输成本（货车）
# 5. 车辆使用成本（货车从中转站到客户）
# 6. 客户需求的超时成本

# 1. 中转站租赁成本
rent_cost = quicksum(RentCost * RentSize for i in N_s for t in T)

# 2. 中转站存货成本
hoard_cost = quicksum(HoardCost * k[i, t] for i in N_s for t in T)

# 3. 仓库到中转站运输成本（火车）
transport_cost1 = quicksum(TravelCost1[N_s.index(i)] * y1[i, t]
                           for i in N_s for t in T)

# 4. 仓库直接到客户运输成本（货车）
transport_cost2 = quicksum(TravelCost2[N_p.index(j)] * y2[j, t]
                           for j in N_p for t in T)

# 5. 车辆使用成本（货车从中转站到客户）
# 使用 node_to_index 映射 i 和 j 到 DispathCost 的索引
vehicle_transport_cost = quicksum(
    DispathCost[node_to_index[i], node_to_index[j]] * x[i, j, t]
    for i in N_s for j in customer_groups[i] for t in T
)

# 6. 客户需求的超时成本
timeout_cost = quicksum(TimeoutCost * l[j, t] for j in N_p for t in T)

# 目标函数为总成本的负数（因为要最大化负成本即最小化成本）
model.setObjective(
    -(rent_cost +
      hoard_cost +
      transport_cost1 +
      transport_cost2 +
      vehicle_transport_cost +
      timeout_cost),
    GRB.MAXIMIZE
)

# 约束条件

# 1. 初始化约束
# 初始时刻所有中转站库存为0
for i in N_s:
    model.addConstr(k[i, 0] == 0, f"Initial_Inventory_{i}")

# 2. 车辆路径约束

# 2.1 每个中转站在每个时间段最多派出K[i]辆车
for i in N_s:
    for t in T:
        model.addConstr(
            quicksum(x[i, j, t] for j in customer_groups[i]) <= K[i],
            f"Vehicle_Limit_{i}_{t}"
        )

# 2.2 每个客户在每个时间段最多被一辆车服务
for j in N_p:
    for t in T:
        model.addConstr(
            quicksum(x[i, j, t] for i in N_s) <= 1,
            f"One_Vehicle_Per_Customer_{j}_{t}"
        )

# 3. 货物量约束

# 3.1 中转站库存不超过租赁容积
for i in N_s:
    for t in T:
        model.addConstr(
            k[i, t] <= RentSize,
            f"Inventory_Capacity_{i}_{t}"
        )

# 3.2 客户需求满足
for j in N_p:
    for t in T:
        model.addConstr(
            y2[j, t] + y3[j, t] + l[j, t] >= r_i_t[j, t],
            f"Demand_Constraint_{j}_{t}"
        )

# 3.3 车辆容量限制
for i in N_s:
    for j in customer_groups[i]:
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
                k[i, t + 1] == k[i, t] + y1[i, t] - quicksum(y3[j, t] for j in customer_groups[i]),
                f"Inventory_Update_{i}_{t}"
            )
    for j in N_p:
        if t < timeInterval - 1:
            # 未完成订单更新
            model.addConstr(
                l[j, t + 1] == l[j, t] + r_i_t[j, t] - y2[j, t] - y3[j, t],
                f"Unmet_Order_Update_{j}_{t}"
            )

# 5. 车辆路径与运输货物的关联约束

for i in N_s:
    for j in customer_groups[i]:
        for t in T:
            # 如果有车辆从i到j，y3[j,t]可以大于0
            # 如果没有车辆从i到j，y3[j,t]必须为0
            model.addConstr(
                y3[j, t] <= Q * x[i, j, t],
                f"Y3_Capacity_Link_{i}_{j}_{t}"
            )

# 6. 确保车辆返回中转站
# 由于车辆路径的时间连续性较复杂，这里暂时简化为不强制返回
# 若需要，可以添加车辆路径的流平衡约束

# 7. 优化模型参数
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
    print("\n从仓库到客户的运输量 y2:")
    for j in N_p:
        for t in T:
            if y2[j, t].X > 0:
                print(f"客户 {j}, 时间 {t}: {y2[j, t].X}")
    
    # y3: 从中转站到客户的运输量
    print("\n从中转站到客户的运输量 y3:")
    for j in N_p:
        for t in T:
            if y3[j, t].X > 0:
                print(f"客户 {j}, 时间 {t}: {y3[j, t].X}")
    
    # x: 车辆路径
    print("\n车辆路径 x:")
    for i in N_s:
        for j in customer_groups[i]:
            for t in T:
                if x[i, j, t].X > 0.5:  # 二进制变量，使用0.5作为阈值
                    print(f"时间 {t}: 从 中转站 {i} 到 客户 {j} 有车辆移动")
    
    # k: 中转站库存
    print("\n中转站库存 k:")
    for i in N_s:
        for t in T:
            if k[i, t].X > 0:
                print(f"中转站 {i}, 时间 {t}: {k[i, t].X}")
    
    # l: 客户未完成订单
    print("\n客户未完成订单 l:")
    for j in N_p:
        for t in T:
            if l[j, t].X > 0:
                print(f"客户 {j}, 时间 {t}: {l[j, t].X}")
else:
    print("未找到最优解。")
import matplotlib.pyplot as plt
import networkx as nx

# 可视化车辆路径（使用networkx图形显示中转站和客户的路径）
def plot_vehicle_paths():
    G = nx.DiGraph()

    # 添加节点
    for i in N_s:
        G.add_node(i, label=f"中转站 {i}")
    for j in N_p:
        G.add_node(j, label=f"客户 {j}")

    # 添加边：根据车辆路径的决策变量x进行添加
    for i in N_s:
        for j in customer_groups[i]:
            for t in T:
                if x[i, j, t].X > 0.5:  # 如果x[i,j,t]为1，表示有车辆在运行
                    G.add_edge(i, j, weight=DispathCost[node_to_index[i], node_to_index[j]])

    # 绘制图形
    pos = nx.spring_layout(G, seed=42)  # 布局
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2, alpha=0.5, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
    plt.title('车辆路径从中转站到客户')
    plt.axis('off')  # 不显示坐标轴
    plt.show()

# 调用可视化函数
import matplotlib.pyplot as plt
import numpy as np

# 可视化仓库到客户的运输量（展示每个时间段和每个客户的运输量）
def plot_transportation_from_warehouse_to_customers():
    fig, ax = plt.subplots(figsize=(10, 6))

    # 创建一个矩阵，用于绘制每个客户在不同时间段的运输量
    transport_matrix = np.zeros((len(N_p), len(T)))

    # 填充运输量数据
    for j in N_p:
        for t in T:
            transport_matrix[N_p.index(j), t] = y2[j, t].X

    # 使用热力图显示仓库到客户的运输量
    cax = ax.imshow(transport_matrix, cmap='YlGnBu', interpolation='nearest')

    ax.set_xticks(np.arange(len(T)))
    ax.set_xticklabels([f"t{t}" for t in T])  # 时间段标签
    ax.set_yticks(np.arange(len(N_p)))
    ax.set_yticklabels(N_p)  # 客户标签

    ax.set_xlabel('时间段')
    ax.set_ylabel('客户')
    ax.set_title('仓库到客户的运输量')

    plt.colorbar(cax)  # 显示热力图的颜色条
    plt.show()

# 可视化每个客户的运输量变化（折线图）
def plot_individual_customer_transportation():
    fig, ax = plt.subplots(figsize=(10, 6))

    # 为每个客户绘制折线图，展示每个时间段的运输量
    for j in N_p:
        transportation = [y2[j, t].X for t in T]
        ax.plot(T, transportation, label=f'客户 {j}', marker='o')

    ax.set_xlabel('时间段')
    ax.set_ylabel('运输量')
    ax.set_title('每个客户的运输量变化')
    ax.legend()
    plt.grid(True)
    plt.show()

# 可视化仓库到客户的运输网络（每条边的宽度代表运输量）
def plot_transportation_network_from_warehouse_to_customers():
    import networkx as nx

    G = nx.DiGraph()  # 创建一个有向图

    # 添加节点：仓库（0）和所有客户
    G.add_node(0, label="仓库")
    for j in N_p:
        G.add_node(j, label=f"客户 {j}")

    # 添加边：根据决策变量y2表示仓库到客户的运输量
    for j in N_p:
        for t in T:
            if y2[j, t].X > 0:
                G.add_edge(0, j, weight=y2[j, t].X)  # 边的权重即为运输量

    # 绘制图形：用边的权重（运输量）来调整宽度
    pos = nx.spring_layout(G, seed=42)  # 选择布局

    plt.figure(figsize=(10, 6))
    edge_widths = [G[u][v]['weight'] for u, v in G.edges()]  # 获取边的权重
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.6, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
    
    plt.title('仓库到客户的运输网络（按运输量显示）')
    plt.axis('off')  # 不显示坐标轴
    plt.show()

# 调用可视化函数
plot_transportation_from_warehouse_to_customers()
plot_individual_customer_transportation()
plot_transportation_network_from_warehouse_to_customers()

plot_vehicle_paths()

