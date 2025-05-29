# SPICE Example

Ths example shows a linkage between an SPICE model and an EDS format datasheet.  The example part is a SN74LVC1G04 Inverter Gate.1.

## **Key SPICE Parameters**

| **Parameter**          | **Symbol**                | **Value**                             | **Datasheet Reference**       |
| :--------------------------- | :------------------------------ | :------------------------------------------ | :---------------------------------- |
| **Threshold Voltage**  | `VTO`                         | NMOS: 0.7V `<br>`PMOS: -0.7V              | Input thresholds (VIH/VIL)          |
| **Transconductance**   | `KP`                          | NMOS: 120e-6 A/V²`<br>`PMOS: 40e-6 A/V² | Output drive current (±24mA @3.3V) |
| **Gate Capacitance**   | `CGSO<br>``CGDO`              | 1nF each                                    | Rise/fall times (1.5ns typ)         |
| **Output Resistance**  | `RDSON`                       | 12.5Ω (NMOS)`<br>`33Ω (PMOS)            | VOL=0.3V @24mA                      |
| **Channel Modulation** | `LAMBDA`                      | 0.05 V⁻¹                                  | Typical for LVC family              |
| **Power Capacitance**  | `Cpd`                         | 18pF (typ)                                  | Power dissipation                   |
| **Package Parasitics** | `R_pkg<br>``L_pkg<br>``C_pkg` | 0.1Ω `<br>`2nH `<br>`1pF               | SOT-23 package specs                |

## FILES

### sn74lvc1g04.mod

SPICE model for the inverter gate.

### spice-context.jsonld

Enables  interoperability between SPICE models, JEDEC JEP30 datasheets, and EDS formats.

### sn74lvc1g04.xml

JEDEC JEP30 part model that references the SPICE model

### sn74lvc1g04.json

References elements in the SPICE model
