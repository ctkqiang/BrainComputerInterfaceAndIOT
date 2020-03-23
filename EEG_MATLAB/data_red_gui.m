function varargout = data_red_gui(varargin)
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @data_red_gui_OpeningFcn, ...
                   'gui_OutputFcn',  @data_red_gui_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
end




function data_red_gui_OpeningFcn(hObject, eventdata, handles, varargin)
handles.output = hObject;
guidata(hObject, handles);
end



function varargout = data_red_gui_OutputFcn(hObject, eventdata, handles) 
varargout{1} = handles.output;
end


function com_num_Callback(hObject, eventdata, handles)
end


% --- Executes during object creation, after setting all properties.
function com_num_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
end



% --- Executes during object deletion, before destroying properties.
function com_num_DeleteFcn(hObject, eventdata, handles)
    fclose(g);
    delete(g); 
end

% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
global g;
    if hObject.String=='Activate'
        hObject.String='Activate';
        %%com_num.
        g=serial(char(handles.com_num.String(handles.com_num.Value)));
        g.BaudRate=115200;
        g.Parity='none';
        g.StopBits=1;
        g.DataBits=8;
        g.FlowControl='none';
        g.InputBufferSize=10000;
        g.BytesAvailableFcnMode='byte';
        g.BytesAvailableFcnCount=1;
        g.BytesAvailableFcn=@uart2_callback
        fopen(g);
        %%global time_num;
        global receive_num
        global length ;
        length=1;
        receive_num=0;
    else
        hObject.String='Activate';
        fclose(g);
    end
end