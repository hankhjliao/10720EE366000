function [ encode ] = check_RLencode(code)
len = length(code);
zero_end = code{len};
if zero_end(1)==0 && zero_end(2)==0
    for i=len-1:-1:1
        check = code{i};
        if check(2)==0
            code=code(1:i);
            code{i}=[0,0];
        else
            break;
        end    
    end
end
encode = code;
