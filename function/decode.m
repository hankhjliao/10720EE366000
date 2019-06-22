function [origin]=decode(DC,AC)
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
matrix = reshape(matrix',[1,64]);

% This part inverse zigzag scan
% put the vector back
count=1;
for k=2:16
    if mod(k,2)==1
        for i=1:8
            for j=1:8
                if (i+j) == k
                    origin(i,j)=matrix(1,count);
                    count=count+1;
                end    
            end
        end   
    else
        for j=1:8
            for i=1:8
                if (i+j) == k
                    origin(i,j)=matrix(1,count);
                    count=count+1;
                end    
            end
        end   
    end
end
origin(1,1)=matrix(1,1);