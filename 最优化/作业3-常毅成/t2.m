
    % 目标函数
    f = @(x) x(1)^2 + 4*x(2)^2 + 3*x(1)*x(2);
    % 梯度
    grad_f = @(x) [2*x(1) + 3*x(2); 8*x(2) + 3*x(1)];
    
    % 初始点
    x = [1; 1];
    epsilon = 0.01;
    max_iter = 100;
    iter = 0;
    
    % 初始化Hessian逆近似为单位矩阵
    H = eye(2);
    
    fprintf('迭代次数 | x1       | x2       | f(x)     | ||grad||\n');
    fprintf('-------------------------------------------------\n');
    
    % 初始梯度
    g = grad_f(x);
    fprintf('%9d | %.6f | %.6f | %.6f | %.6f\n', ...
            iter, x(1), x(2), f(x), norm(g));
    
    while norm(g) > epsilon && iter < max_iter
        % 计算搜索方向
        d = -H * g;
        
        % 线搜索
        line_search = @(alpha) f(x + alpha*d);
        alpha = fminbnd(line_search, 0, 1);
        
        % 更新点
        s = alpha * d; % 位移
        x_new = x + s;
        
        % 计算梯度差
        g_new = grad_f(x_new);
        y = g_new - g;
        
        % BFGS更新H
        if y'*s > 0 % 确保更新稳定性
            rho = 1 / (y'*s);
            H = (eye(2) - rho*s*y') * H * (eye(2) - rho*y*s') + rho*(s*s');
        end
        
        % 更新变量
        x = x_new;
        g = g_new;
        iter = iter + 1;
        
        % 显示结果
        fprintf('%9d | %.6f | %.6f | %.6f | %.6f\n', ...
                iter, x(1), x(2), f(x), norm(g));
    end
    
    fprintf('\n最终点: [%.6f, %.6f]\n', x(1), x(2));
    fprintf('目标函数值: %.6f\n', f(x));
    fprintf('梯度范数: %.6f\n', norm(g));
    fprintf('迭代次数: %d\n', iter);
