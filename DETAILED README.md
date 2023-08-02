# Data Acquisition System
 A detailed insight into the various sensors and codes implimented to creare our fully functional Formula Student Data Acquisition System

<!-- ---------------------------------------------------------------------------------------------------------- -->
## Table of Contents
- [Sensors Used](#sensors-used)
- [Data Gathering](#data-gathering)
- [Getting DAQ Ready](#getting-daq-ready)
- [Motor Controller MC](#motor-controller-mc)
- [BMS Battery Management System](#bms-battery-management-system)
- [The Hall Effect Sensor](#the-hall-effect-sensor)
- [Mass Flow Rate (MFR)](#mass-flow-rate-mfr)
- [User interface](#user-interface)
- [Telemetry](#telemetry)
- [Credits](#credits)
  
<!-- ---------------------------------------------------------------------------------------------------------- -->
## Sensors Used
We use the following sensors from which the data needs to be extracted:
<details><summary> Motor Controller (MC)</summary> 

DTI HV 500 LC (https://drivetraininnovation.com/webshop/inverters/dti-hv-500-liquid-cooled).
Refer to *HV-500 CAN Manual 2.3*
<p align="center"><img src="./resources/readme images/mc.jpg" alt="mc" width="300"/></p>
</details>

<details><summary> Battery Management System(BMS) </summary>  
	
BMS Orion 2 (https://www.orionbms.com/products/orion-bms-standard)
<p align="center"><img src="./resources/readme images/bms.jpg" alt="bms" width="300"/></p>
</details>

<details><summary> Mass Flow rate Sensor (MFR) </summary> 
	
Speed of the fluid in the cooling system tubes 
<p align="center"><img src="./resources/readme images/mfr.jpg" alt="mfr" width="300"/></p>
</details>

<details><summary> Hall Effect Sensor </summary>
	
Used to determine the RPM of the Wheels.Became obselete once we figured out to obtain the same via motor controller
<p align="center"><img src="./resources/readme images/hall effect.jpeg" alt="mfr" width="300"/></p>
</details>

<!-- ---------------------------------------------------------------------------------------------------------- -->
## Data Gathering
We fetch the following data:
<details><summary> From Motor Controller  </summary>
	
1. Motor Temperature
2. Motor Controller Temperature 
3. ERPM
4. Throttle
 </details>

<details><summary> From BMS  </summary>
	
1. Accumulator current
2. Accumulator Voltage
3. State of charge
4. Highest temperature of a cell in the battery
5. lowest temperature of a cell in the battery
 </details>

<details><summary> From MFR  </summary>
Speed of the fluid in the cooling system tubes (unit: L/minute)
 </details>

<!-- ---------------------------------------------------------------------------------------------------------- -->
## Getting DAQ Ready

<details><summary>  Hardware, Softwares and Modules </summary>
	
1. **CANBUS wiring**(twisted) with two 120 ohm resistors at both ends: to communicate with Motor Controller and BMS
2. **MCP2515 module:** to communicate between CANBUS and Arduino. (https://github.com/autowp/arduino-mcp2515/archive/master.zip)
3. **Arduino Mega 2560:** to process the data received by all the sensors and convert it into useable form
4. **Raspberry Pi 4:** to receive the data from Arduino and display it on the dashboard screen with appropriate UI
5. **HC12 module:** for telemetry, i.e, send the real time data from sensors to the pit station where teams can review it and also perform data logging
6. **Buck Converter:** to convert the 12V DC (from LV battery) into a constant 5V DC supply to power the Arduino and Raspberry pi
7. **mcp-can.h module:** To recieve canbus data via mcp(https://downloads.arduino.cc/libraries/github.com/coryjfowler/mcp_can-1.5.0.zip)
8. **Arduino IDE:** Download the latest version of arduino IDE on your laptop to upload the code onto the arduino as well as observe incoming data

*In the arduino IDE, go to Sketch -> Include Library -> Add .ZIP Library and add the .zip files for the libararies you just downloaded.*
</details>



<details><summary> Connections </summary>

1. Connect the CAN2.0 High and CAN2.0 Low wires of Motor Controller and BMS to the CANBUS wiring. Make sure these nodes are connected in parallel.
2. Also connect the MCP2515 module in parallel to the nodes.
<p align="center"><img src="./resources/readme images/canbus.jpeg" alt="canbus" width="350"/></p>

3. Now connect the MCP2515 with the Arduino Mega in the following way:
<p align="center"><img src="./resources/readme images/mega to mcp.jpg" alt="megatomcp" width="350"/></p>
4. Also connect the MFR sensor to the arduino. The 'data' wire should go in pin 4 of arduino. And the V+ve and V-ve wires should go in 5V and GND pins respectively.

5. Connect the HC12 module such that it's RX and TX pins are connected to pin 10 and pin 11 of the arduino respectively. Also it's Vcc and GND pins should be connected to the 5V and GND pins of arduino

6. Power the arduino using Type A to Type B connector from the raspberry pi

7. Raspberry pi should get it's power from the general GPIO pins which are connected to the LV battery via a buck converter. The buck converter's potentiometer should be adjusted such that it converts the 12V input into 5V output

8. Raspberry pi should further be connected to the monitor present in the dashboard

</details>

<details><summary> Steps to follow </summary>
	
1. Establish the connections as mentioned above. Initially connect the arduino to your personal laptop instead of the raspberry to upload a code.
2. On your personal laptop (having the arduino IDE), install the libraries:
	1. arduino-mcp2515 (https://github.com/autowp/arduino-mcp2515/archive/master.zip)
	2. mcp-can.h (https://downloads.arduino.cc/libraries/github.com/coryjfowler/mcp_can-1.5.0.zip)
3. In the arduino IDE, go to Sketch -> Include Library -> Add .ZIP Library and add the .zip files for both the libararies you just downloaded.
4. Upload the merged-arduino-code.ino onto the Arduino Mega 2560 using the IDE.
5. Open Serial Monitor with Ctrl+Shift+M to ensure data is coming in properly and the output is appropriate
6. Close the arduino IDE. Disconnect the arduino from your personal laptop and connect it back to the raspberry pi.
7. Power up the raspberry pi and copy the entire folder of UI onto it.
8. Run the file gui_returns.py by first navigating to the path where you copied the UI folder in the terminal. Then typing:
python3 'folder-name' '.py file-name'
<img src="./resources/readme images/working pit ui.png" alt="PIT display" />
<img src="./resources/readme images/working ui.png" alt="Dash display" />
</details>

<!-- ---------------------------------------------------------------------------------------------------------- -->
# Motor Controller MC:
### Credits: **Harsh Srivastava** (https://github.com/harshsrivastava0)

<p align="center"><img src="./resources/readme images/mc.jpg" alt="mc" width="300"/></p>

We use the **DTI HV 500 LC** (https://drivetraininnovation.com/webshop/inverters/dti-hv-500-liquid-cooled).
Refer to *HV-500 CAN Manual 2.3*


Following this readme file, you'll be able to extract data from the DTI HV-500 LC motor controller starting from scratch. This Motor Controller uses CANBUS communication to send and receive data. We'll be seeing how to establish a connection between the Motor Controller and the CANBUS wiring, how to get the raw canbus data, and how to convert this raw data into useable form.


<details><summary> Connections: </summary> 
<p align="center"><img src="./resources/readme images/entire mc setup.jpeg" alt="entire-mc-setup" width="300"/></p>

1. To the CAN high wire, connect the wire coming in from PIN-12 of the Motor Controller's Harness Connector. This pin is marked for CAN2.0 high.
2. To the CAN low wire, connect the wire coming in from PIN-4 of the Motor Controller's Harness Connector. This pin is marked for CAN2.0 low.
<p align="center"><img src="./resources/readme images/mc harness connector.png" alt="mc harness connector.png" width="300"/></p>

3. To the CAN high wire, also connect the wire coming in from MCP2515 module's CAN-H pin and to the CAN low wire, also connect the wire coming in from MCP2515 module's CAN-L pin.
4. Then connect the MCP2515 to the Arduino Mega 2560 Board using the following connections: 
<p align="center"><img src="./resources/readme images/mega to mcp.jpg" alt="mega to mcp" width="300"/></p>
This MCP2515 module is used to communicate the raw canbus data to the arduino board via SPI communication protocol.

5. Now connect the Arduino board to your laptop using the Type-A to Type-B connector.
And voila! you're good to go.
 </details>


<!-- ---------------------------------------------------------------------------------------------------------- -->
# BMS Battery Management System:
### Credits: **Satwik Jain** (https://github.com/satwikjain23)
A battery management system (BMS) is any electronic system that manages a rechargeable battery, such as by protecting the battery from operating outside its safe operating area, monitoring its state, calculating secondary data, reporting that data, controlling its environment, balancing it.
<p align="center"><img src="./resources/readme images/bms.jpg" alt="bms" width="300"/>></p>

We use the **BMS Orion 2** (https://www.orionbms.com/products/orion-bms-standard)

<details><summary> Documentation: </summary> 
	
- [Wiring and Installation Manual](https://www.orionbms.com/manuals/pdf/orionbms2_wiring_manual.pdf)
- [Operation Manual](https://www.orionbms.com/manuals/pdf/orionbms2_operational_manual.pdf)
- [Utility Manual](https://www.orionbms.com/manuals/pdf/orionbms2_operational_manual.pdf)
- [Utility Installation](https://www.orionbms.com/downloads/orionbms2_utility_stable.exe)
</details>

<details><summary> LED Status </summary> 
	
- **Continuous RED Light** - BMS OK
- **Flashing RED Light** - Fault in wiring (**TURN OFF THE BMS!!**)
</details>

<details><summary> Wiring </summary>
	
For testing the BMS connect it to the charger first instead of HV:
1. Connect the **Ready Power** and **Ground** of BMS to positive and negative terminals of charger respectively
2. Connect **Always On Power** and **Charge Power** to each other via a fuse
3. Attach a wire to the **Ground Lug** and join it with **Ground** of BMS,i.e.both of the wires are connected to the negative terminal of charger
</details>

<details><summary> How to edit canbus messages: </summary>

Refer to the link : (https://www.orionbms.com/downloads/misc/editing_canbus_messages.pdf)
1. Scale the parameters in your arduino code and not in the utility
2. For parameters with lenth of 2 bytes (eg-Pack Current, Pack Inst. Voltage,etc) data from both the bytes need to be joined first and then scaled.
3. You can see the **Scalling** value of parameters from the following pdf (https://www.orionbms.com/downloads/misc/orionbms_obd2_pids.pdf)
</details>

<details><summary> Connections to access utility: </summary>
	
1. Connect the BMS to laptop using CAN Adapter,which is attached to the CAN 1 wires.
2. Click on **Connect to BMS option**.
3. Click on **Connect**
4. You can view the incoming data by clicking on **Live CANBUS Traffic**.
5. Click on **Send Profile Changes To BMS** only after making proper changes to CANBUS settings
</details>
 
<details><summary> Connections to Arduino </summary>

1. Connect the CAN2 wires, CAN2_H and CAN2_L to MCP2515 module
2. Connect the MCP2515 to Arduino UNO using the earliar shown connections.
</details>

<details><summary> Faults </summary>
	
Convert the parameters **DTC FLAGS #1** and **DTC FLAGS #2** to binary and check each bit for faults
<p align="left"><img src="./resources/readme images/BMS DTC flags 1.png" alt="BMS DTC flags 1.png" width="500"/></p>
<p align="left"><img src="./resources/readme images/BMS DTC flags2.png" alt="BMS DTC flags 2.png" width="500"/></p>
</details>

<details><summary> Additional Links </summary>
	
- https://www.orionbms.com/general/retrieving-data-obd2-canbus/
</details>

<!-- ---------------------------------------------------------------------------------------------------------- -->
# The Hall Effect Sensor
### Credits:  **Ayan Mahajan** (https://github.com/ayanhmm)
Used to determine the RPM of the Wheels.Became obselete once we figured out to obtain the same via motor controller.
We use the  Honeywell LCZ Series Hall-effect Zero Speed Sensor.
<p align="center"><img src="./resources/readme images/hall effect.jpeg" alt="hall effect" width="300"/></p>
<details><summary> Wiring </summary>

1. Connect the 5v and ground wires to their respective pins
2. Connect the output wire to the arduino pin suggested in the code itself (currently Pin 5)
</details>

<details><summary> Working </summary>
Hall effect sensor is used to detect when magnetic materials(primarily iron) are brought close to it. It is mounted near the
rotating wheel and it is able to sense each rim that passes from front of it. the time between two consecutive rims and using the distance between them, we calculate the RPM which along with tyre radius gives Speed
<p align="center"><img src="./resources/readme images/working of hall effect.png" alt="working of hall effect.png" width="300"/></p>
</details>


<!-- ---------------------------------------------------------------------------------------------------------- -->
# Mass Flow Rate (MFR) 
### Credits:  **Raman Saini** (https://github.com/Raman-Saini9)
Speed of the fluid in the cooling system tubes 
<p align="center"><img src="./resources/readme images/mfr.jpg" alt="mfr" width="300"/></p>
<details><summary> Wiring </summary>

</details>

<details><summary> Working </summary>

</details>


<!-- ---------------------------------------------------------------------------------------------------------- -->
# User interface:
### Credits:  **Ayan Mahajan** (https://github.com/ayanhmm)
GUI to display the data obtained from various sensors on the Dashboard as well as pit screen for the crew to observe any anomalies as well as log it for future references

<img src="./resources/readme images/working pit ui.png" alt="PIT display" width="400"/> &nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp; <img src="./resources/readme images/working ui.png" alt="Dash display" width="400"/>



<details><summary> UI Pre Requirements </summary>

### Install the following python libraries:
1. Tkinter : **```pip install tk```**
2. Python Imaging Library :  **```pip install pillow```**
3. Serial : **```pip install pyserial```**

Used the Tkinter and Serial Library of python to create a **Working UI** for both the dash and the pit screen.Using the Tkinter module, created *live graphs of the incoming date, a percentage based throttle bar as well as a analog-type speedometer*.The task of **Logging the Data** for future use was tackled using the csv and logging modules of python

### Libraries no Longer Required in the Latest Version 
1. **```pip install pandas```**
2. **```pip install openpyxl```**
3. **```pip install p```**
4. **```pip install pyserial pySerialTransfer```**
                         
                         
### Install the following Fonts:
For convenience purposes, downloadable files of the specified fonts have been added to the repository
1. Caution: https://fontmeme.com/polices/police-caution/
2. Race Numbers: https://fontmeme.com/polices/police-racing-numbers/#previewtool
3. Race Space: https://fontmeme.com/polices/police-race-space/

### Make sure the Following Backgrounds are Downloaded:
For convenience purposes, downloadable images of the specified backgrounds have been added to the repository
1. Pit-Screen background

   <img src="./resources/readme images/pit bg.png" alt="pit" width="500"/>

2. Dashboard background

   <img src="./resources/readme images/dash bg.png" alt="pit" width="500"/>
   
</details>

<details><summary> Data Displayed </summary>
	
The following data is being displayed on the Dash and the PIT screen.It is to be noted that the data must also be recieved from the arduino in form of a string separated by comas and in the same order as written below.
1. Motor Temperature
2. Motor Controller Temperature
3. ERPM
4. Speed
5. Throttle
6. Pack Current
7. Instantaneous Pack Voltage
8. State of charge
9. Battery Maximum Temperarture
10. Battery Minimum Temperarture
11. BMS Input Voltage(LV Battery Voltage)
12. Motor Controller Input Voltage
13. Motor Controller Input Current
14. Motor Controller FAULTS
15. BMS FAULTS
</details>

<details><summary> Graph Logging </summary>

**get logged data as graph.py** is a python program to take the logged data and plot it as a graph so as to make it easiar to study the logged data.Is is also capable of plotting the data of more than one sensor on the same canvas so as to conviniently study the simultaneous behaviors of differsnt datasets
<img src="./resources/readme images/graph logging.png" alt="graph plot" />
</details>

<details><summary> Sources of Errors </summary>

This is a list of some errors that were faced during implementation of the python UI code while recieving data from the arduino

1. **Utf Decoding Error**- Baud rate of arduino and ui code SER.read should be same.if errer still persists,then can fixed by adding condition to decode only if decoding can be done(see main_dash.py).
2. **Canbus Fail** - "Canbus fail" error might take place when one of the following takes place. 
   1. **Faulty CS Pin**: CS pin is not declared correcty in the ide code. The Chip Select pins are special pins that can only be connected to pre defined pins of the arduino which might not be of the same number on different types of arduinos. So cross check from the internet that the code CS pin is correct.
   2. **Loose Connections**: Mcp to canbus or mcp to arduino connections are either loose or wrongly connected and can be fixed by tightning the hardware connections
3. **Port Busy**- Some other application is utilizing the port.it is probably the arduino ide running in background,can be fixed by closing it’s serial moniter.The error still might persist when no application seems to be using specified port, then try restaring your laptop.
4. **Arduino not detected** - wrong port name declared in ui ser.read(see main_dash.py).
5. **Data not refreshing in gui** - data list recieved from arduino is shorter than the data being displayed in the ui(see main_dash.py).This can also happen if there is loosening of the mcp to arduino connections due to which data is no longer being recieved.
6. **Resizing error** - this error sometimes appears while running the code on raspberry pi even if it works effortlessly on laptops. remedy :: donot resize in code but resize before hand using google. This will also conserve primary memory.For the sake of convenience, an image of the same size as our UI screen has been added to the repository
7. **Delayed refreshing** - Some delay might be seen between the sensors sending the data and it being displayed on the UI.
   1. **Baudrate out of sync**: This can also happen if the baudrate by which the sensors specially the motor controller or the bms are sending their data is different from the baudrate by which the arduino or the UI is recieving that data
   2. **Delay Error**: This can be caused if the delay set in the main_dash.py code is too long. this can be easily fixed by reducing the delay in root.after(). this delay should be equal to the delay in arduino code.
</details>

<!-- ---------------------------------------------------------------------------------------------------------- -->
# Telemetry:
### Credits:  **Monis** (https://github.com/Monis6113)	and **Ayush Jain** (https://github.com/ayushjain143)
This project involves telemetry i.e transmission and reception of data from various sensors such as Battery Management System, Motor Control, Mass Flow Rate Sensor,Hall Effect Sensor etc to a remote computer using HC-12 module on UART serial communication protocol.
<p align="center"><img src="./resources/readme images/HC12 module.png" alt="HC12 module.png" width="300"/></p>

<details><summary> Connections </summary>

<p align="center"><img src="./resources/readme images/Arduino to HC12.png" alt="Arduino to HC12.png" width="300"/></p>
1. Connect the VCC pin of HC-12 module to 5V or 3.3 V of the Arduino board.

2. Connect the GND pin of HC-12 module to any of the GND port of the Arduino board to ensure common grounding.
   
3. Connect the RX pin to the digital pin 11 and the TX pin to the digital pin 10.
   
4. Power the Arduino Mega using LV(Low voltage) power supply from the power outlet whereas power the Arduino Uno using Arduino USB cable Type A to Type B.
   
5. Open Arduino IDE software and choose appropriate Arduino Board and COM port to ensure correct serial values and uploading.
</details>

<details><summary> Code Explained </summary>
	
The telemetry sender in the code is implemented using the SoftwareSerial library and a struct named TelemetryData. The struct is defined to hold the telemetry data that will be transmitted. The struct has the following fields:

mctempmotor: a double value representing the motor temperature in degrees Celsius. mctempcontroller: a double value representing the controller temperature in degrees Celsius. pack_current: a double value representing the current flowing in the battery pack in amperes. pack_inst_voltage: a double value representing the instantaneous voltage of the battery pack in volts. state_of_charge: a double value representing the percentage of charge left in the battery pack. high_temp: a double value representing the highest temperature recorded in the battery pack in degrees Celsius. low_temp: a double value representing the lowest temperature recorded in the battery pack in degrees Celsius. The telemetrySerial is initialized as a SoftwareSerial object with pin 10 as the receive pin and pin 11 as the transmit pin. In the loop(), the telemetry data is read from the CAN bus and assigned to the corresponding fields of the TelemetryData struct. The struct is then transmitted over the telemetrySerial using the following format:

"motor_temp: controller_temp: pack_current: pack_voltage: state_of_charge: high_temp: low_temp"

The values for each field are separated by colons (:) and there are no spaces between the values. The telemetry data is sent once every second using the delay() function.

Receiver code defines a struct to hold telemetry data and reads it from a software serial port. The telemetry data contains information about the temperature, current, voltage, state of charge, and other parameters of a motor controller and battery pack.

The setup() function initializes the serial ports for debugging and telemetry data transmission.

The loop() function checks if a full telemetry packet has been received by the software serial port. If a full packet is available, it is read into a byte array and then decapsulated into a TelemetryData object using the memcpy function.
</details>


<!-- ---------------------------------------------------------------------------------------------------------- -->
## Credits
1. **Harsh Srivastava** (https://github.com/harshsrivastava0): Taking in the raw canbus data of the motor controller and converting it into readable form, merging all codes to prepare a final DAQ.
2. **Satwik Jain** (https://github.com/satwikjain23): Handling the gigantic task of receiving data from BMS, and converting it from raw CANBUS data into useable form.
3. **Ayan Mahajan** (https://github.com/ayanhmm): Handling the entire UI aspect ranging from displaying data on screen after receiving it from arduino, managing the pit screen and performing data logging as well.Also extracting data from the hall effect sensor and documenting the DAQ.
4. **Raman Saini** (https://github.com/Raman-Saini9): Handling the wiring and making sure each component receives appropriate power. Also extracting data from MFR.
5. **Monis** (https://github.com/Monis6113): Helping in figuring out Data logging and telemetry.
6. **Ayush Jain** (https://github.com/ayushjain143): Managing the telemetry aspect of the DAQ.
