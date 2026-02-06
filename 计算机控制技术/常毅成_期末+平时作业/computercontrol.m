%% 基于状态空间的线性系统状态反馈与观测器协同设计仿真
% 对应报告题目：《基于状态空间的线性系统状态反馈与观测器协同设计及仿真研究》
clear; clc; close all;

%% 1. 系统建模 (System Modeling)
% 建立一个三阶不稳定/或典型的线性系统模型
% A矩阵选择：标准型，易于分析
A = [0   1   0;
     0   0   1;
     -6 -11 -6]; % 开环极点在 -1, -2, -3 (稳定但动态性能可能不满足要求)
     % 如果想要更明显的控制效果，可以改得稍微不稳定，但这个经典模型足够说明问题
     
B = [0; 0; 1];
C = [1 0 0];
D = 0;

% 检查可控性和可观测性
Co = ctrb(A,B);
Ob = obsv(A,C);

if rank(Co) < length(A) || rank(Ob) < length(A)
    error('系统不可控或不可观测，无法进行设计');
else
    disp('系统完全可控且完全可观测。');
end

%% 2. 状态反馈控制器设计 (Controller Design)
% 目标：配置闭环极点，使系统响应更快，阻尼合适
% 期望极点：设计一对共轭复根增加阻尼，一个实根远离虚轴
P_des = [-2; -2+2i; -2-2i]; 

% 使用Ackermann公式或place函数计算反馈增益 K
K = place(A, B, P_des);
fprintf('状态反馈增益矩阵 K = [%f, %f, %f]\n', K(1), K(2), K(3));

%% 3. 状态观测器设计 (Observer Design)
% 目标：观测器极点应位于控制器极点的左侧（快2-5倍）
P_obs = [-10; -10.1; -10.2]; % 稍微错开一点点

% 计算观测器增益 L (注意place是对偶形式: A' 和 C')
L_t = place(A', C', P_obs);
L = L_t';
fprintf('观测器增益矩阵 L = [%f; %f; %f]\n', L(1), L(2), L(3));

%% 4. 协同仿真模型构建 (Simulation Setup)
% 基于观测器的状态反馈系统可以写成增强的状态空间形式
% 状态变量为 [x; e]，其中 e = x - x_hat
% 动态方程:
% [dx/dt]   [A-BK  BK   ] [x]
% [     ] = [           ] [ ]
% [de/dt]   [0     A-LC ] [e]

% 定义复合系统矩阵
Big_A = [A - B*K,  B*K; 
         zeros(3), A - L*C];
     
% 定义初始条件
% 假设系统初始状态 x0 不为零（受到了扰动）
x0 = [1; -1; 0.5]; 
% 假设观测器初始状态 x_hat0 为零（因为初始不知道状态）
x_hat0 = [0; 0; 0];
% 误差初始值 e0 = x0 - x_hat0
e0 = x0 - x_hat0;

% 复合系统的初始状态
X0_aug = [x0; e0];

% 仿真时间
t = 0:0.01:5;

% 系统自由响应（也就是调节器问题，目标是回到零点）
[y_aug, t, x_aug] = initial(ss(Big_A, [], eye(6), []), X0_aug, t);

% 提取数据
x_real = x_aug(:, 1:3);      % 真实状态
e_sim  = x_aug(:, 4:6);      % 估计误差
x_est  = x_real - e_sim;     % 估计状态 (x_hat = x - e)
u_ctrl = -K * x_est';        % 控制输入 u = -K * x_hat

%% 5. 绘图与结果分析 (Plotting)
% 修复了字符解释器报错的问题，去掉了不兼容的 latex 指令

% 设置绘图通用参数
set(0,'DefaultAxesFontSize', 12); % 字体稍微大一点，报告里好看

% --- 图1：状态对比 ---
figure('Name', '系统状态响应对比', 'Color', 'w');

subplot(3,1,1);
plot(t, x_real(:,1), 'b', 'LineWidth', 1.5); hold on;
plot(t, x_est(:,1), 'r--', 'LineWidth', 1.5);
title('状态 x_1 与 估计值 x_{est1} 对比'); % 用 x_{est} 代替 \hat
ylabel('幅值');
legend('真实值 x_1', '估计值 x_{est1}', 'Location', 'Best'); grid on;

subplot(3,1,2);
plot(t, x_real(:,2), 'b', 'LineWidth', 1.5); hold on;
plot(t, x_est(:,2), 'r--', 'LineWidth', 1.5);
title('状态 x_2 与 估计值 x_{est2} 对比');
ylabel('幅值');
legend('真实值 x_2', '估计值 x_{est2}', 'Location', 'Best'); grid on;

subplot(3,1,3);
plot(t, x_real(:,3), 'b', 'LineWidth', 1.5); hold on;
plot(t, x_est(:,3), 'r--', 'LineWidth', 1.5);
title('状态 x_3 与 估计值 x_{est3} 对比');
xlabel('时间 (s)'); ylabel('幅值');
legend('真实值 x_3', '估计值 x_{est3}', 'Location', 'Best'); grid on;

% --- 图2：误差收敛 ---
figure('Name', '观测误差收敛曲线', 'Color', 'w');
plot(t, e_sim, 'LineWidth', 1.5);
title('观测器估计误差 e(t) 收敛过程');
xlabel('时间 (s)'); ylabel('误差幅值');
legend('e_1', 'e_2', 'e_3'); grid on;

% --- 图3：控制输入 ---
figure('Name', '控制输入信号', 'Color', 'w');
plot(t, u_ctrl, 'k', 'LineWidth', 1.5);
title('控制输入 u(t)');
xlabel('时间 (s)'); ylabel('电压/输入量'); grid on;