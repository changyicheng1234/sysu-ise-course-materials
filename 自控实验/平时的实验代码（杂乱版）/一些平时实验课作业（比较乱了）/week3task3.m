num = 100;
den = [1 3 0];
sys = tf(num,den);
sysc = feedback(sys,1);
step(sysc);
