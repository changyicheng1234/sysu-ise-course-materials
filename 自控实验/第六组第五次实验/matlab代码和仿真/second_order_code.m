t_step = 1e-6;
freq = 150;
omega = 2 .* pi .* freq;
sim("second_order_sim.slx", TimeOut, 10);
uom = max(out.uom.Data);
uim = max(out.uim.Data);
db = 20 .* log10(uom ./ uim);
% phi = rad2deg(abs(find(out.uom.Data == uom, 1) - find(out.uim.Data == uim, 1))...
%     .* t_step .* omega);
phi = rad2deg(abs(0.015 - 0.019) .* t_step .* omega);
%%
Gs = tf([500], [1 10 500]);
bode(Gs)