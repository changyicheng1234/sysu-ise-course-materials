% 读取原始图像、噪声图像和去噪后的图像
src = imread('D:\\学习\\大三上\\图像处理\\src3.png');  % 原始图像
noisy = imread('D:\\学习\\大三上\\图像处理\\zao3.png');   % 带噪声的图像
denoised = imread('D:\\学习\\大三上\\图像处理\\denoised3.png'); % 去噪后的图像

% 确保图像为灰度图像
if size(src, 3) == 3
    src = rgb2gray(src);   % 将彩色图像转换为灰度图像
end

if size(noisy, 3) == 3
    noisy = rgb2gray(noisy);
end

if size(denoised, 3) == 3
    denoised = rgb2gray(denoised);
end

% 假设 src, noisy, denoised 已经定义并且是有效的图像
% 计算原始图像和去噪图像的 MSE, PSNR, SSIM

% 计算 MSE (均方误差)
mse_original = mean((double(src) - double(noisy)).^2, 'all');
mse_denoised = mean((double(src) - double(denoised)).^2, 'all');

% 计算 PSNR (峰值信噪比)
max_value = 255;  % 对于8位图像，最大值为255
psnr_original = 10 * log10(max_value^2 / mse_original);
psnr_denoised = 10 * log10(max_value^2 / mse_denoised);

% 计算 SSIM (结构相似性指数)
[ssim_original, ~] = ssim(noisy, src);
[ssim_denoised, ssim_map] = ssim(denoised, src);

% 可视化结果
figure;

subplot(2, 3, 1);
imshow(src);
title('Original Image');

subplot(2, 3, 2);
imshow(noisy);
title('Noisy Image');

subplot(2, 3, 3);
imshow(denoised);
title('Denoised Image');

subplot(2, 3, 4);
imshow(ssim_map, []);
colorbar;
title('SSIM Map');

subplot(2, 3, 5);
imshow(abs(double(src) - double(denoised)), []);
title('Difference Image');

subplot(2, 3, 6);
text(0.5, 0.5, ...
    sprintf('MSE (Noisy): %.2f\nPSNR (Noisy): %.2f dB\nSSIM (Noisy): %.4f\n\nMSE (Denoised): %.2f\nPSNR (Denoised): %.2f dB\nSSIM (Denoised): %.4f', ...
    mse_original, psnr_original, ssim_original, mse_denoised, psnr_denoised, ssim_denoised), ...
    'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
axis off;
title('Evaluation Metrics');

% 显示计算结果
fprintf('MSE (Noisy): %.2f\n', mse_original);
fprintf('PSNR (Noisy): %.2f dB\n', psnr_original);
fprintf('SSIM (Noisy): %.4f\n', ssim_original);
fprintf('MSE (Denoised): %.2f\n', mse_denoised);
fprintf('PSNR (Denoised): %.2f dB\n', psnr_denoised);
fprintf('SSIM (Denoised): %.4f\n', ssim_denoised);

