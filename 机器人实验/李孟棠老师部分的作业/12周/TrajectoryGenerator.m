function result_traj= TrajectoryGenerator(Tseinitial,Tscinitial,Tscfinal,Tcegrasp,Tcestandoff,k)
%UNTITLED2 此处显示有关此函数的摘要
% 初始位形𝑇𝑠𝑒𝑖𝑛𝑖𝑡𝑖𝑎𝑙
% Tscinitial 物块初始位形
% Tscfinal 物块期望终点位形
% Tcegrasp 爪子开始闭合时相对于物块的位形
% 待命位形Tcestandoff
% 每秒的参考轨迹数目k
result_traj = zeros(k,13); 

result_traj(1:k,:) = row_vector(ScrewTrajectory(Tseinitial,Tscinitial*Tcestandoff,1,k,3),0,k);
writematrix(result_traj,'traj_csv_file.csv');

result_traj(1:k,:) = row_vector(ScrewTrajectory(Tscinitial*Tcestandoff, Tscinitial*Tcegrasp, 5, k, 3), 0,k);
writematrix(result_traj,'traj_csv_file.csv','writeMode','append');

result_traj(1:k,:)  = row_vector(ScrewTrajectory(Tscinitial*Tcegrasp, Tscinitial*Tcegrasp, 5, k, 3), 1,k);
writematrix(result_traj,'traj_csv_file.csv','writeMode','append');

result_traj(1:k,:)  = row_vector(ScrewTrajectory(Tscinitial*Tcegrasp, Tscinitial*Tcestandoff, 5, k, 3), 1,k);
writematrix(result_traj,'traj_csv_file.csv','writeMode','append');

result_traj(1:k,:) = row_vector(ScrewTrajectory(Tscinitial*Tcestandoff, Tscfinal*Tcestandoff, 5, k, 3), 1,k);
writematrix(result_traj,'traj_csv_file.csv','writeMode','append');

result_traj(1:k,:)  = row_vector(ScrewTrajectory(Tscfinal*Tcestandoff, Tscfinal*Tcegrasp, 5, k, 3), 1,k);
writematrix(result_traj,'traj_csv_file.csv','writeMode','append');

result_traj(1:k,:)  = row_vector(ScrewTrajectory(Tscfinal*Tcegrasp, Tscfinal*Tcegrasp, 5, k, 3), 0,k);
writematrix(result_traj,'traj_csv_file.csv','writeMode','append');

result_traj(1:k,:)  = row_vector(ScrewTrajectory(Tscfinal*Tcegrasp, Tscfinal*Tcestandoff, 5, k, 3), 0,k);
writematrix(result_traj,'traj_csv_file.csv','writeMode','append');
end



