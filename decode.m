function [matrix]=decode(DC,AC)
matrix = zeros(8,8);

for i =1:8
    for j = 1:8
        if i==1 && j ==1
           matrix(i,j)=DC;
        else
            [value,AC] = select_val(AC);
            matrix(i,j)=value;
        end   
    end
end

    