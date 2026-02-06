num = [1,5,6];
den = [1,2,1,0];
[z,p,k] = tf2zp(num,den);
sys = zpk(z,p,k)