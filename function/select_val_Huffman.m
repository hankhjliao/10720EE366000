function [value,AC] = select_val_Huffman(origin)
% This version retrieve data from cell
% this function select the value to fill back the matrix
% there are three case
% first (0,0) : all value should be 0
% second (X,Y,Z) : there are zeros before Z
% third (0,Y,Z) : fill Z back
temp=origin{1};
AC=origin;
if temp(1)== 0 && temp(2) == 0
    value = 0;
else
    if temp(1) > 0
        value = 0;
        temp(1)=temp(1)-1;
        if temp(1)==0 && temp(3)==0
            AC = AC(2:end);
        else    
            AC{1}=temp;
        end    
    else
        value = temp(3);
        AC = AC(2:end);
    end    
end