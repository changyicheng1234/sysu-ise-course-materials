Xd = [0 0 1 0.5;0 1 0 0;-1 0 0 0.5;0 0 0 1];
Xdnext = [0 0 1 0.6;0 1 0 0;-1 0 0 0.3;0 0 0 1];
X = [0.17 0 0.985 0.387;0 1 0 0;-0.985 0 0.17 0.57;0 0 0 1];
Kp = eye(6);
Ki = eye(6);
dt = 0.01;
thetalist = [0;  0;  0.2; -1.6;  0];%可修改
[Vd,AdXinvXdVd,V,Xerr,control] = FeedbackControl(X,Xd,Xdnext,Kp,Ki,dt,thetalist);
