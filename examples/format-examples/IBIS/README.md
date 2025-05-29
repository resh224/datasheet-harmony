# IBIS Example

Ths example shows a conversion between an IBIS model to an EDS format.  The example part is a SN74LVC1G04 Inverter Gate.

### Key Mappings

| **IBIS Element** | **EDS JSON Element**   | **Conversion Logic**          |
| :--------------------- | :--------------------------- | :---------------------------------- |
| `[Model] Vinl`       | `eds:params[0x1000]`       | Direct value mapping with unit      |
| `[Pulldown] 24mA`    | `eds:params[0x1001]`       | Current-to-UINT16 conversion        |
| `[Pin] Y`            | `eds:communicationObjects` | Logic state mapping for CANopen I/O |
| `[Package] R/L/C`    | `eds:package`              | Structural translation              |

This workflow enables automated conversion from IBIS behavioral models to machine-readable EDS files, preserving electrical context while adding semantic annotations.
