function [value,AC] = select_val(origin)
% this function select the value to fill back the matrix
% there are three case
% first (0,0) : all value should be 0
% second (X,Y,Z) : there are zeros before Z
% third (0,Y,Z) : fill Z back
AC=origin;
if origin(1)== 0 && origin(2) == 0
    value = 0;
else
    if origin(1) > 0
        value = 0;
        AC(1)=AC(1)-1;
    else
        value = AC(3);
        AC = AC(4:end);
    end    
end