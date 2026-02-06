srcPath = 'D:\\学习\\大三上\\图像处理\\src.png';  % 源图像路径
refPath = 'D:\\学习\\大三上\\图像处理\\ref.png';  % 参考图像路径

% 读取图像
src = imread(srcPath);
ref = imread(refPath);

% 如果是彩色图像，转换为灰度图像
if size(src, 3) == 3
    src = rgb2gray(src);
end
if size(ref, 3) == 3
    ref = rgb2gray(ref);
end

% 设置噪声的标准差
stddev = 0.08;

% 调用维纳滤波函数进行去噪
[dst, noisyImage] = WienerFilter(src, ref, stddev, 0.01);

% 显示结果
% 创建图形窗口
figure;

% 设置大图像显示尺寸
set(gcf, 'Position', [100, 100, 1200, 400]); % 设置图像窗口大小为1200x400

% 显示原图
subplot(1, 3, 1);
imshow(src); 
title('原图');
axis off;  


subplot(1, 3, 2);
imshow(noisyImage);
title('加上高斯噪声后的图');
axis off;

% 显示去噪后的图像
subplot(1, 3, 3);
imshow(dst);
title('维纳滤波处理后的图');
axis off;

set(gcf, 'Color', 'w'); % 设置图像背景色为白色

