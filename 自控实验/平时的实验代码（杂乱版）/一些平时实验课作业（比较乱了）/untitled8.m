num = [1 0 0 0];
den = [1 3];
[r,p,k] = residue(num,den)
syms s
Gs = -27/(s+3)+s^2-3.*s+9