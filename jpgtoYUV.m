function [YUV]=jpgtoYUV(image)
[X,map] = rgb2ind(image,32);
RGB = ind2rgb(X,map);
YUV=rgb2ycbcr(RGB);
end