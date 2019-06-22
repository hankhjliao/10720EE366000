function [AC,AC_cell] = crop_AC (origin)
% This function will output one RLencode of 8*8 matrix
% which we use it to recover the origin matrix

len=length(origin);
find = false;
AC_cell = origin;

while ~find
    for i = 1:len
        if origin(i)==0 && origin(i+1)==0
            AC=origin(1:i+1);
            AC_cell(1:i+1)=[];
            find = true;
            break;
        end    
    end    
end