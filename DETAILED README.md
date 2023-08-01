# Data-Acquisition-System
 A data acquisition system (DAQ) created for the Formula Student Car of Team Defianz Racing wherein we take data from various sensors and display them on dashboard screen as well as the pit screen(via telemetry) while logging it at the same time for future references.

This repository is a combination of the already exiting repositories of Formula-Student-Daq-Arduino-Code, Formula-Student-Dashboard-GUI and the Formula-Student-PitScreen-UI.

## Table of Contents
- [Sensors-Used](#sensors-used)
- [Hardware-and-Modules](#hardware-and-modules)
- [Data-Displayed](#data-displayed)
- [UI-Pre-Requirements](#ui-pre-requirements)
- [Connections](#connections)
- [Steps-to-follow](#steps-to-follow)
- [Graph-Logging](#graph-logging)
- [Sources-of-Errors](#sources-of-errors)
- [My-Role](#my-role)
- [Credits](#credits)


## Sensors Used
We use the following sensors from which the data needs to be extracted:
1. **Motor Controller:** DTI HV 500 LC (https://drivetraininnovation.com/webshop/inverters/dti-hv-500-liquid-cooled).
Refer to *HV-500 CAN Manual 2.3*
<img src="./resources/readme images/mc.jpg" alt="mc" width="300"/>


2. **Battery Management System(BMS):** BMS Orion 2 (https://www.orionbms.com/products/orion-bms-standard)
<img src="./resources/readme images/bms.jpg" alt="bms" width="300"/>


3. **Mass Flow rate Sensor (MFR):** Speed of the fluid in the cooling system tubes 
<img src="./resources/readme images/mfr.jpg" alt="mfr" width="300"/>


4. **Hall Effect Sensor:** Used to determine the RPM of the Wheels.Became obselete once we figured out to obtain the same via motor controller
<img src="./resources/readme images/hall effect.jpeg" alt="mfr" width="300"/>

## Hardware and Modules
1. **CANBUS wiring**(twisted) with two 120 ohm resistors at both ends: to communicate with Motor Controller and BMS
2. **MCP2515 module:** to communicate between CANBUS and Arduino
3. **Arduino Mega 2560:** to process the data received by all the sensors and convert it into useable form
4. **Raspberry Pi 4:** to receive the data from Arduino and display it on the dashboard screen with appropriate UI
5. **HC12 module:** for telemetry, i.e, send the real time data from sensors to the pit station where teams can review it and also perform data logging
6. **Buck Converter:** to convert the 12V DC (from LV battery) into a constant 5V DC supply to power the Arduino and Raspberry pi


## Data Displayed
We fetch the following data:
1. **From Motor Controller:** Motor Temperature, Motor Controller Temperature, ERPM, Throttle
2. **From BMS:** Accumulator current, Accumulator Voltage, State of charge, Highest temperature of a cell in the battery, lowest temperature of a cell in the battery
3. **From MFR:** Speed of the fluid in the cooling system tubes (unit: L/minute)

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

## UI Pre Requirements

### Install the following python libraries:
1. Tkinter : **```pip install tk```**
2. Python Imaging Library :  **```pip install pillow```**
3. Serial : **```pip install pyserial```**


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

## Connections
1. Connect the CAN2.0 High and CAN2.0 Low wires of Motor Controller and BMS to the CANBUS wiring. Make sure these nodes are connected in parallel.
2. Also connect the MCP2515 module in parallel to the nodes.
<img src="./resources/readme images/canbus.jpeg" alt="canbus" width="350"/>
3. Now connect the MCP2515 with the Arduino Mega in the following way:
<img src="./resources/readme images/mega to mcp.jpg" alt="megatomcp" width="350"/>
4. Also connect the MFR sensor to the arduino. The 'data' wire should go in pin 4 of arduino. And the V+ve and V-ve wires should go in 5V and GND pins respectively.
5. Connect the HC12 module such that it's RX and TX pins are connected to pin 10 and pin 11 of the arduino respectively. Also it's Vcc and GND pins should be connected to the 5V and GND pins of arduino
6. Power the arduino using Type A to Type B connector from the raspberry pi
7. Raspberry pi should get it's power from the general GPIO pins which are connected to the LV battery via a buck converter. The buck converter's potentiometer should be adjusted such that it converts the 12V input into 5V output
8. Raspberry pi should further be connected to the monitor present in the dashboard

## Steps to follow
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

## Graph Logging
**get logged data as graph.py** is a python program to take the logged data and plot it as a graph so as to make it easiar to study the logged data.Is is also capable of plotting the data of more than one sensor on the same canvas so as to conviniently study the simultaneous behaviors of differsnt datasets
<img src="./resources/readme images/graph logging.png" alt="graph plot" />

## Sources of Errors
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


## My Role
Handling the entire UI aspect ranging from displaying data on screen after receiving it from arduino, managing the pit screen and performing data logging as well. Added to this, I also worked on the Hall Effect sensor.

For **Designing the UI Backgrounds**, I put my skills to action using designing softwares such as Adobe Illustrator and Canva along with various minor image editing softwares.

<img src="./resources/readme images/pit bg.png" alt="pit" width="500"/>      <img src="./resources/readme images/dash bg.png" alt="pit" width="500"/>

Once the backgrounds were finalised, I used the Tkinter and Serial Library of python to create a **Working UI** for both the dash and the pit screen.Using the Tkinter module, I was able to create *live graphs of the incoming date, a percentage based throttle bar as well as a analog-type speedometer*.The task of **Logging the Data** for future use was tackled using the csv and logging modules of python.Inorder to make inspection of the logged data more convenient, I created another program to display the logged data in a graphical manner(**Graph Logging**).

Added to this, I also worked extensively upon the **Hall Effect Sensor** which was earliar being used to determine the wheel RPM of the vehicle


## Credits
1. **Satwik Jain** (https://github.com/satwikjain23): Handling the gigantic task of receiving data from BMS, and converting it from raw CANBUS data into useable form.
2. **Harsh Srivastava** (https://github.com/harshsrivastava0): Taking in the raw canbus data of the motor controller and converting it into readable form.
3. **Raman Saini** (https://github.com/Raman-Saini9): Handling the wiring and making sure each component receives appropriate power. Also extracting data from MFR.
4.**Monis** (https://github.com/Monis6113): Helping in figuring out Data logging and telemetry.
5. **Ayush Jain** (https://github.com/ayushjain143): Managing the telemetry aspect of the DAQ.
