z = [-1 -2]';
p = [0 -5 -6 -3];
k = 8;
[num,den] = zp2tf(z,p,k)
G = tf(num,den)