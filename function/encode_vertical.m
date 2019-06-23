function [DC,X,RLcode] = encode_vertical(x)
% This function do two implement:
% 1.zigzag scan
% 2.RL encode

% vertical scan
X = reshape(x,[1,64]);

% DC term
DC = X(1,1);
RLcode=[];

% Run length encode, This method encodes all AC term, 
% and each cell contain three information
% RLcode = [num,size,val]
% num = number of zeros before this element
% size = number of bits needed to represent element value (ceil,log2)
% val = actual value of the element
% (0,0) represent the array contains 0 to the end of 8*8 -1 matrix (no DC)
num_zero=0;
for i=2:64
    if i==64 && X(1,i)==0
        RLcode = [RLcode,[0,0]];
    elseif X(1,i)==0
        num_zero=num_zero+1;
    else
        size = floor(log2(abs(X(1,i))))+1;
        RLcode =[RLcode,[num_zero,size,X(1,i)]];
        num_zero=0;
    end    
end
X=reshape(X,[8,8]).';