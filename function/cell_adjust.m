function [new_code] = cell_adjust (code)
new_code = {};
for i=1:length(code)
    temp = code{i};
    if length(temp)==3
        temp=temp(1:2);
    end
    new_code{i} = temp;
end