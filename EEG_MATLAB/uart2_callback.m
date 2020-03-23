function uart2_callback(g,BytesAvailable)
global  data_s;
global 	read_flag;
global datamiao;

global receive_num;%%Ö¡Î»ÖÃ
    
try
    out=fread(g,17,'uint8');%%Êý¾Ýbuff
catch
    return ;    
end
    data_num_temp=1;
    while data_num_temp<=17
        global ok
        ok=0;
        switch receive_num;
            case 0
                if(out(data_num_temp)==165)
                    ok=1;
                end
            case 1
                if(out(data_num_temp)==90)
                    ok=1;
                end
            case 2
                if(out(data_num_temp)==2)
                    ok=1;
                end
            case 3
                ok=1;
            case {4,5,6,7,8,9,10,11,12,13,14,15}
                ok=1;
                global temp_data
                temp_data(receive_num-3)=out(data_num_temp);
                temp_data
            case 16
                global length
                %%temp_data
                xh=1;
                while(xh<=6)
                    datamiao((xh+1)/2,length)=data_signed(temp_data(xh),temp_data(xh+1));
                    xh=xh+2;
                end
                length=length+1;
                ok=0;
                receive_num=0;
                %%datamiao
        end
        
        if ok==1;
            receive_num=receive_num+1;
            ok=0;
        else
            receive_num=0;
        end
        %%out(data_num_temp)
        %%receive_num
        data_num_temp=data_num_temp+1;
    end


end

function data=data_signed(data_H,data_L)
data=data_H*256+data_L;
if(data>32768)
    data=data-65536; 
end
end