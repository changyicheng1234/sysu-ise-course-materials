z = [-1+1i,-1-1i]';
p = [0,0,-5,-1,1];
k = 8;
[num,den] = zp2tf(z,p,k);
[r,p,k] = residue(num,den);
syms s;
