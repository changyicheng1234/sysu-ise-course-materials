
    % 目标函数
    f = @(x) 5*x(1)^2 + 2*x(2)^2 + x(1)*x(2);
    % 梯度
    grad_f = @(x) [10*x(1) + x(2); 4*x(2) + x(1)];
    
    % 初始点
    x = [3; -2];
    epsilon = 0.001;
    max_iter = 1000;
    iter = 0;
    
    fprintf('迭代次数 | x1       | x2       | f(x)     | ||grad||\n');
    fprintf('-------------------------------------------------\n');
    
    while norm(grad_f(x)) > epsilon && iter < max_iter
        % 计算搜索方向
        d = -grad_f(x);
        
        % 线搜索
        line_search = @(alpha) f(x + alpha*d);
        alpha = fminbnd(line_search, 0, 1);
        
        % 更新点
        x = x + alpha*d;
        iter = iter + 1;
        
        % 显示结果
        fprintf('%9d | %.6f | %.6f | %.6f | %.6f\n', ...
                iter, x(1), x(2), f(x), norm(grad_f(x)));
    end
    
    fprintf('\n最终点: [%.6f, %.6f]\n', x(1), x(2));
    fprintf('目标函数值: %.6f\n', f(x));
    fprintf('梯度范数: %.6f\n', norm(grad_f(x)));
    fprintf('迭代次数: %d\n', iter);
