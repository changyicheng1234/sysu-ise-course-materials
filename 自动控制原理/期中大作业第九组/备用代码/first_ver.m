clc;clear all;
% 被控量——平均动脉压
%%
syms t s;
y_t = t*exp(-2*t);  % 模型的脉冲响应
G_s = laplace(y_t,t,s);  %对应脉冲响应的传递函数模型
H_s = 1;      % 传感器的传递函数,假设无测量噪声
Gp_s = 1/s;   % 泵的传递函数

% 定义Gc_s 
syms K_P K_I K_D;  % 定义比例增益、积分增益、微分增益
K_I = subs(K_I,0);K_P = subs(K_P,0.1);K_D = subs(K_D,0.1);
Gc_s = K_P+K_I/s+K_D*s; 

%%
% 取N(S)=0,Td(s)=0,分别基于PD，PI控制器对系统进行Matlab仿真
s = subs(s,0:0.01:20);
% s = 0:0.01:20; % 以100Hz的频率进行采样
R_s = 96;   % 期望输出的MAP为96mmHg
% PD控制器

%K_I = 0;
%K_P = 0.1;k_D = 0.1;
K_s = H_s+1/(Gc_s*Gp_s*G_s);
Y_s = R_s/K_s;
Y_t = ilaplace(Y_s,t);
t = 0:0.1:5;
RES=eval(Y_t);
% plot(RES,t);
% grid on
% plot(Y_s,s)
%% 无噪声






