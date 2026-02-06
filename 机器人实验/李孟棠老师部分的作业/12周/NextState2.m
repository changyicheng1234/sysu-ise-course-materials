 q = [0,0,0,0,0,0,0,0,0,0,0,0]';

result = zeros(400, 12);
for i = 1:100
    u = [0 0 0 0 0 10  10 10 10]';
    if i == 1
        result(i, :) = NextState(q,u,0.01,5);
    else
        result(i, :) = NextState(result(i-1, :)',u,0.01,100);
    end
end
for i = 101:200
    u = [0 0 0 0 0 -10 10 -10 10]'
    result(i, :) = NextState(result(i-1, :)',u,0.01,100);
end
for i = 201:300
    u = [0 0 0 0 0 -10 -10 -10 -10]'
    result(i, :) = NextState(result(i-1, :)',u,0.01,100);
end
for i = 301:400
    u = [0 0 0 0 0 10 -10 10 -10]'
    result(i, :) = NextState(result(i-1, :)',u,0.01,100);
end
result = [result, ones(400, 1)];
csvwrite('q_k_csv_file.csv',result);