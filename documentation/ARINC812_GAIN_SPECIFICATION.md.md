# ARINC Specification 812 / 812A Galley Insert Equipment (GAIN) Technical Specification

## 1\. Executive Summary & Purpose

**ARINC Specification 812** ("Standard Data Interface for Galley Insert Equipment") and its evolution **ARINC 812A** define the standardized digital communications, electrical interfaces, operational state transitions, and power shedding protocols for modern commercial passenger aircraft galleys.

In modern airliners (Airbus A350, A380, A330neo, Boeing 787 Dreamliner, 777-300ER, 777X), galleys contain numerous high-power **Galley Insert (GAIN)** devices:

- Convection and steam ovens (ATA 25-30)  
- Espresso and hot beverage makers (ATA 25-30)  
- Air chillers and beverage refrigeration units (ATA 25-30)  
- Rapid water boilers (ATA 25-30)  
- Electro-hydraulic trash compactors (ATA 25-30)  
- Wine chillers and bun warmers

Because total aircraft electrical generation is constrained (especially under single-generator dispatch, de-icing load conditions, or APU backup), the **Galley Network Controller (GNC)** orchestrates all GAIN inserts over a standardized **CAN 2.0B bus network** to dynamically regulate and shed power loads before feeder circuit breakers trip.

---

## 2\. CAN 2.0B 29-Bit Extended Identifier Protocol Framing

Under ARINC 812, communication between GAINs and the GNC is conducted over an **ISO 11898-1 CAN 2.0B** serial data bus operating at a nominal bit rate of **125 kbps** (or optional high-speed **250 kbps**).

### 2.1 29-Bit Identifier Bitfield Map

| Bit Range | Field Name | Description / Bit Allocation |
| :---- | :---- | :---- |
| **Bits 26–28** | Priority | 3 bits. `000` (Highest, Priority 0\) to `111` (Lowest, Priority 7\) |
| **Bit 25** | Reserved | 1 bit. Always set to `0` |
| **Bit 24** | Data Page | 1 bit. Set to `0` for ARINC 812 normative messages |
| **Bits 16–23** | Message Type / PDU Format | 8 bits defining message semantic: `0x01`\=GNC Broadcast, `0x02`\=Config, `0x03`\=Power Request, `0x04`\=Power Grant/Shed, `0x05`\=Telemetry/Status, `0x06`\=BITE/Fault, `0x07`\=Heartbeat |
| **Bits 8–15** | Destination Address | 8-bit destination CAN address (`0x01` for GNC, `0xFF` for broadcast) |
| **Bits 0–7** | Source Address | 8-bit transmitting GAIN node address (`0x10` to `0xFE`) |

---

## 3\. GAIN Power Feeder Architecture & Load Shedding Rules

### 3.1 Aircraft Power Input

- **Nominal Voltage**: 115 VAC RMS phase-to-neutral (3-phase 4-wire Wye).  
- **Frequency**: 400 Hz nominal (380 Hz to 420 Hz variable frequency AC per RTCA DO-160G Section 16).  
- **Galley Feeder A**: Dedicated 8.0 kVA circuit breaker rating.  
- **Galley Feeder B**: Dedicated 6.0 kVA circuit breaker rating.  
- **Total Galley Maximum**: 12.0 kVA (dual-generator operational envelope).  
- **Single-Generator De-rate**: 8.0 kVA total galley cap.

### 3.2 Shedding Priority Hierarchy

When total galley demand or an individual feeder branch exceeds its rated capacity, the GNC executes automatic shedding in strictly deterministic priority sequence:

1. **Priority 1 (Preserved / Non-Sheddable)**: Galley Air Chillers. Essential to preserve the perishable food cold chain (FDA / EASA 4.0°C safety requirement).  
2. **Priority 2 & 3 (High)**: Convection Steam Ovens 1 & 2 during active meal rethermalization cycles.  
3. **Priority 4 (Medium)**: Hot Beverage and Espresso makers during active brewing cycles.  
4. **Priority 5 (Low / Shed First)**: Rapid Water Boilers (can coast thermally for 15–20 minutes without service interruption).  
5. **Priority 6 (Lowest / Shed Immediately)**: Trash Compactors (intermittent mechanical cycle).

---

## 4\. ARINC 429 Discrete Cabin Bus Telemetry

The GNC bridges galley status onto the aircraft Core Cabin Management System (CMS) and Integrated Modular Avionics (IMA) via ARINC 429 discrete bus words:

### Label 264 (Octal 264 / Hex 0xB4): Feeder Load & Shedding Status

- **Bits 11–14**: Feeder A Load (4 bits, 0.5 kVA resolution, 0 to 7.5 kVA)  
- **Bits 15–18**: Feeder B Load (4 bits, 0.5 kVA resolution, 0 to 7.5 kVA)  
- **Bit 19**: Load Shedding Active (`0`\=Normal, `1`\=Shedding Engaged)  
- **Bit 20**: Feeder A Overload Warning (`0`\=Normal, `1`\=Warning)  
- **Bit 21**: Feeder B Overload Warning (`0`\=Normal, `1`\=Warning)  
- **Bits 29–30**: Sign/Status Matrix (SSM: `11` \= Normal Operation)  
- **Bit 32**: Odd Parity over bits 1–31.

### Label 265 (Octal 265 / Hex 0xB5): GAIN Health & Bus Mode

- **Bits 11–16**: Online Active GAIN Count (0 to 63 nodes)  
- **Bits 17–22**: Faulted / Degraded GAIN Count  
- **Bits 23–24**: Aircraft Power Generation Mode (`00`\=Dual Gen Normal, `01`\=Single Gen De-rate, `10`\=APU Power, `11`\=External GPU Ground Power)  
- **Bits 29–30**: Sign/Status Matrix (SSM: `11` \= Normal Operation)  
- **Bit 32**: Odd Parity over bits 1–31.