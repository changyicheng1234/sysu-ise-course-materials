% 读入模糊图像
blurred_image = imread("D:\\学习\\大三上\\图像处理\\src.png");
 
% 将模糊图像转换为双精度数据类型
blurred_image_double = im2double(blurred_image);
 
% 获取图像的尺寸
[a, b] = size(blurred_image_double);
 
% 将模糊图像从时域转换为频域
fft_blurred_image = fft2(blurred_image_double);
fft_blurred_image = fftshift(fft_blurred_image);
 
% 构建退化函数（模糊核）的频域表示
[u, v] = meshgrid(1:b, 1:a); % 注意 u 和 v 的顺序与之前不同
H = exp(-0.0025 * ((u - b/2).^2 + (v - a/2).^2).^(5/6));
 
% 定义维纳滤波器的参数
K = 0.01; % 维纳滤波器的常数
gamma = 0.0001; % 正则化参数
 
% 计算维纳滤波器的频域表示
weiner_filter = conj(H) ./ (abs(H).^2 + K);
 
% 应用维纳滤波器
fft_restored_image = fft_blurred_image .* weiner_filter;
 
% 将图像从频域转换回时域
restored_image = ifftshift(fft_restored_image);
restored_image = ifft2(restored_image);
restored_image = uint8(abs(restored_image)*256);
 
imshow(restored_image);
imwrite(restored_image,"restored_kkimage.jpg")