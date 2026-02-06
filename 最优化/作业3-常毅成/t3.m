
    % 目标函数
    f = @(x) 3*x(1)^4 + 2*x(2)^2 - 4*x(1)*x(2);
    % 梯度
    grad_f = @(x) [12*x(1)^3 - 4*x(2); 4*x(2) - 4*x(1)];
    
    % 初始点
    x = [2; -1];
    epsilon = 0.01;
    max_iter = 1000;
    iter = 0;
    
    % 初始方向
    d = -grad_f(x);
    
    fprintf('迭代次数 | x1       | x2       | f(x)     | ||grad||\n');
    fprintf('-------------------------------------------------\n');
    
    while norm(grad_f(x)) > epsilon && iter < max_iter
        % 线搜索
        line_search = @(alpha) f(x + alpha*d);
        alpha = fminbnd(line_search, 0, 1);
        
        % 更新点
        x_new = x + alpha*d;
        
        % 计算beta (Polak-Ribière)
        g = grad_f(x);
        g_new = grad_f(x_new);
        beta = max(0, (g_new' * (g_new - g)) / (g' * g));
        
        % 更新方向
        d = -g_new + beta*d;
        x = x_new;
        iter = iter + 1;
        
        % 显示结果
        fprintf('%9d | %.6f | %.6f | %.6f | %.6f\n', ...
                iter, x(1), x(2), f(x), norm(grad_f(x)));
    end
    
    fprintf('\n最终点: [%.6f, %.6f]\n', x(1), x(2));
    fprintf('目标函数值: %.6f\n', f(x));
    fprintf('梯度范数: %.6f\n', norm(grad_f(x)));
    fprintf('迭代次数: %d\n', iter);
