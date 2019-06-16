function [AC,AC_cell] = crop_AC (origin)
len=length(origin);
find = false;

while ~find
    for i = 1:len
        if origin(i)==0 && origin(i+1)==0
            AC=origin(1:i+1);
            AC_cell = origin(i+2:end);
            find = true;
            break;
        end    
    end    
end