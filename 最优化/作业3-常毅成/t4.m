% Coordinate Descent Method for Optimization

% Define objective function
f = @(x) x(1)^2 + x(2)^2 - 3*x(1) - x(1)*x(2);

% Gradient function
gradf = @(x) [2*x(1) - 3 - x(2); 2*x(2) - x(1)];

% Initial point and tolerance
x = [0; 0]; % X0 = [0, 0]^T
epsilon = 0.1;
max_iter = 1000;
iter = 0;

% Store history for visualization
x_history = x';

while iter < max_iter
    x_old = x;
    
    % Update x1 (fix x2)
    x1_new = (3 + x_old(2)) / 2;
    x(1) = x1_new;
    
    % Update x2 (fix x1)
    x2_new = x(1) / 2;
    x(2) = x2_new;
    
    % Check convergence
    if norm(gradf(x)) < epsilon
        break;
    end
    
    x_history = [x_history; x'];
    iter = iter + 1;
end

% Display results
fprintf('Optimal point: [%.4f, %.4f]\n', x(1), x(2));
fprintf('Optimal value: %.4f\n', f(x));
fprintf('Number of iterations: %d\n', iter);
fprintf('Gradient norm: %.4f\n', norm(gradf(x)));