num = [1,4,2];
den = conv([1,0,0,0],conv([1,0,4],[1,4,0]));
Gs = tf(num,den);
