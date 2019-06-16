function [matrix]=decode(DC,AC)
matrix = zeros(8,8);

% Decode run length encode back to origin 8*8 matrix

for i =1:8
    for j = 1:8
        if i==1 && j ==1
            %This is DC term
           matrix(i,j)=DC;
        else
            % select_val function will output value and modified AC
            [value,AC] = select_val(AC);
            matrix(i,j)=value;
        end   
    end
end

    