function Tse = row_vector(traj,zero_or_one,k)
    Tse = zeros(k,13);
    for i = 1:k
    Tse(i,:) = [traj{i}(1,1) traj{i}(1,2) traj{i}(1,3) traj{i}(2,1) traj{i}(2,2)...
        traj{i}(2,3) traj{i}(3,1) traj{i}(3,2) traj{i}(3,3) traj{i}(1,4) ...
        traj{i}(2,4) traj{i}(3,4) zero_or_one];
    end
end