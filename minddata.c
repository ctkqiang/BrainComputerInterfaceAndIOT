/**
* @AUTHOR: JOHN MELODY ME
* This module is used to collect EEG data and convert it into a 16-bit time domain signal.
* Brain wave module operating voltage is 3.3v, built-in 50hz filter circuit
* The module output is a UART serial port, the serial port parameters and data format are as follows
*
* Serial output configuration:
* Check digit: None
* Data bit: 8bit
* Stop bit: 1bit
* Baud rate: 115200
*
*        Data Format:    
*        The P2 Firmware Protocol was the inital transmission protocol of the OpenEEG project,
*        used by ModularEEG. It is compatible with the ElectricGuru application.
*        P2 uses 17 data bytes to transmit 6 channels of EEG data:
*
*        1: sync0;          // synchronisation byte 1 = 0xa5  
*        2: sync1;          // synchronisation byte 2 = 0x5a
*        3: version;        // version number = 2
*        4: count;          // packet counter. Increases by 1 each packet.
*        5: Chn1high        // channel 1 high byte
*        6: Chn1low         // channel 2 low byte
*        7: Chn2high        // channel 2 high byte
*        8: Chn2low        
*        9: Chn3high
*        10: Chn3low
*        11: Chn4high
*        12: Chn4low
*        13: Chn5high
*        14: Chn5low
*        15: Chn6high
*        16: Chn6low        // channel 6 low byte
*        17: switches;      // State of PD5 to PD2, in bits 3 to 0.
*
*       // 17 байтов данных для передачи 6 каналов данных ЭЭГ
*
*        A5 5A 02 39 02 33 01 EB 02 22 01 B3 02 00  02 00 0F
*        -- -- -- -- ----- ----- ----- ----- ----- -----  --
*        |  |  |  |   |     |     |     |     |     |
*        |  |  |  |   |     |     |     |     |     +-------- ch6
*        |  |  |  |   |     |     |     |     +-------------- ch5
*        |  |  |  |   |     |     |     +-------------------- ch4
*        |  |  |  |   |     |     +-------------------------- ch3
*        |  |  |  |   |     +-------------------------------- ch2
*        |  |  |  |   +-------------------------------------- ch1
*        |  |  |  +------------------------------------------ packet counter. Increases by 1 each packet.
*        |  |  +--------------------------------------------- version number = 2
*        |  +------------------------------------------------ synchronisation byte 2 = 0x5a
*        +--------------------------------------------------- synchronisation byte 1 = 0xa5
*
*       Here we provide a 2-channel module, so the 9th to 16th data is meaningless.
*       Here we give two sample code (the team can use this as a template to write data reading software)
*
*       Parsing code example:
*       Embedded code (C language)
*       Serial port receiving and parsing : 
*       For the convenience of reading, the algorithm is not simplified,
*/


#define FFT_N 256 // AMOUNT OF DATA PER/SEC;
#define Chnum_MAX 2 // THE NUMBER OF BRAINWAVE CHANNELS THE CHIP PROVIDED THIS TIME IS A 2-CHANNEL VERSION.
S16 MindDataBuf[FFT_N][Chnum_MAX]; // extracted one second data
U8 MindData_used=1; // DATA HAS BEEN USED;

Void USART1_IRQHandler(void) {
        Static u16 MindData_num=0; // 256 COUNT;
        Static u8 UART_receive_num = 0; // FRAME FORMAT COUNT;
        Static u8 MindDatabyteBuf[Chnum_MAX][2]={0}; // Valid data extracted in each frame (before and after bytes)
        If ((USART_GetITStatus(USART1, USART_IT_RXNE)!=RESET)) {
            U8 tempByts = (uint8_t)USART1->DR;//Read one bit of data from the register
                // The current one second data can be received again after being used
                // (normally, the data will be transferred in time without causing data block)
            If(MindData_used==0x01) {
                    switch (UART_receive_num)
                    {
                        case 0:
                        { if(tempByts== 0xA5) UART_receive_num++; }
                        break;
                        case 1:
                        {
                            if(tempByts== 0x5A)
                            { UART_receive_num++;}
                            else
                            { UART_receive_num=0;}
                        }
                        break;
                        case 2:
                        {
                            if(tempByts==0x02)
                            { UART_receive_num++;}
                            else
                            { UART_receive_num=0;}
                        }
                        break;
                        case 3://Data sequence, no processing at the moment
                        {
                            UART_receive_num++;
                        }break;
                        case 4:
                        case 5:
                        case 6:
                        case 7:
                        case 8:
                        case 9:
                        case 10:
                        case 11:
                        case 12:
                        case 13:
                        case 14: //low position
                        case 15:
                        {
                            u8 temp_ch=(UART_receive_num-4)/2; //Number of channels, note that UART_receive_num must be integer
                            u8 temp_hl=(UART_receive_num-4)%2; //Data high and low
                            if(temp_ch<Chnum_MAX)
                            {
                                MindDatabyteBuf[temp_ch][temp_hl]=tempByts;
                            }
                            UART_receive_num++;
                        }
                        break;
                        case 16://Deadline
                        {
                            if(tempByts == 0x0f || tempByts == 0xf0)  //Data is valid, storage
                            {
                                for(int temp=0;Chnum_MAX>temp;temp++) //Store only valid channel data
                                {
                                    // 8bit array combined into 16bit data
                                    MindDataBuf[MindData_num][temp]=(MindDatabyteBuf[temp][0] <<8) | MindDatabyteBuf[temp][1];
                                }
                                MindData_num++;
                                if(MindData_num==FFT_N)
                                {
                                    MindData_num=0;
                                    MindData_used=0;//End of data collection
                                }
                            }
                            UART_receive_num=0;
                        }
                    }
                }
            }
        }
        WinformCode(C#)
        /// <summary>
        /// Serial port receive callback function
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public void comport_main_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
                int temp_bytenum = 0;//Store serial port cache data
                try
                {
                        temp_bytenum =comport_main.BytesToRead;
                }
                catch (Exception)
                {
                        return;
                }
                if (temp_bytenum > 0)
                {
                    Byte[] temp_buff = new Byte[temp_bytenum];
                    comport_main.Read(temp_buff, 0, temp_bytenum); //Read data into the cache

                        for (int xh = 0; xh < temp_bytenum; xh++)
                        {
                            switch (receive_num)
                            {
                                case 0:
                                        if (temp_buff[xh] == 0xA5) receive_num++;
                                        break;
                                case 1:
                                        if (temp_buff[xh] == 0x5A) receive_num++;
                                        break;
                                case 2:
                                        if (temp_buff[xh] == 0x02)
                                        {
                                                receive_num++;
                                                this.toolStripStatusLabel2.Text = "";
                                        }
                                        else
                                        {
                                                receive_num = 0;
                                        }
                                        break;
                                case 3:
                                        {
                                                receive_num++;
                                        }
                                        break;
                                case 4:
                                case 5:
                                case 6:
                                case 7:
                                case 8:
                                case 9:
                                case 10:
                                case 11:
                                case 12:
                                case 13:
                                case 14://High Position
                                case 15://Lower Position
                                        {
                                                int temp = (receive_num - 4) / 2;//Number of channels
                                                MindDatabyteBuf[temp, receive_num % 2] = temp_buff[xh];
                                                receive_num++;
                                        }
                                        break;
                                case 16:
                                        {
                                                if (temp_buff[xh] == 0x0f || temp_buff[xh] == 0xf0)
                                                {
                                                        new Note(MindDatabyteBuf, list);
                                                }
                                                receive_num = 0;
                                        }
                                        break;
                            }
                        }
                }
        }

        public Note(byte[,] data_buff,DataList datalist)//Add node
        {
                for (short xh = 0; xh < 6; xh++)
                {
                        data[xh] = (short)((data_buff[xh, 0] << 8) + data_buff[xh, 1]);
                }
                datalist.end.next = this;//Tail node movement
                datalist.end = this;
                datalist.longadd();
        }
/*
After the data is read, it is a time domain signal. If you need to perform brain wave processing, you may need to use the frequency domain signal. Please take care of it yourself. Example: The simplest method, if you use matlab, you can directly call the function calculation of Fourier transform.
Regarding the processing of brain wave signals, please participate in the inquiry and exploration by each participating team.
*/

