DB1 = 20.*log10(max(out.uo)./1);
Uom = max(out.uo);
peak_time_diff = 5.2e-04; % 峰值时间差
period = 1/300; % 假设周期为1，单位与峰值时间差相同

% 计算相位差，单位是角度
phase_diff_deg = (peak_time_diff / period) * 360;
