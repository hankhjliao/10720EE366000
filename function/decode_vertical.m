function [origin]=decode_vertical(DC,AC)
% This function do two implement:
% 1. RL decode
% 2. inverse zigzag scan
matrix = zeros(8,8);
origin = zeros(8,8);

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
% convert the matrix into a vector
origin = reshape(matrix',[8,8]);

% This part inverse zigzag scan
% put the vector back
%origin(1,1)=matrix(1,1);