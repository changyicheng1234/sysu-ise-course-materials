% 假设result1.Time和result1.Data已经是你的数据
% 找到峰值
[peakValue, peakIndex] = max(result1.Data);
% 找到稳态值，这里我们取最后100个数据点的平均值作为稳态值
steadyStateValue = mean(result1.Data(end-100:end));
% 计算超调量
overshoot = (peakValue - steadyStateValue) / steadyStateValue * 100;

% 计算调节时间
if steadyStateValue == 0
    settlingTime = result1.Time(end) - result1.Time(1); % 如果稳态值为0，则调节时间为整个时间跨度
else
    % 计算调节时间，这里我们假设系统在峰值之后5%以内稳定
    tolerance = 0.05 * steadyStateValue;
    settlingTimeIndex = find(abs(result1.Data - steadyStateValue) >= tolerance, 1, 'last');
    if isempty(settlingTimeIndex)
        settlingTime = NaN; % 如果没有找到满足条件的点，则设置为NaN
    else
        settlingTime = result1.Time(settlingTimeIndex) - result1.Time(1);
    end
end

% 计算上升时间
riseTimeIndex10 = find(result1.Data >= 0.1 * steadyStateValue, 1, 'first');
riseTimeIndex90 = find(result1.Data >= 0.9 * steadyStateValue, 1, 'first');
if isempty(riseTimeIndex10) || isempty(riseTimeIndex90)
    riseTime = NaN; % 如果没有找到满足条件的点，则设置为NaN
else
    riseTime = result1.Time(riseTimeIndex90) - result1.Time(riseTimeIndex10);
end

% 绘制图形
figure;
plot(result1.Time, result1.Data, 'b-', 'LineWidth', 2);
hold on;
plot(result1.Time(peakIndex), peakValue, 'ro'); % 标记峰值
if ~isnan(settlingTime)
    plot(result1.Time(settlingTimeIndex), result1.Data(settlingTimeIndex), 'go'); % 标记调节时间的结束点
end
if ~isnan(riseTimeIndex10)
    plot(result1.Time(riseTimeIndex10), result1.Data(riseTimeIndex10), 'kx'); % 标记10%上升点
    plot(result1.Time(riseTimeIndex90), result1.Data(riseTimeIndex90), 'kx'); % 标记90%上升点
end
xlabel('Time (s)');
ylabel('Response');
title('PID Response with Overshoot, Settling Time, and Rise Time');
legend('Response', 'Peak', 'Settling Time', '10% Rise Time', '90% Rise Time');
grid on;

% 标注超调量、调节时间和上升时间
if ~isnan(settlingTime)
    annotation('textbox', [0.15, 0.7, 0.1, 0.1], 'String', sprintf('Overshoot: %.2f%%', overshoot), 'EdgeColor', 'none');
    annotation('textbox', [0.15, 0.6, 0.1, 0.1], 'String', sprintf('Settling Time: %.2fs', settlingTime), 'EdgeColor', 'none');
    annotation('textbox', [0.15, 0.5, 0.1, 0.1], 'String', sprintf('Rise Time: %.2fs', riseTime), 'EdgeColor', 'none');
else
    annotation('textbox', [0.15, 0.7, 0.1, 0.1], 'String', sprintf('Overshoot: %.2f%%', overshoot), 'EdgeColor', 'none');
    annotation('textbox', [0.15, 0.6, 0.1, 0.1], 'String', 'Settling Time: N/A', 'EdgeColor', 'none');
    annotation('textbox', [0.15, 0.5, 0.1, 0.1], 'String', 'Rise Time: N/A', 'EdgeColor', 'none');
end





% 假设result2.Time和result2.Data已经是你的数据
% 找到峰值
[peakValue, peakIndex] = max(result2.Data);
% 找到稳态值，这里我们取最后100个数据点的平均值作为稳态值
steadyStateValue = mean(result2.Data(end-100:end));
% 计算超调量
overshoot = (peakValue - steadyStateValue) / steadyStateValue * 100;

% 计算调节时间
if steadyStateValue == 0
    settlingTime = result2.Time(end) - result2.Time(1); % 如果稳态值为0，则调节时间为整个时间跨度
else
    % 计算调节时间，这里我们假设系统在峰值之后5%以内稳定
    tolerance = 0.05 * steadyStateValue;
    settlingTimeIndex = find(abs(result2.Data - steadyStateValue) >= tolerance, 1, 'last');
    if isempty(settlingTimeIndex)
        settlingTime = NaN; % 如果没有找到满足条件的点，则设置为NaN
    else
        settlingTime = result2.Time(settlingTimeIndex) - result2.Time(1);
    end
end

% 计算上升时间
riseTimeIndex10 = find(result2.Data >= 0.1 * steadyStateValue, 1, 'first');
riseTimeIndex90 = find(result2.Data >= 0.9 * steadyStateValue, 1, 'first');
if isempty(riseTimeIndex10) || isempty(riseTimeIndex90)
    riseTime = NaN; % 如果没有找到满足条件的点，则设置为NaN
else
    riseTime = result2.Time(riseTimeIndex90) - result2.Time(riseTimeIndex10);
end

% 绘制图形
figure;
plot(result2.Time, result2.Data, 'b-', 'LineWidth', 2);
hold on;
plot(result2.Time(peakIndex), peakValue, 'ro'); % 标记峰值
if ~isnan(settlingTime)
    plot(result2.Time(settlingTimeIndex), result2.Data(settlingTimeIndex), 'go'); % 标记调节时间的结束点
end
if ~isnan(riseTimeIndex10)
    plot(result2.Time(riseTimeIndex10), result2.Data(riseTimeIndex10), 'kx'); % 标记10%上升点
    plot(result2.Time(riseTimeIndex90), result2.Data(riseTimeIndex90), 'kx'); % 标记90%上升点
end
xlabel('Time (s)');
ylabel('Response');
title('PID Response with Overshoot, Settling Time, and Rise Time');
legend('Response', 'Peak', 'Settling Time', '10% Rise Time', '90% Rise Time');
grid on;

% 标注超调量、调节时间和上升时间
if ~isnan(settlingTime)
    annotation('textbox', [0.15, 0.7, 0.1, 0.1], 'String', sprintf('Overshoot: %.2f%%', overshoot), 'EdgeColor', 'none');
    annotation('textbox', [0.15, 0.6, 0.1, 0.1], 'String', sprintf('Settling Time: %.2fs', settlingTime), 'EdgeColor', 'none');
    annotation('textbox', [0.15, 0.5, 0.1, 0.1], 'String', sprintf('Rise Time: %.2fs', riseTime), 'EdgeColor', 'none');
else
    annotation('textbox', [0.15, 0.7, 0.1, 0.1], 'String', sprintf('Overshoot: %.2f%%', overshoot), 'EdgeColor', 'none');
    annotation('textbox', [0.15, 0.6, 0.1, 0.1], 'String', 'Settling Time: N/A', 'EdgeColor', 'none');
    annotation('textbox', [0.15, 0.5, 0.1, 0.1], 'String', 'Rise Time: N/A', 'EdgeColor', 'none');
end



% 假设result1.Time和result1.Data已经是你的数据
% 找到峰值
[peakValue, peakIndex] = max(result3.Data);
% 找到稳态值，这里我们取最后100个数据点的平均值作为稳态值
steadyStateValue = mean(result3.Data(end-100:end));
% 计算超调量
overshoot = (peakValue - steadyStateValue) / steadyStateValue * 100;

% 计算调节时间，这里我们假设系统在峰值之后5%以内稳定
tolerance = 0.05 * steadyStateValue;
settlingTimeIndex = find(abs(result3.Data - steadyStateValue) >= tolerance, 1, 'last');
if tolerance == 0
    settlingTime = NaN; % 如果没有找到满足条件的点，则设置为NaN
else
    settlingTime = result3.Time(settlingTimeIndex) - result3.Time(1);
end

% 计算上升时间
riseTimeIndex10 = find(result3.Data >= 0.1 * steadyStateValue, 1, 'first');
riseTimeIndex90 = find(result3.Data >= 0.9 * steadyStateValue, 1, 'first');
if isempty(riseTimeIndex10) || isempty(riseTimeIndex90)
    riseTime = NaN; % 如果没有找到满足条件的点，则设置为NaN
else
    riseTime = result3.Time(riseTimeIndex90) - result3.Time(riseTimeIndex10);
end

% 绘制图形
figure;
plot(result3.Time, result3.Data, 'b-', 'LineWidth', 2);
hold on;
plot(result3.Time(peakIndex), peakValue, 'ro'); % 标记峰值
if ~isnan(settlingTimeIndex)
    plot(result3.Time(settlingTimeIndex), result3.Data(settlingTimeIndex), 'go'); % 标记调节时间的结束点
end
if ~isnan(riseTimeIndex10)
    plot(result3.Time(riseTimeIndex10), result3.Data(riseTimeIndex10), 'kx'); % 标记10%上升点
    plot(result3.Time(riseTimeIndex90), result3.Data(riseTimeIndex90), 'kx'); % 标记90%上升点
end
xlabel('Time (s)');
ylabel('Response');
title('PID Response with Overshoot, Settling Time, and Rise Time');
legend('Response', 'Peak', 'Settling Time', '10% Rise Time', '90% Rise Time');
grid on;

% 标注超调量、调节时间和上升时间
if ~isnan(settlingTime)
    annotation('textbox', [0.15, 0.7, 0.1, 0.1], 'String', sprintf('Overshoot: %.2f%%', overshoot), 'EdgeColor', 'none');
    annotation('textbox', [0.15, 0.6, 0.1, 0.1], 'String', sprintf('Settling Time: %.2fs', settlingTime), 'EdgeColor', 'none');
    annotation('textbox', [0.15, 0.5, 0.1, 0.1], 'String', sprintf('Rise Time: %.2fs', riseTime), 'EdgeColor', 'none');
else
    annotation('textbox', [0.15, 0.7, 0.1, 0.1], 'String', sprintf('Overshoot: %.2f%%', overshoot), 'EdgeColor', 'none');
    annotation('textbox', [0.15, 0.6, 0.1, 0.1], 'String', 'Settling Time: N/A', 'EdgeColor', 'none');
    annotation('textbox', [0.15, 0.5, 0.1, 0.1], 'String', 'Rise Time: N/A', 'EdgeColor', 'none');
end




