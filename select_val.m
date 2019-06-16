function [value,AC] = select_val(origin)
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