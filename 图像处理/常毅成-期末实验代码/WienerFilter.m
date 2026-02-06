function [dst,noisyImage] = WienerFilter(src, ref, stddev, lambda)
    % 输入： src - 原始彩色图像或灰度图像
    %       ref - 参考图像或模糊图像
    %       stddev - 噪声标准差
    %       lambda - 正则化系数
    % 输出： dst - 滤波后的彩色图像或灰度图像

    % 检查输入图像是否为灰度图像
    if size(src, 3) == 1  % 灰度图像
        numChannels = 1;
    else  % 彩色图像
        numChannels = 3;
    end

    % 获取原图的最佳尺寸
    m = 2^nextpow2(size(src, 1));  
    n = 2^nextpow2(size(src, 2));  

    % 对原图进行0填充，获得最佳尺寸的图像
    pad = padarray(src, [m - size(src, 1), n - size(src, 2)], 0, 'post');

    % 将参考图像 resize 到与原图相同的大小
    tmpR = imresize(ref, [m, n]);
    
    % 如果是灰度图像，确保参考图像也是单通道
    if size(tmpR, 3) == 3
        tmpR = rgb2gray(tmpR);  % 将参考图像转换为灰度
    end
    
    % 初始化输出图像
    dst = zeros(size(src), 'like', src);  
    
    % 对每个通道分别进行处理
    for i = 1:numChannels
        % 获取每个颜色通道
        srcChannel = pad(:,:,i);
        refChannel = tmpR(:,:,i);
        
        % 生成高斯噪声图像
        noisyImage = imnoise(srcChannel, 'gaussian', 0, stddev.^2);  % 添加高斯噪声

        % 显示带噪图像
        figure;
        subplot(1, 2, 1);
        imshow(srcChannel, []);
        title('Original Image Channel');
        
        subplot(1, 2, 2);
        imshow(noisyImage, []);
        title('Noisy Image Channel');
        
        % 对带噪图像进行傅里叶变换
        cpx = fft2(noisyImage);  % 使用带噪图像进行傅里叶变换

        % 分离实部和虚部
        realPart = real(cpx);
        imagPart = imag(cpx);

        % 计算参考图像的频谱（用于维纳滤波）
        refSpectrum = GetSpectrum(refChannel);

        % 计算滤波因子：结合正则化系数
        % 这里采用简单的频谱模型，加上 lambda 参数进行正则化
        factor = refSpectrum ./ (refSpectrum + stddev^2 + lambda);  % 增加正则化项 lambda

        % 对实部和虚部应用滤波因子
        realPart = realPart .* factor;
        imagPart = imagPart .* factor;

        % 合并实部和虚部
        cpxFiltered = realPart + 1i * imagPart;

        % 反傅里叶变换
        filteredChannel = ifft2(cpxFiltered);

        % 取实部，并转换为8位无符号整数
        dst(:,:,i) = uint8(real(filteredChannel(1:size(src, 1), 1:size(src, 2))));
    end
end

function spectrum = GetSpectrum(src)
    % 计算图像的频谱
    % src - 输入图像（单通道）
    % spectrum - 频谱（频域幅值的平方）
    
    % 对图像进行傅里叶变换
    cpx = fft2(src);

    % 分离实部和虚部
    realPart = real(cpx);
    imagPart = imag(cpx);

    % 计算幅值
    magnitude = sqrt(realPart.^2 + imagPart.^2);

    % 频谱是幅度的平方
    spectrum = magnitude.^2;
end
