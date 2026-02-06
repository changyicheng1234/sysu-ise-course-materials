%%
num=[1043.19];
den=[1 0 -623.956];
p=roots(den)
figure();
bode(num,den);
grid;



%%
omega = 75;
alpha = (1 - sind(omega)) ./ (1 + sind(omega));
syms w
equ = abs(1043.19*2.989752/(-w^2-623.956))-sqrt(alpha) == 0;
w = solve(equ, w);
w = double(w(find(w>0)));
T = 1 ./ w ./ sqrt(alpha);
K = 2.989752;
Kc = K ./ alpha;
num = conv(Kc, [1, 1./T]);
den = [1, 1./alpha./T];
[z,p,k] = tf2zpk(num, den)
num = conv(Kc, conv([1, 1./T], 1043.19));
den = conv([1, 1./alpha./T], [1, 0, -623.956]);
Gs = tf(num, den);
figure(1);
bode(Gs);
grid on;
figure(2);
step(feedback(Gs, 1));


