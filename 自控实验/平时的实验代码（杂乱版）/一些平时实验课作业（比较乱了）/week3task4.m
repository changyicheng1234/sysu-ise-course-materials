num = [1 1];
den = [1 1 1];
G = tf(num,den);
u = heaviside(t) + t .* heaviside(t);
t = [0:0.1:20];
lsim(G,u,t),hold on,plot(t,u,'r');
grid on;