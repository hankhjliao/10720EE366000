function [AC,AC_cell] = crop_AC_Huffman (origin)
% This version select data from cell
% This function will output one RLencode of 8*8 matrix
% which we use it to recover the origin matrix

len=length(origin);
find = false;
AC_cell = origin;

while ~find
    for i = 1:len
        check = origin{i};
        if length(check)==2
            AC=origin(1:i);
            AC_cell(1:i)=[];
            find = true;
            break;
        end    
    end    
end