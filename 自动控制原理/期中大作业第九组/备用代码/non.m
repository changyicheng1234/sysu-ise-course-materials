%%    画图
time = out.ScopeData.time;
y_value = 96*ones(size(time));
value = out.ScopeData.signals.values;
steadyStatevalue = mean(value(end-10:end)); % 确定实际稳态值
plot(time,y_value,'r');
hold on;
plot(time, value,'b');
xlabel("Time(sec)")
ylabel("MAP(mmHg)")
title("Mean arterial pressure(MAP) disturbance step response")
grid on;

%   计算动态误差和稳态误差
% 超调量 和 峰值时间
y_value_max = max(value);
y_mean = steadyStatevalue;
percentOvershoot = 0;
index = 0;
if y_value_max > y_mean
    percentOvershoot = (y_value_max-y_mean)/y_mean;
end
disp(['超调量', num2str(percentOvershoot)]);

% %% 延迟时间，第一次到达终值时
% for i = 1:size(time)
%     if abs(value(i)-steadyStatevalue*0.5)<0.1
%         break
%     end
% end
% td = time(i);
% disp(['延迟时间', num2str(td)]);
% 稳态误差;
steadyStatevalue = mean(value(end-10:end)); % 确定稳态值
e_ss = abs(steadyStatevalue-96);
disp(['稳态误差', num2str(e_ss)]);

%
info = stepinfo(value,time);
disp(info)

% %% 调节时间
% steadyStatevalue = mean(value(end-10:end)); % 确定稳态值
% % 找到首个超过稳态值的时间点
% riseTimeStartIdx = find(value > steadyStateValue, 1);
% 
% % 找到最后一个超过稳态值的时间点
% riseTimeEndIdx = find(value > steadyStateValue, 1, 'last');
% 
% % 计算调节时间
% risetime = time(riseTimeEndIdx)-time(riseTimeStartIdx);
% disp(['调节时间：', num2str(risetime)]);







