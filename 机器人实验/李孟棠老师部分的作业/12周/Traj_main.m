Tseinitial = [0 0 1 0.5518;0 1 0 0; -1 0 0 0.4012 ; 0 0 0 1];
Tscinitial = [1 0 0 1;0 1 0 0;0 0 1 0.025;0 0 0 1];
Tscfinal = [0 1 0 0;-1 0 0 -1;0 0 1 0.025;0 0 0 1];
Tcegrasp = [cos(3*pi/4) 0 sin(3*pi/4) 0.005; 0 1 0 0;-sin(3*pi/4) 0 cos(3*pi/4) -0.005;0 0 0 1];
Tcestandoff = Tcegrasp;
Tcestandoff(3,4) = 0.05;
k = 100;
result_traj = TrajectoryGenerator(Tseinitial,Tscinitial,Tscfinal,...
    Tcegrasp,Tcestandoff,k);
