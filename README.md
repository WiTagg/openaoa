# openaoa
Angle of Arrival implementation using MUSIC algorithm. The implementation is very flexible. It can support L-shape, Uniform Circular Array(UCA), Uniform Rectangular Array(URA) and more antenna geometries. The current configuration works for WiTagg 12 antenna array.

                                 ant array
                                   0 degree
                                      |
                                      |
                    +--------+--------+--------+--------+
                    | Ant 10 | ANT 11 | ANT 0  | ANT 1  |
                    +--------+--------+--------+--------+
                    | Ant 9  |                 | ANT 2  |
                    +--------+                 +--------+--------- 270 degree
                    | Ant 8  |                 | ANT 3  |
                    +--------+--------+--------+--------+
                    | Ant 7  | ANT 6  | ANT 5  | ANT 4  |
                    +--------+--------+--------+--------+
                                      |
                                      |
                                   180 degree


step 1:
    install numpy : pip3 install numpy
    install pyserial : pip3 install pyserial

step 2:
    run command : python3 ble_aoa_main.py --l
    
    we can see some output:
    
    if on windows system output like down:
        COM10 - XDS110 Class Auxiliary Data Port (COM10)
        COM9 - XDS110 Class Application/User UART (COM9)
        
    then we use [XDS110 Class Application/User UART] port so is COM9

    if on linux system output like down:
        /dev/ttyACM1 - XDS110 (03.00.00.13) Embed with CMSIS-DAP
        /dev/ttyACM0 - XDS110 (03.00.00.13) Embed with CMSIS-DAP
        
    then we use port /dev/ttyACM0

step 3:
    use putty or other sofeware to open serial port COM9 (on linux use minicom open /dev/ttyACM0). The serial parameter are : 
    
        [baudrate 115200, data bits 8, stop bits 1, parity None, flow control None]
        
    we can see some output below:
    
        START{"type": 6,"mac":"01:23:45:67:89:ab","seq":441003,"rssi":-64,"channel":39,"csi_data":
        [69,55,68,56,70,56,73,57,-287,58,-284,56,-277,51,84,50,                           //ant0 8 times sample
        -46,79,-46,80,-44,79,-46,78,-45,76,-42,73,-42,72,-39,74,                         //ant1 8 times sample
        183,32,-175,32,-171,32,-176,31,-178,31,-179,30,-175,30,-171,32,                  //ant2 8 times sample
        -50,46,-47,45,-46,47,-47,47,-49,48,-49,46,-46,48,-48,50,                         //ant3 8 times sample
        36,36,33,34,31,30,35,29,32,30,35,31,34,33,39,35,                                 //ant4 8 times sample
        142,69,142,71,142,71,142,69,145,68,149,67,-212,70,-214,71,                       //ant5 8 times sample
        223,80,222,81,221,81,222,82,-136,84,-135,86,-130,90,-129,91,                     //ant6 8 times sample
        275,65,275,66,-86,68,-85,71,-85,74,-83,73,-79,71,-79,71,                         //ant7 8 times sample
        199,85,198,83,200,82,199,82,202,82,207,82,209,82,-149,84,                        //ant8 8 times sample
        195,51,198,51,199,48,199,45,203,43,202,42,203,43,202,43,                         //ant9 8 times sample
        -188,86,-186,86,171,86,172,87,173,89,172,90,173,93,172,95,                       //ant10 8 times sample
        -131,94,-130,94,-126,96,239,97,239,98,244,99,244,99,244,96                       //ant11 8 times sample
        ]}END
        
    every IQ data combines a pair of phase and amplitude vaules. Each row is for an antena and has 8 samples

step 4:
    Run the ble_aoa_main code. (Make sure to exit putty or close any sofeware that have opened the serial port.)
    run command :
        [on windows] python3 ble_aoa_main.py --data_source=COM9
        [on linux] sudo python3 ble_aoa_main.py --data_source=/dev/ttyACM0
        
    we can see output like this:
        {"recv_time": "1972-03-24 15:06:38", "mac": "01:23:45:67:89:ab", "seq": 446194, "rssi": -64, "freq": 2480000000, "aoa": 39}
        {"recv_time": "1972-03-24 15:06:38", "mac": "01:23:45:67:89:ab", "seq": 446195, "rssi": -68, "freq": 2480000000, "aoa": 36}
        {"recv_time": "1972-03-24 15:06:38", "mac": "01:23:45:67:89:ab", "seq": 446196, "rssi": -68, "freq": 2480000000, "aoa": 33}
        {"recv_time": "1972-03-24 15:06:39", "mac": "01:23:45:67:89:ab", "seq": 446197, "rssi": -71, "freq": 2480000000, "aoa": 33}
        {"recv_time": "1972-03-24 15:06:39", "mac": "01:23:45:67:89:ab", "seq": 446198, "rssi": -71, "freq": 2480000000, "aoa": 33}
        
    aoa is the angle value in 360 degree.
