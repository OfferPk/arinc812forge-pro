/**
 * ARINC812Forge Pro — Core Engine
 * Standard Data Interface for Galley Insert (GAIN) Equipment & Galley Network Controller (GNC)
 * Standards: ARINC Specification 812 / 812A, ISO 11898-1 (CAN 2.0B 29-bit), RTCA DO-160G Sec 16
 */

class ARINC812Engine {
  constructor() {
    this.aircraft = {
      type: 'Boeing 777-300ER',
      tailNumber: 'A6-EGA',
      galleyComplex: 'G5 Aft Main Galley',
      electricalBus: '115VAC 400Hz 3-Phase Variable Frequency AC'
    };

    // Feeder Configuration & Thresholds (kVA)
    this.powerFeeders = {
      feederA: {
        id: 'FEEDER_A',
        ratedKva: 8.0,
        currentKva: 0.0,
        voltageVac: 115.0,
        frequencyHz: 400.0,
        status: 'NORMAL'
      },
      feederB: {
        id: 'FEEDER_B',
        ratedKva: 6.0,
        currentKva: 0.0,
        voltageVac: 115.0,
        frequencyHz: 400.0,
        status: 'NORMAL'
      },
      totalMaxKva: 12.0,
      singleGeneratorLimitKva: 8.0,
      singleGeneratorMode: false,
      sheddingEngaged: false
    };

    // Galley Insert Equipment (GAIN) Inventory
    this.gainDevices = [
      {
        id: 'GAIN_CHL_01',
        name: 'Galley Air Chiller Unit',
        type: 'CHILLER',
        ataChapter: '25-30',
        canAddress: 0x31,
        feeder: 'FEEDER_B',
        ratedKva: 1.6,
        actualKva: 1.4,
        priority: 1, // Highest priority (Food safety critical, 4°C rule)
        state: 'RUNNING',
        powerGranted: true,
        temperatureC: 3.8,
        targetTempC: 4.0,
        biteStatus: 'NORMAL',
        faultCode: '0x00'
      },
      {
        id: 'GAIN_OVN_01',
        name: 'Convection Steam Oven 1',
        type: 'OVEN',
        ataChapter: '25-30',
        canAddress: 0x11,
        feeder: 'FEEDER_A',
        ratedKva: 3.2,
        actualKva: 3.1,
        priority: 2,
        state: 'HEATING',
        powerGranted: true,
        temperatureC: 175.0,
        targetTempC: 180.0,
        biteStatus: 'NORMAL',
        faultCode: '0x00'
      },
      {
        id: 'GAIN_OVN_02',
        name: 'Convection Oven 2',
        type: 'OVEN',
        ataChapter: '25-30',
        canAddress: 0x12,
        feeder: 'FEEDER_A',
        ratedKva: 3.2,
        actualKva: 3.0,
        priority: 3,
        state: 'HEATING',
        powerGranted: true,
        temperatureC: 158.0,
        targetTempC: 160.0,
        biteStatus: 'NORMAL',
        faultCode: '0x00'
      },
      {
        id: 'GAIN_BEV_01',
        name: 'Espresso Beverage Maker',
        type: 'BEVERAGE_MAKER',
        ataChapter: '25-30',
        canAddress: 0x21,
        feeder: 'FEEDER_B',
        ratedKva: 2.8,
        actualKva: 2.6,
        priority: 4,
        state: 'BREWING',
        powerGranted: true,
        temperatureC: 92.5,
        targetTempC: 94.0,
        biteStatus: 'NORMAL',
        faultCode: '0x00'
      },
      {
        id: 'GAIN_WTR_01',
        name: 'Rapid Water Boiler',
        type: 'WATER_BOILER',
        ataChapter: '25-30',
        canAddress: 0x41,
        feeder: 'FEEDER_A',
        ratedKva: 2.2,
        actualKva: 2.1,
        priority: 5,
        state: 'STANDBY',
        powerGranted: false, // Shedded or idle
        temperatureC: 78.0,
        targetTempC: 88.0,
        biteStatus: 'NORMAL',
        faultCode: '0x00'
      },
      {
        id: 'GAIN_CMP_01',
        name: 'Electro-Hydraulic Trash Compactor',
        type: 'TRASH_COMPACTOR',
        ataChapter: '25-30',
        canAddress: 0x51,
        feeder: 'FEEDER_B',
        ratedKva: 1.4,
        actualKva: 0.1, // Standby idle
        priority: 6, // Lowest priority (First to shed)
        state: 'STANDBY',
        powerGranted: false,
        temperatureC: 22.0,
        targetTempC: 22.0,
        biteStatus: 'NORMAL',
        faultCode: '0x00'
      }
    ];

    // CAN Bus 2.0B Telemetry Log Buffer
    this.canBusHistory = [];
    this.recomputeFeederLoads();
  }

  // --- ARINC 812 29-bit CAN Identifier Synthesis ---
  encodeCan29BitId(priority, messageType, destinationAddr, sourceAddr) {
    // Priority: Bits 26-28 (0=High, 7=Low)
    // Reserved & Data Page: Bits 24-25 (0b00)
    // Message Type / PDU Format: Bits 16-23 (8 bits)
    // PDU Specific / Destination: Bits 8-15 (8 bits)
    // Source Address: Bits 0-7 (8 bits)
    let canId = 0;
    canId |= (priority & 0x07) << 26;
    canId |= 0 << 24; // Reserved + Data page
    canId |= (messageType & 0xFF) << 16;
    canId |= (destinationAddr & 0xFF) << 8;
    canId |= (sourceAddr & 0xFF);
    return canId >>> 0;
  }

  // --- Dynamic Power Feeder Arbitration & Load Shedding ---
  recomputeFeederLoads() {
    let loadA = 0.0;
    let loadB = 0.0;

    for (const gain of this.gainDevices) {
      if (gain.powerGranted) {
        if (gain.feeder === 'FEEDER_A') loadA += gain.actualKva;
        if (gain.feeder === 'FEEDER_B') loadB += gain.actualKva;
      }
    }

    this.powerFeeders.feederA.currentKva = parseFloat(loadA.toFixed(2));
    this.powerFeeders.feederB.currentKva = parseFloat(loadB.toFixed(2));

    const totalCurrent = loadA + loadB;
    const maxAllowed = this.powerFeeders.singleGeneratorMode 
      ? this.powerFeeders.singleGeneratorLimitKva 
      : this.powerFeeders.totalMaxKva;

    // Check if shedding is required
    if (loadA > this.powerFeeders.feederA.ratedKva || 
        loadB > this.powerFeeders.feederB.ratedKva || 
        totalCurrent > maxAllowed) {
      this.executePowerShedding(maxAllowed);
    } else {
      this.powerFeeders.sheddingEngaged = false;
      this.powerFeeders.feederA.status = 'NORMAL';
      this.powerFeeders.feederB.status = 'NORMAL';
    }
  }

  executePowerShedding(maxAllowedTotal) {
    this.powerFeeders.sheddingEngaged = true;

    // Sort active devices by priority descending (highest numeric value = lowest priority, shedded first)
    const activeGains = this.gainDevices
      .filter(g => g.powerGranted)
      .sort((a, b) => b.priority - a.priority);

    for (const gain of activeGains) {
      // Cannot shed Priority 1 (Food Chiller / Critical)
      if (gain.priority === 1) continue;

      const currentTotal = this.powerFeeders.feederA.currentKva + this.powerFeeders.feederB.currentKva;
      const exceedsFeederA = this.powerFeeders.feederA.currentKva > this.powerFeeders.feederA.ratedKva;
      const exceedsFeederB = this.powerFeeders.feederB.currentKva > this.powerFeeders.feederB.ratedKva;

      if (currentTotal > maxAllowedTotal || (gain.feeder === 'FEEDER_A' && exceedsFeederA) || (gain.feeder === 'FEEDER_B' && exceedsFeederB)) {
        gain.powerGranted = false;
        gain.state = 'SHEDDED';
        if (gain.feeder === 'FEEDER_A') {
          this.powerFeeders.feederA.currentKva = parseFloat((this.powerFeeders.feederA.currentKva - gain.actualKva).toFixed(2));
        } else {
          this.powerFeeders.feederB.currentKva = parseFloat((this.powerFeeders.feederB.currentKva - gain.actualKva).toFixed(2));
        }
        
        // Log CAN Shedding Command (Type 0x04)
        const canId = this.encodeCan29BitId(1, 0x04, gain.canAddress, 0x01);
        this.canBusHistory.push({
          timestamp: new Date().toISOString(),
          canIdHex: '0x' + canId.toString(16).toUpperCase().padStart(8, '0'),
          messageType: 'POWER_SHED_COMMAND',
          targetDevice: gain.id,
          payloadHex: '04 00 00 00' // Shed grant code
        });
      }
    }
  }

  setSingleGeneratorMode(enabled) {
    this.powerFeeders.singleGeneratorMode = enabled;
    this.recomputeFeederLoads();
  }

  injectFault(gainId, faultCode, biteDesc) {
    const gain = this.gainDevices.find(g => g.id === gainId);
    if (!gain) return false;
    gain.biteStatus = 'FAULT';
    gain.faultCode = faultCode;
    gain.state = 'FAULT_ISOLATED';
    gain.powerGranted = false;
    this.recomputeFeederLoads();

    // Log BITE Fault message (Type 0x06)
    const canId = this.encodeCan29BitId(2, 0x06, 0x01, gain.canAddress);
    this.canBusHistory.push({
      timestamp: new Date().toISOString(),
      canIdHex: '0x' + canId.toString(16).toUpperCase().padStart(8, '0'),
      messageType: 'BITE_FAULT_REPORT',
      targetDevice: gain.id,
      payloadHex: `${faultCode} 00 00 00`
    });
    return true;
  }

  // --- ARINC 429 Discrete Bus Telemetry Synthesis ---
  generateARINC429Words() {
    this.recomputeFeederLoads();

    // Label 264 (Octal 264, Hex 0xB4): Cabin Galley Feeder Load & Shedding Status
    const label264 = 0xB4;
    let data264 = 0;

    const feederAStep = Math.min(15, Math.round(this.powerFeeders.feederA.currentKva / 0.5));
    const feederBStep = Math.min(15, Math.round(this.powerFeeders.feederB.currentKva / 0.5));
    const shedBit = this.powerFeeders.sheddingEngaged ? 1 : 0;
    const ovldA = (this.powerFeeders.feederA.currentKva >= this.powerFeeders.feederA.ratedKva) ? 1 : 0;
    const ovldB = (this.powerFeeders.feederB.currentKva >= this.powerFeeders.feederB.ratedKva) ? 1 : 0;

    data264 |= (feederAStep & 0x0F) << 10; // Bits 11-14: Feeder A (0.5 kVA steps)
    data264 |= (feederBStep & 0x0F) << 14; // Bits 15-18: Feeder B (0.5 kVA steps)
    data264 |= (shedBit & 0x01) << 18;     // Bit 19: Shedding Active
    data264 |= (ovldA & 0x01) << 19;       // Bit 20: Feeder A Overload Warning
    data264 |= (ovldB & 0x01) << 20;       // Bit 21: Feeder B Overload Warning
    data264 |= (0x03 & 0x03) << 28;        // Bits 29-30: SSM (Normal Operation)

    let word264 = (data264 & 0x7FFFFF00) | (label264 & 0xFF);
    word264 = this.applyOddParity(word264);

    // Label 265 (Octal 265, Hex 0xB5): GAIN Device Health & BITE Status Summary
    const label265 = 0xB5;
    let data265 = 0;

    const onlineCount = this.gainDevices.filter(g => g.state !== 'FAULT_ISOLATED').length;
    const faultCount = this.gainDevices.filter(g => g.biteStatus === 'FAULT').length;
    const genMode = this.powerFeeders.singleGeneratorMode ? 1 : 0;

    data265 |= (onlineCount & 0x3F) << 10; // Bits 11-16: Active Online GAINs
    data265 |= (faultCount & 0x3F) << 16;  // Bits 17-22: Faulted Devices
    data265 |= (genMode & 0x03) << 22;     // Bits 23-24: Generator Bus Configuration
    data265 |= (0x03 & 0x03) << 28;        // Bits 29-30: SSM

    let word265 = (data265 & 0x7FFFFF00) | (label265 & 0xFF);
    word265 = this.applyOddParity(word265);

    return {
      label264: {
        octal: '264',
        hex: '0x' + (word264 >>> 0).toString(16).toUpperCase().padStart(8, '0'),
        parity: this.verifyOddParity(word264),
        feederAKva: this.powerFeeders.feederA.currentKva,
        feederBKva: this.powerFeeders.feederB.currentKva,
        sheddingActive: this.powerFeeders.sheddingEngaged
      },
      label265: {
        octal: '265',
        hex: '0x' + (word265 >>> 0).toString(16).toUpperCase().padStart(8, '0'),
        parity: this.verifyOddParity(word265),
        onlineGains: onlineCount,
        faultedGains: faultCount,
        singleGenMode: this.powerFeeders.singleGeneratorMode
      }
    };
  }

  applyOddParity(word32) {
    let bits = word32 & 0x7FFFFFFF;
    let count = 0;
    for (let i = 0; i < 31; i++) {
      if ((bits >> i) & 1) count++;
    }
    if (count % 2 === 0) {
      bits |= (1 << 31);
    }
    return bits >>> 0;
  }

  verifyOddParity(word32) {
    let count = 0;
    for (let i = 0; i < 32; i++) {
      if ((word32 >>> i) & 1) count++;
    }
    return count % 2 === 1;
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { ARINC812Engine };
}
