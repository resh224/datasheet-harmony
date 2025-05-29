* SN74LVC1G04 Inverter Gate
[Device]  
ProductName = SN74LVC1G04  
VendorName = Texas Instruments  
VendorID = 0x00000001  
ProductCode = 0x74LVC1G04  
RevisionNumber = 1.0  

[Params]  
0x1000 = UINT16:3.3V   ; Supply Voltage (VCC)  
0x1001 = FLOAT32:0.7   ; NMOS Threshold Voltage (VTO_N) [SPICE Parameter][1]  
0x1002 = FLOAT32:-0.7  ; PMOS Threshold Voltage (VTO_P) [SPICE Parameter][1]  
0x1003 = FLOAT32:120e-6 ; NMOS Transconductance (KP_N) [SPICE Parameter][1]  
0x1004 = FLOAT32:40e-6  ; PMOS Transconductance (KP_P) [SPICE Parameter][1]  
0x1005 = FLOAT32:0.1    ; Package Resistance (R_pkg) [SPICE Parameter][1]  
0x1006 = STRING:2nH     ; Package Inductance (L_pkg) [SPICE Parameter][1]  

.SUBCKT SN74LVC1G04 A Y VCC GND
M1 Y A VCC VCC PMOS W=2u L=0.1u
M2 Y A GND GND NMOS W=1u L=0.1u
.MODEL PMOS PMOS (VTO=-0.7 KP=40e-6 LAMBDA=0.05 CGSO=1n CGDO=1n)
.MODEL NMOS NMOS (VTO=0.7 KP=120e-6 LAMBDA=0.05 CGSO=1n CGDO=1n)
.ENDS
