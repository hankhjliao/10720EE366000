function [table,freq]=cell_frequency(code,pre_table,pre_freq)
table=pre_table;
freq=pre_freq;
for i=1:length(code)
    check = code{i};
    check = check(1:2);
    find = false;
    for j=1:length(table)
        if isequal(check,table{j})
            freq(j)=freq(j)+1;
            find=true;
        end
    end
    if ~find
        table=[table,check];
        freq=[freq,1];
    end
end