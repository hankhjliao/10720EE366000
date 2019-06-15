function [X] = encode(x)

X = zeros(1,64);
count=1;
for k=2:16
    if mod(k,2)==1
        for i=1:8
            for j=1:8
                if (i+j) == k
                    X(1,count)=x(i,j);
                    count=count+1;
                end    
            end
        end   
    else
        for j=1:8
            for i=1:8
                if (i+j) == k
                    X(1,count)=x(i,j);
                    count=count+1;
                end    
            end
        end   
    end
end

X=reshape(X,[8,8]).';