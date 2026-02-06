function [result_traj,result_conf,result_Xerr] = Main_function(Tscfinal)
%UNTITLED6 此处显示有关此函数的摘要
%   此处显示详细说明
Tseinitial = [0 0 1 0.5518;0 1 0 0; -1 0 0 0.4012 ; 0 0 0 1];
Tscinitial = [1 0 0 1;0 1 0 0;0 0 1 0.025;0 0 0 1];

Tcegrasp = [cos(3*pi/4) 0 sin(3*pi/4) 0.005; 0 1 0 0;-sin(3*pi/4) 0 cos(3*pi/4) -0.005;0 0 0 1];
Tcestandoff = Tcegrasp;
Tcestandoff(3,4) = 0.05;
k = 700;
result_traj = TrajectoryGenerator(Tseinitial,Tscinitial,Tscfinal,...
    Tcegrasp,Tcestandoff,k);

result_traj = readmatrix('traj_csv_file.csv');
[rows, cols] = size(result_traj);
N = rows;
max_speed = 5;

Xd = [result_traj(1,1) result_traj(1,2) result_traj(1,3) result_traj(1,10); 
result_traj(1,4) result_traj(1,5) result_traj(1,6) result_traj(1,11); 
result_traj(1,7) result_traj(1,8) result_traj(1,9) result_traj(1,12); 
  0                0                0                1]; 


Xdnext =  [result_traj(2,1) result_traj(2,2) result_traj(2,3) result_traj(2,10); 
result_traj(2,4) result_traj(2,5) result_traj(2,6) result_traj(2,11); 
result_traj(2,7) result_traj(2,8) result_traj(2,9) result_traj(2,12); 
0                0                0                1]; 


current_conf = [0 0 0 0 0 0 0 0 0 0 0 0]; % 1x12 
Tsb_0 = [cos(0) -sin(0)  0  0; 
           sin(0)  cos(0)  0  0; 
           0       0         1  0.0963; 
           0       0         0  1]; 

Tb0 = [ 1  0  0  0.1662; 
         0  1  0   0; 
         0  0  1   0.0026; 
         0  0  0   1]; 
M0e = [ 1  0  0  0.033; 
         0  1  0   0; 
         0  0  1   0.6546; 
         0  0  0   1]; 
Tse = Tsb_0*Tb0*M0e;  
X = Tse; 
Blist = [[0;  0;  1;  0;  0.033;  0],... 
           [0; -1;  0; -0.5076; 0;  0],... 
           [0; -1;  0; -0.3526; 0;  0],... 
           [0; -1;  0; -0.2176; 0;  0],... 
           [0;  0;  1;  0;      0;  0]]; 
thetalist = zeros(5,1); 
result_conf = zeros(N-1, 13); 
result_Xerr = zeros(N-1, 6); 
Kp = 50*eye(6);
Ki = 5*eye(6);
dt = 0.01;
for i = 1:N-2
    thetalist(:,1) = current_conf(4:8); 
    [~,~,~,Xerr,control]  = FeedbackControl(X, Xd, Xdnext, Kp, Ki, dt, thetalist);
    control = [control(5:9);control(1:4)];
    [next_conf] = NextState(current_conf', control, dt, max_speed) ;
    result_conf(i,1:12) = next_conf; 
    result_conf(i,13) = result_traj(i,13); 
    result_Xerr(i,:) = Xerr; 
    phi = next_conf(1); 
    x = next_conf(2); 
    y = next_conf(3); 
    thetalist(:,1) = next_conf(4:8); 
    T0e = FKinBody(M0e, Blist, thetalist); 
    Tsb_phi = [cos(phi) -sin(phi)  0  x; 
                 sin(phi)  cos(phi)  0  y; 
                 0         0         1  0.0963; 
                 0         0         0  1]; 
    Tse = Tsb_phi*Tb0*T0e; 
    X = Tse; 

    Xd =[result_traj(i+1,1) result_traj(i+1,2) result_traj(i+1,3) result_traj(i+1,10); 
      result_traj(i+1,4) result_traj(i+1,5) result_traj(i+1,6) result_traj(i+1,11); 
      result_traj(i+1,7) result_traj(i+1,8) result_traj(i+1,9) result_traj(i+1,12); 
      0                0                0                1]; 
    Xdnext =  [result_traj(i+2,1) result_traj(i+2,2) result_traj(i+2,3) result_traj(i+2,10); 
    result_traj(i+2,4) result_traj(i+2,5) result_traj(i+2,6) result_traj(i+2,11); 
    result_traj(i+2,7) result_traj(i+2,8) result_traj(i+2,9) result_traj(i+2,12); 
    0                0                0                1]; 
    current_conf = next_conf;
end
writematrix(result_conf,'result_conf.csv');
writematrix(result_Xerr,'result_Xerr.csv');
end